# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class PhoneItem(Item):
    # define the fields for your item here like:
    # name = Field()
    pass

class PhoneCommentUrlItem(Item):
    name = Field()
    url = Field()

class PhoneCommentItem(Item):
    name = Field() # 名称
    like = Field() # 最喜欢
    dislike = Field() # 最不喜欢
    appearance = Field() # 外观
    performance = Field() # 性能
    fluency = Field() # 流畅度
    camera = Field() # 相机拍照
    other = Field() # 其他描述

class PhoneScoreItem(Item):
    name = Field() # 名称
    score = Field() # 评分
    cheap = Field() # 性价比
    display = Field() # 屏幕显示
    fluency = Field() # 流畅度
    battery = Field() # 电池续航
    camera = Field() # 相机拍照