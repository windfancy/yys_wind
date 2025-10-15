import cv2,time,os,random,sys,mss,copy,subprocess,pyautogui
import config
import numpy
from PyQt6.QtWidgets import QMessageBox,QPushButton,QInputDialog

game_config = config.Config(config_path="config.ini")
#global variables
devices_tab=[None]
adb_enable=[False]
adb_path=None
scalar=False
scaling_factor=1
monitor=None
screen_number = game_config.NTTHREAD
#截屏，并裁剪以加速
HEIGHT = game_config.HEIGHT
WIDTH = game_config.WIDTH
POINTX = game_config.POINTX
POINTY = game_config.POINTY

class monitorclass:
    def __init__(self,number,step_x=WIDTH, step_y=HEIGHT):
        self.width = step_x
        self.height = step_y
        self.monitorscreen=None
        self.monitors = []
        point_x =POINTX.split(",")
        point_y = POINTY.split(",")
   
        for i in range(number):
            x = int(point_x[i])
            y = int(point_y[i])
            mm =  {"top": y, "left": x, "width": step_x, "height": step_y}
            print(mm)
            self.monitors.append(mm)    
    def get_monitor_point(self,index):        
        x = self.monitors[index]['left']
        y = self.monitors[index]['top']
        return x,y
    
monitors = monitorclass(screen_number,WIDTH,HEIGHT)
#默认桌面版
if sys.platform=='darwin':
    scalar=True
    scaling_factor=1/2
else:
    scalar=False
    scaling_factor=1



#initialization thread
def init_thread_variable(nthread):
    global devices_tab,adb_enable
    devices_tab=[None]*nthread
    adb_enable=[False]*nthread

def startup(window):
    global scalar,scaling_factor,monitor,adb_enable,adb_path,devices_tab
    thread_id=window.tabWidget.currentIndex()
    textBrowser=window.tab[thread_id].textBrowser
    pushButton_restart=window.tab[thread_id].pushButton_restart
    textBrowser.append('请把桌面版窗口移动到第一个屏幕的左上角')
    adb_enable[thread_id]=False
    pyautogui.FAILSAFE=False

    #检测系统
    if sys.platform=='darwin' and not adb_enable[thread_id]:
        scalar=True
        scaling_factor=1/2
    else:
        scalar=False
        scaling_factor=1

    #截屏，并裁剪以加速
    upleft = (0, 0)
    if scalar==True:
        downright = (HEIGHT,WIDTH)
    else:
        downright = (HEIGHT, WIDTH)
    a,b = upleft
    c,d = downright
    monitor = {"top": b, "left": a, "width": c, "height": d}

def reset_resolution(window):
    thread_id = window.tabWidget.currentIndex()
    textBrowser=window.tab[thread_id].textBrowser
    pushButton_restart=window.tab[thread_id].pushButton_restart
    if adb_enable[thread_id]:
        textBrowser.append('重置安卓分辨率')
        comm=[adb_path,"-s",devices_tab[thread_id],"shell","wm","size","reset"]
        subprocess.run(comm,shell=False)
        #remove device info
        devices_tab[thread_id]=None
        adb_enable[thread_id]=False
        #日志更新
        textBrowser.append('已断开连接')
        window.tabWidget.setTabText(thread_id, '设备'+str(thread_id+1)+'：桌面版')
        pushButton_restart.setText('连接ADB')

def screenshot(thread_id):
    #屏幕   
    monitor = monitors.monitors[thread_id]
    with mss.mss() as sct:
        if scalar:
            #{"top": b, "left": a, "width": c, "height": d}
            #shrink monitor to half due to macOS default DPI scaling
            monitor2=copy.deepcopy(monitor)
            monitor2["width"]=int(monitor2["width"]*scaling_factor)
            monitor2["height"]=int(monitor2["height"]*scaling_factor)
            screen=sct.grab(monitor2)
            #mss.tools.to_png(screen.rgb, screen.size, output="screenshot.png")
            screen = numpy.array(screen)
            #textBrowser.append('Screen size: ',screen.shape)
            #MuMu助手默认拉伸4/3倍
            screen = cv2.resize(screen, (int(screen.shape[1]*0.75), int(screen.shape[0]*0.75)),
                                interpolation = cv2.INTER_LINEAR)
        else:
            screen = numpy.array(sct.grab(monitor))
    #all else failed
    if screen is None:
        return screen
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    return screen

#在背景查找目标图片，并返回查找到的结果坐标列表，target是背景，want是要找目标
def locate(target,want, show=bool(0), msg=bool(0)):
    loc_pos=[]
    want,treshold,c_name=want[0],want[1],want[2]
    if target is None:
        return loc_pos
    result=cv2.matchTemplate(target,want,cv2.TM_CCOEFF_NORMED)
    location=numpy.where(result>=treshold)
    #textBrowser.append(location)

    if msg:  #显示正式寻找目标名称，调试时开启
        textBrowser.append(c_name,'searching... ')

    h,w=want.shape[:-1] #want.shape[:-1]

    n,ex,ey=1,0,0
    for pt in zip(*location[::-1]):    #其实这里经常是空的
        x,y=pt[0]+int(w/2),pt[1]+int(h/2)
        if (x-ex)+(y-ey)<15:  #去掉邻近重复的点
            continue
        ex,ey=x,y

        cv2.circle(target,(x,y),10,(0,0,255),3)

        if msg:
            textBrowser.append(c_name,'we find it !!! ,at',x,y)

        if scalar:
            x,y=int(x*scaling_factor),int(y*scaling_factor)
        else:
            x,y=int(x),int(y)
            
        loc_pos.append([x,y])

    if show:  #在图上显示寻找的结果，调试时开启
        textBrowser.append('Debug: show action.locate')
        cv2.imshow('we get',target)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()

    if len(loc_pos)==0:
        #textBrowser.append(c_name,'not find')
        pass

    return loc_pos


