import random,time
from PyQt6.QtCore import QObject,pyqtSignal
import action
import battle

class Worker(QObject):
    finished = pyqtSignal(int)
    progress = pyqtSignal(str,int)
    
    def __init__(self,thread_id=None,index=None,cishu_max=None):
        super().__init__()
        self.game_name='yys'
        self.thread_id = thread_id
        #设置默认功能和次数
        self.func=[{'description':'0 屏幕截图并保存','func_name':0,'count_default':'inf'},\
        {'description':'1 御魂\御灵\觉醒\魂海(单刷)','func_name':self.solo,'count_default':50},\
        {'description':'2 英杰升级','func_name':self.yingjie,'count_default':100},\
        {'description':'3 源赖光技能','func_name':self.yingjiejn,'count_default':30},\
        {'description':'4 魂土\魂海(司机)','func_name':self.yhsj,'count_default':100},\
        {'description':'5 魂土\魂海(打手)','func_name':self.yhds,'count_default':100},\
        {'description':'6 契灵boss(单刷)','func_name':self.guiwang,'count_default':50},\
        {'description':'7 困28','func_name':self.kun,'count_default':30},\
        {'description':'8 活动','func_name':self.guiwang,'count_default':50}]
        #功能序号
        self.index=index
        self.cishu_max=cishu_max
        self.isRunning=False

    def run(self):
        #self.progress.emit('Thread is '+str(self.thread_id),self.thread_id)
        #self.progress.emit('Call function index '+str(self.index)+' with max count of '+str(self.cishu_max),self.thread_id)
        command=self.func[self.index]['func_name']
        command()
        self.finished.emit(self.thread_id)
    
    def message_output(self,msg):
        self.progress.emit(msg,self.thread_id)
    
    #暂停并支持提前停止
    def sleep_fast(self,t=0):
        if not self.isRunning:
            return True
        time.sleep(t)
        return False
    
    ####################################################
    #以下是脚本功能代码
    ####################################################
    #御魂单人
    def solo(self):        
        # 初始化战斗图例
        model = 'solo'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")
        
            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                messages, should_stop = solo_battle.run(screen)
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False
    
    #御魂单人
    def kun(self):        
        # 初始化战斗图例
        model = 'kun'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        other_imgs = action.load_imgs(self.game_name,model, 'other')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_other=other_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")
        
            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                messages, should_stop = solo_battle.run(screen)
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False
    ########################################################
    def ylgsj(self,screen,prepare_imgs):
        for key, want in prepare_imgs.items():
            target=screen
            pts=action.locate(target,want,0) 
            if not len(pts)==0:  
                size = want[0].shape
                h, w , ___ = size                        
                w1 = random.randint(0,50)
                h1 = random.randint(0,40)
                pts1 = (200,500)
                xy1 = action.cheat(pts1,self.thread_id, w1, h1)                       
                action.touch(xy1) 
                t = random.randint(50,100) / 100                              
                time.sleep(t)                  
                xy = action.cheat(pts[0],self.thread_id, w, h)               
                action.touch(xy)        
                return True
            else:
                return False
    
    def yingjiejn(self):
        # 初始化战斗图例
        model = 'yingjiejn'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        prepare_imgs = action.load_imgs(self.game_name,model, 'prepare')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")
            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                if self.ylgsj(screen,prepare_imgs):
                    self.message_output("升级技能")
                    time.sleep(1)
                else:
                    messages, should_stop = solo_battle.run(screen)
                    for msg in messages:
                        self.message_output(msg)
                    if should_stop:
                        self.message_output("任务已终止")
                        break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False        

    ########################################################    
    #鬼王单人
    def guiwang(self):
        # 初始化战斗图例
        model = 'gw'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")
            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                messages, should_stop = solo_battle.run(screen)
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False
    ########################################################
    #英杰单人
    def yingjie(self):
        # 初始化战斗图例
        model = 'yingjie'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")

            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                messages, should_stop = solo_battle.run(screen)
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False
    ########################################################
    #御魂司机
    def yhsj(self):
        # 初始化战斗图例
        model = 'yhsj'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")

            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                messages, should_stop = solo_battle.run(screen)
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False

    ########################################################
    #御魂打手
    def yhds(self):
        # 初始化战斗图例
        model = 'yhds'
        start_imgs = action.load_imgs(self.game_name,model, 'start')
        end_imgs = action.load_imgs(self.game_name,model, 'end')
        loop_imgs = action.load_imgs(self.game_name,model, 'loop')
        try:  
            # 创建 battle 实例
            solo_battle = battle.battle(
                imgs_start=start_imgs,
                imgs_end=end_imgs,
                imgs_loop=loop_imgs,
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
            self.message_output(f"最大挑战次数: {self.cishu_max}")

            while self.isRunning:  # 直到取消，或者出错
                screen = action.screenshot(self.thread_id)
                messages, should_stop = solo_battle.run(screen)
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
                time.sleep(1)

        except Exception as e:
            self.message_output(f"发生错误: {str(e)}")
            self.isRunning = False
    ########################################################
    #结界突破
    def tupo(self):
        tupo_battle = battle.tupo(
                THREAD_ID=self.thread_id,
                CISHU_MAX=self.cishu_max
            )
        self.message_output(f"选择突破:") 
        screen = action.screenshot_small(thread_id,180,120,300,120)
        '''
        while self.isRunning:  # 直到取消，或者出错            
            screen = action.screenshot(self.thread_id)     
            if click == 0:
                self.message_output("准备完成")
                xy = action.cheat(tupo_battle.jiejie_map[n], self.thread_id, tupo_battle.jiejie_width, tupo_battle.jiejie_height)
                action.touch(xy) 
                click = 1              
            else:                    
                messages, should_stop = tupo_battle.run(screen) 
                click = 0
                n = n + 1               
                for msg in messages:
                    self.message_output(msg)
                if should_stop:
                    self.message_output("任务已终止")
                    break
            time.sleep(0.5)
        '''


        
    
