from botmanager import BotManager
from userconfig import *

from copy import deepcopy
from tqdm import tqdm
import os


if __name__ == "__main__":
    cfg = bot1_simu_game
    # cfg = bot2_simu_game
    bm = BotManager(username=cfg.username,device=cfg.device,item_type=cfg.item_type)
    bm.run()