#按【文件内容，匹配精度，名称】格式批量聚聚要查找的目标图片，精度统一为0.95，名称为文件名
def load_imgs(game_name,model,class_name):
    dpi = f"{str(WIDTH)}_{str(HEIGHT)}"
    #dpi = "845_510"
    mubiao = {}
    acc=0.95
    path = os.getcwd()
    path = f"{path}/{game_name}/png/{dpi}/{model}/{class_name}"
    file_list = os.listdir(path)
    for file in file_list:
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        name = file.split('.')[0]
        file_path = path + '/' + file
        mubiao[name] = cv2.cvtColor(cv2.imread(file_path), cv2.COLOR_BGR2GRAY)
    file_list = os.listdir(path)
    for file in file_list:
        if not file.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
        name = file.split('.')[0]
        file_path = path + '/' + file
        a = [cv2.cvtColor(cv2.imread(file_path),cv2.COLOR_BGR2RGB),acc,name]
        mubiao[name] = a
    return mubiao

#蜂鸣报警器，参数n为鸣叫次数
def alarm(n):
    frequency = 1500
    duration = 500

    if os.name=='nt':
        import winsound
        winsound.Beep(frequency, duration)
    else:
        #os.system('afplay /System/Library/Sounds/Sosumi.aiff')
        sys.stdout.write('\a')
        sys.stdout.flush()

#裁剪图片以缩小匹配范围，screen为原图内容，upleft、downright是目标区域的左上角、右下角坐标
def cut(screen,upleft,downright): 

    a,b=upleft
    c,d=downright
    screen=screen[b:d,a:c]

    return screen

#随机偏移坐标，防止游戏的外挂检测。p是原坐标，w、n是目标图像宽高，返回目标范围内的一个随机坐标
def cheat(p,theard_id, w, h):
    a,b = p
    monitor_x,monitor_y = monitors.get_monitor_point(theard_id)
    a = a + monitor_x
    b = b + monitor_y
    if scalar:
        w, h = int(w/3/2), int(h/3/2)
    else:
        w, h = int(w/3), int(h/3)
    if h<0:
        h=1
    c,d = random.randint(-w, w),random.randint(-h, h)
    e,f = a + c, b + d
    y = [e, f]
    return(y)

# 点击屏幕，参数pos为目标坐标
def touch(pos):
    x, y = pos 
    pyautogui.click(pos)
def swipe(pos,thread_id):
    x, y = pos
    dy=800
    x1=x
    if y>dy:
        y1=y-dy
    else:
        y1=1
    
    if adb_enable[thread_id]:
        comm=[adb_path,"-s",devices_tab[thread_id],"shell","input","touchscreen","swipe",str(x),str(y),str(x1),str(y1)]
        #print(comm)
        #textBrowser.append('Command: ',comm)
        subprocess.run(comm,shell=False)
    else:
        pyautogui.click(pos)

def screenshot_small(thread_id,left,top,w,h):
    #屏幕   
    monitor = monitors.monitors[thread_id]
    monitor['top'] = monitor['top'] + top
    monitor['left'] = monitor['left'] + left
    monitor["width"]=int(w*scaling_factor)
    monitor["height"]=int(h*scaling_factor) 
    with mss.mss() as sct:
        if scalar:
            #{"top": b, "left": a, "width": c, "height": d}
            #shrink monitor to half due to macOS default DPI scaling
            monitor2=copy.deepcopy(monitor)
            monitor2["width"]=int(monitor2["width"]*scaling_factor)
            monitor2["height"]=int(monitor2["height"]*scaling_factor)            
            screen=sct.grab(monitor2)
            #mss.tools.to_png(screen.rgb, screen.size, output="screenshot.png")
            screen = numpy.array(screen)
            #textBrowser.append('Screen size: ',screen.shape)
            #MuMu助手默认拉伸4/3倍
            screen = cv2.resize(screen, (int(screen.shape[1]*0.75), int(screen.shape[0]*0.75)),
                                interpolation = cv2.INTER_LINEAR)
        else:
            print(monitor)
            screen = numpy.array(sct.grab(monitor))
    #all else failed
    if screen is None:
        return screen
    screen = cv2.cvtColor(screen, cv2.COLOR_BGR2RGB)
    cv2.imwrite('ceshi.png', cv2.cvtColor(screen, cv2.COLOR_RGB2BGR))
    return screen

if __name__ == "__main__":
    thread_id = 0  # 假设当前线程ID为0
    points= [(120,180),(420,180),(720,180),
                     (120,300),(420,300),(720,300),
                     (120,420),(420,420),(720,420)]
    point = points[3]
    top = point[1]
    left = point[0]
    width = 300
    height = 120
    screen = screenshot_small(thread_id,left,top,width,height)