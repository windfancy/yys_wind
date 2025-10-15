import os,configparser
class Config:
    def __init__(self, config_path=None):
        if config_path is None:
            config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
        else:
            if os.path.exists(config_path):
                print("config.ini")
            else:
                print("未找到config.ini")
                return None
        con = configparser.ConfigParser(inline_comment_prefixes=';')
        con.sections()
        con.read(config_path)
        #inputs from terminal
        self.DEBUG = con['general']['debug'].lower()
        self.GAME_NAME = con['general']['game']
        self.NTTHREAD = int(con['general']['Nthread'])
        self.HEIGHT = int(con['general']['height'])
        self.WIDTH = int(con['general']['width'])
        self.POINTX = con['general']['x']
        self.POINTY = con['general']['y']


    

