from botmanager import BotManager
from userconfig import *

from copy import deepcopy
from tqdm import tqdm
import os
from random import sample
import time
from tkinter import messagebox


def task_stack(cfg_list,iter_num=20,sleep_time=60):
    bm_list = []
    for cfg in cfg_list:
        bm_list.append({'cfg':cfg,'bm':BotManager(username=cfg.username,device=cfg.device,item_type=cfg.item_type)})
    index = 0
    for bm_dict in bm_list:
        for _ in range(iter_num):
            name = bm_dict['cfg'].username
            bm = bm_dict['bm']
            print('simulator:',name)
            bm.run_one()
            index += 1 
            print('finish:',index)
            time.sleep(sleep_time)
        time.sleep(300)

if __name__ == "__main__":
    # cfg = bot1_simu_game # jougg时代 #
    # cfg = bot2_simu_game # 飞檐走壁
    # cfg = bot3_simu_game # bilun
    # cfg = bot4_simu_game # 悟天逸 #
    # cfg = bot5_simu_game # 斯坦赛德
    # cfg = bot6_simu_game # 阿拉斯 #
    # cfg = bot7_simu_game # 5z5531j3TF
    # cfg = bot8_simu_game # XS22oS3LA #
    # cfg = bot9_simu_game # L7t8p14DKpb #
    cfg = bot10_simu_game # 雷躺净刈砸狭
    # cfg = bot11_simu_game # hxacefbo37702
    # cfg = bot12_simu_game # E42Qa0W6Y
    # cfg = bot13_simu_game # TS18M3yWeRL4
    # cfg = bot14_simu_game # 我是胸手_y8m #
    # cfg = bot15_simu_game # 官靡囱馗弛剿
    # cfg = bot16_simu_game # 77HZ5Vb73P #
    # cfg = bot17_simu_game # 定蒂维置
    # cfg = bot18_simu_game # 陌腋裙顾假等 #
    # cfg = bot19_simu_game # 烫渣惧嚏闻煌 #

    bm = BotManager(username=cfg.username,device=cfg.device,item_type=cfg.item_type)
    bm.run(4)
    messagebox.showinfo(message='finish')
    os.system('taskkill /f /t /im '+'nox.exe')

    # cfg_list = [bot7_simu_game,bot8_simu_game,bot9_simu_game,bot10_simu_game]
    # task_stack(cfg_list)

    # bm.bot.recover_comment(max_count=2)