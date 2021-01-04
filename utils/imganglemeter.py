import cv2
import os
import numpy as np
import matplotlib.pyplot as plt


class ImgAngleMeter(object):
    """
    计算图片旋转的角度
    """
    def __init__(self):
        # self.outpath = os.path.join(os.path.dirname(__file__),'../','img')
        self.img_prefix = 'rotateverifycode'
        self.img_list = []

    def load_img(self,img):
        for i in range(1, 9):
            name = self.img_prefix + str(i) + '.jpg'
            self.img_list.append(cv2.imread(name))

    def line(self,img,angle=np.pi,thre=50,minLineLength=100,maxLineGap=10):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gaus = cv2.GaussianBlur(gray,(3,3),0)
        edges = cv2.Canny(gaus, 50, 150, apertureSize=3)
        thre = thre
        minLineLength = minLineLength
        maxLineGap = maxLineGap
        angle = angle
        lines = cv2.HoughLinesP(edges, 1, angle / 180, thre, minLineLength, maxLineGap)

        for line in lines:
            x1, y1, x2, y2 = line[0]
            cv2.line(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
        return img