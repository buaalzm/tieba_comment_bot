"""
导入namelist目录下的txt文件，里面存有待搜索的项目
"""
import os


class FileLoader():
    name_list = []
    def loadfile(self,filename):
        with open(os.path.join(os.path.dirname(__file__),'../','namelist',filename),"r",encoding='utf-8') as f:    #设置文件对象
            data = f.read()    #可以是随便对文件的操作
            self.name_list = data.split('\n')
        self.name_list = [item for item in self.name_list if item] # 去除空值
        self.name_num = len(self.name_list)
    
    def set_start(self,name):
        """
        设定起始名称
        name[str]
        """
        assert name in self.name_list
        index = 0
        for item in self.name_list:
            if name==item:
                break
            index = index+1
            self.name_list = self.name_list[index:]

    def get_name_list(self):
        return self.name_list


if __name__ == "__main__":
    f = FileLoader()
    # f.loadfile('phone.txt')
    f.loadfile('movie.txt')
    # f.loadfile('game.txt')
    print(f.name_list)