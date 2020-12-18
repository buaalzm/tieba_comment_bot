from aip import AipOcr
import PIL.Image as img

 
""" 你的 APPID AK SK """
APP_ID = '23155272'
API_KEY = 'qdlYc2dmoxkFqCZyzWpc0Pbq'
SECRET_KEY = 'aK0bY8g09WGuqmGnbiKpzAhqzfjdu4M5'
 

class VerifyCodeCracker():
    def __init__(self,):
        self.client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
        """ 如果有可选参数 """
        self.options = {}
        """ 识别语言类型 """
        self.options["language_type"] = "CHN_ENG"
        """ 检测图片朝向 """
        self.options["detect_direction"] = "false"
        """ 检测语言 """
        self.options["detect_language"] = "false"
        """ 置信度 """
        self.options["probability"] = "false"

    def _get_file_content(self,filePath):
        with open(filePath, 'rb') as fp:
            return fp.read()
        
    def get_code(self,filePath):
        image = self._get_file_content(filePath)
        """ 带参数调用通用文字识别, 图片参数为本地图片 """
        result=self.client.basicGeneral(image, self.options)
        return result


class ImageCroper():
    @staticmethod
    def crop_and_save(image,device_type,name):
        """
        params:
        {
            image[PILimage]
        }
        """
        if device_type=='honor20':
            box = (270,520,810,640) # x1,y1,x2,y2
        if device_type=='simulator':
            box = (360,324,721,402) # x1,y1,x2,y2
        ng = image.crop(box)
        ng.save(name+'temp.jpg')
        ng.save('box.jpg')


if __name__ == "__main__":
    v = VerifyCodeCracker()
    import os
    img_path = os.path.join('../','飞檐走壁temp.jpg')
    print(v.get_code(img_path))