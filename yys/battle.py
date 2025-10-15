import random,time
import action

class battle:
    def __init__(self,imgs_start=None,imgs_end=None,imgs_loop=None,imgs_prepare=None,imgs_other=None,THREAD_ID=None,CISHU_MAX=None,battle_start=[],battle_end=[],battle_other=[]):
        try:       
            self.imgs_start = imgs_start
            self.imgs_end = imgs_end
            self.imgs_loop = imgs_loop
            self.imgs_other = imgs_other
            self.imgs_prepare = imgs_prepare
            self.pts = None
            self.height = None
            self.width = None
            self.THREAD_ID = THREAD_ID
            self.CISHU_MAX = CISHU_MAX
            self.cishu = 0
            self.last_click=''
            self.refresh=0
            self.T_START = [100,200]
            self.T_END = [50,150]
            self.T_OTHER = [15,50]
        except Exception as e:
            print(e)
        
    #是否战斗开始
    def battle_start(self,screen):
        target=screen
        imgs = self.imgs_start
        if imgs==None:
            return False 
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
        
    #是否战斗结束    
    def battle_end(self,screen):
        target=screen
        imgs = self.imgs_end
        if imgs==None:
            return False
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                 
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
    
    #是否正在战斗
    #返回值：True:战斗中，False:不在战斗中
    def battle_loop(self,screen):
        target=screen
        imgs = self.imgs_loop
        if imgs==None:
            return False
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                 
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
    
    #返回值：True:战斗中，False:不在战斗中
    def battle_other(self,screen):
        target=screen
        imgs = self.imgs_other
        if imgs==None:
            return False
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                 
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
    def run(self,screen): 
        messagess = []                             
        if self.battle_start(screen):
             
            w = self.width
            h = self.height
            pts = self.pts
            self.cishu = self.cishu+1
            if self.cishu>self.CISHU_MAX:
                messagess.append('进攻次数上限')
                return messagess,True
            messagess.append('挑战次数：'+str(self.cishu)+'/'+str(self.CISHU_MAX))            
            t = random.randint(self.T_START[0],self.T_START[1]) / 100             
            xy = action.cheat(self.pts,self.THREAD_ID, w, h)  
            time.sleep(t) 
            messagess.append(f"战斗开始，延迟{t}秒，点击:{xy}")                                
            action.touch(xy)              
            return messagess,False
                  
        if self.battle_end(screen):
            flag = random.randint(0,4)
            w = self.width
            h = self.height
            pts = self.pts
            #20%几率点图标
            if flag==-1:
                t = random.randint(self.T_END[0],self.T_END[1]) / 100
            #80%几率点右下角
            else:
                w = w + random.randint(0,20)
                h = h + random.randint(0,20)
                x1 = int(pts[0] * 1.8)
                y1 = pts[1] 
                pts = (x1,y1)
                t = random.randint(self.T_END[0],self.T_END[1]) / 100
            xy = action.cheat(pts,self.THREAD_ID, w, h)
            action.touch(xy)
            time.sleep(t)  
            messagess.append(f"战斗结束，延迟{t}秒，点击:{xy}")                   
             
            return messagess,False
                
        if self.battle_loop(screen):
            w = self.width
            h = self.height
            pts = self.pts
            t = 0.2
            xy = action.cheat(pts,self.THREAD_ID, w, h)                       
            action.touch(xy)                
            time.sleep(t)
            messagess.append(f"战斗中，关闭打扰，点击:{xy}")
            return messagess,False

        if self.battle_other(screen):
            w = self.width
            h = self.height
            pts = self.pts
            t = 0.2
            xy = action.cheat(pts,self.THREAD_ID, w, h)                       
            action.touch(xy)                
            time.sleep(t)
            messagess.append(f"战斗中，点击:{xy}")
            return messagess,False
        
        return messagess,False
    

class tupo:
    def __init__(self,THREAD_ID=None,CISHU_MAX=None):
        try:       
            self.jiejie_point= [(120,180),(420,180),(720,180),
                     (120,300),(420,300),(720,300),
                     (120,420),(420,420),(720,420)]
            self.jiejie_width = 300
            self.jiejie_height = 120
            self.imgs_start = action.load_imgs('yys','tupo', 'start')
            self.imgs_end = action.load_imgs('yys','tupo', 'start')
            self.imgs_loop = action.load_imgs('yys','tupo', 'start')
            self.imgs_prepare = action.load_imgs('yys','tupo', 'start')
            self.pts = None
            self.height = None
            self.width = None
            self.THREAD_ID = THREAD_ID
            self.CISHU_MAX = CISHU_MAX
            self.cishu = 0
            self.last_click=''
            self.refresh=0
            self.T_START = [50,100]
            self.T_END = [100,300]
            self.T_OTHER = [15,50]
        except Exception as e:
            print(e)
        
    #是否战斗开始
    def battle_start(self,screen):
        target=screen
        imgs = self.imgs_start 
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
        
    #是否战斗结束    
    def battle_end(self,screen):
        target=screen
        imgs = self.imgs_end
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                 
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
    
    #是否突破界面
    def battle_prepare(self,screen):
        target=screen
        imgs = self.imgs_prepare
        for key, want in imgs.items():           
            pts=action.locate(target,want,0)
            if not len(pts)==0:                
                return True
        return True
    
    #是否正在战斗
    #返回值：True:战斗中，False:不在战斗中
    def battle_loop(self,screen):
        target=screen
        imgs = self.imgs_loop
        for key, want in imgs.items():
            pts=action.locate(target,want,0)            
            if not len(pts)==0:                 
                size = want[0].shape
                h, w , ___ = size          
                self.pts = pts[0]
                self.height = h
                self.width = w
                return True
        return False
                
    def run(self,screen): 
        messagess = []
        if self.battle_start(screen):                
            w = self.width
            h = self.height
            pts = self.pts
            self.cishu = self.cishu+1
            if self.cishu>self.CISHU_MAX:
                messagess.append('进攻次数上限')
                return messagess,True
            messagess.append('挑战次数：'+str(self.cishu)+'/'+str(self.CISHU_MAX))
            t = random.randint(self.T_START[0],self.T_START[1]) / 100 
            xy = action.cheat(pts,self.THREAD_ID, w, h)                       
            action.touch(xy)                
            time.sleep(t)
            messagess.append(f"战斗开始，延迟{t}秒，点击:{xy}") 
            return messagess,False
                
        if self.battle_end(screen):
            flag = random.randint(0,4)
            w = self.width
            h = self.height
            pts = self.pts
            #20%几率点图标
            if flag==0:
                t = random.randint(self.T_END[0],self.T_END[1]) / 100
            #80%几率点右下角
            else:
                w = w + random.randint(0,20)
                h = h + random.randint(0,20)
                pts = (1060,600)
                t = random.randint(self.T_END[0],self.T_END[1]) / 100
            xy = action.cheat(pts,self.THREAD_ID, w, h)                       
            action.touch(xy)                
            time.sleep(t)
            messagess.append(f"战斗结束，延迟{t}秒，点击:{xy}")
            return messagess,False
                
        if self.battle_loop(screen):
            w = self.width
            h = self.height
            pts = self.pts
            t = 0.2
            xy = action.cheat(pts,self.THREAD_ID, w, h)                       
            action.touch(xy)                
            time.sleep(t)
            messagess.append(f"战斗中，关闭打扰，点击:{xy}")
            return messagess,False
        else:
            time.sleep(0.5)
        return messagess,False



                                        