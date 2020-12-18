class Config():
    def __init__(self,username,device,item_type):
        self.username = username
        self.device = device
        self.item_type = item_type

# 模拟器屏幕分辨率为 1080，2232
bot1_simu_game = Config(username='jougg时代',device='127.0.0.1:62001',item_type='game')
bot2_simu_game = Config(username='飞檐走壁',device='127.0.0.1:62025',item_type='game')
