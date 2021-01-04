import uiautomator2 as u2
import time
from datetime import datetime
import subprocess
import os
import PIL.Image as img
from utils.verifycodecrack import VerifyCodeCracker, ImageCroper


class TiebaBot():
    def __init__(self,device=None,save_file_name=None,log_file_name=None,item_type='',username=''):
        """
        params:
        {
            device[str]:adb devices中查询到的要连接的设备，如果只连一个设备可为空
            save_file_name[str]:输出的文件名，文件保存到out目录下
            log_file_name[str]:日志的名字，输出到log目录下
            item_type[str]:为'game'或'phone'
        }
        """
        # self.d = u2.connect_usb(device)
        self.wait_until_connect(device=device)
        self.tieba_init()
        print(self.d.device_info)
        self.device = self.d.device_info['serial']
        self.type = item_type
        self.username = username
        self.savename = save_file_name if save_file_name else datetime.now().strftime("%Y-%m-%d")+'.txt'
        self.logname = log_file_name if log_file_name else datetime.now().strftime("%Y-%m-%d")+'.log'
        self.log('devices start',str(self.d.device_info))
        self.log('init','username:{},item type:{}'.format(username,item_type))
        print("启动时要先打开贴吧app，点开搜索，否则会造成指令链紊乱")
        self.d = u2.connect(device)
        self.codecracker = VerifyCodeCracker()

        if '127.0.0.1' in device:
            self.device_type = 'simulator'
        if device == 'CUY0219618008985':
            self.device_type = 'honor20'

    def wait_until_connect(self,device,max_try=20):
        """
        一直尝试连接设备，连上为止
        """
        succ = False
        count = 0
        while not succ:
            try:
                self.d = u2.connect_usb(device)
                succ = True
            except:
                count +=1
                print('连接尝试第{}次，剩余{}次'.format(count,max_try-count))
                if count==max_try:
                    exit()
                time.sleep(5)

    def tieba_init(self):
        while not self.d(resourceId="com.baidu.tieba:id/home_et_search").exists():
            if self.d(resourceId="com.baidu.tieba:id/cancel_download_button").exists():
                self.d(resourceId="com.baidu.tieba:id/cancel_download_button").click()
                time.sleep(0.5)
                continue
            if self.d(resourceId="com.baidu.tieba:id/search").exists():
                self.d(resourceId="com.baidu.tieba:id/search").click()
                time.sleep(0.5)
                continue
            if self.d(text="谷歌安装器").exists():
                self.d.app_start("com.baidu.tieba")
                time.sleep(5)
            if self.d(text="系统删贴").exists():
                return

        
    
    def action(self,subject,comment,star):
        """
        入口是点开首页的搜索框，完成的时候也是到这里。
        params：
        {
            subject[str]:是粘进去就能进贴吧的贴吧名
        }
        """ 
        self.d(resourceId="com.baidu.tieba:id/home_et_search").set_text(subject)
        time.sleep(0.5)
        if not self.d(resourceId="com.baidu.tieba:id/searchSuggestTitle").exists():
            # 贴吧不存在
            self.log(subject,'没有出现补全的搜索项,点击灰叉，准备下一次搜索')
            self.prepare_next() # 点击灰叉，准备下一次搜索
            return False
        
        self.d(resourceId="com.baidu.tieba:id/searchSuggestTitle").click() # 点击补全的项，进入贴吧
        time.sleep(5)

        if self.device_type=='honor20':
            self.d.click(0.516, 0.205)# 真正进入贴吧
        if self.device_type=='simulator':
            self.d.click(0.57, 0.154)

        self.log(subject,'进入贴吧')

        # 这里要判断有没有评价
        time.sleep(2)
        if not self.d(text="评价").exists():
            # 没有评价入口
            self.log(subject,'没找到评价入口,点击灰叉，准备下一次搜索')
            self.prepare_next()
            return False
        self.d.xpath('//*[@text="评价"]').click() # 开始评价
        time.sleep(1)
        # self.d(resourceId="com.baidu.tieba:id/evaluate_container").click()
        self.d(text="点击发布评价").click()
        self.log(subject,'进入评价界面')
        # 进入评价界面
        time.sleep(2)

        self.put_comment(subject=subject,comment=comment,star=star)

        time.sleep(0.5)
        self.share()
        time.sleep(0.5)
        url = self.d.clipboard
        assert url != None
        print('url:{}'.format(url))
        self.url_save(subject=subject,url=url)
        self.d.press("back")
        self.log(subject,'点击灰叉，准备下一次搜索')
        time.sleep(0.5)
        self.d(resourceId="com.baidu.tieba:id/home_bt_search_del").click() # 点击灰叉，准备下一次搜索
        time.sleep(0.5)
        return True

    def put_comment(self, subject,comment,star=5):
        """
        在评论界面的操作
        params:
        {
            subject[str]:
            comment[str]
            star[int]
        }
        """
        comment = comment
        self.add_star(star)
        self.log(subject,'{}星'.format(str(star)))
        self.log(subject,comment)
        self.d(resourceId="com.baidu.tieba:id/post_content").set_text(comment) # 添加评论内容
        time.sleep(5)
        self.d(text="发布").click() # 评价
        time.sleep(0.5)
        while self.d(text="发布").exists():
            time.sleep(0.3)
            self.d(text="发布").click() # 评价
            time.sleep(0.5)

        time.sleep(1.5)
        # 这里要判断验证码

        if self._in_verify_code_page():
            self.veryfycode_pass()
            # 处理验证码

        if self.d(resourceId="com.baidu.tieba:id/new_user_anim").exists():
            # 弹出勋章
            self.log(subject,'处理弹窗')
            self.d.press("back")
            time.sleep(1)

    def add_star(self,star):
        """
        点星星，按坐标去点，换设备这个要重新调试
        """
        if self.device_type=='honor20':
            if star==1:
                self.d.click(0.31, 0.296)
            elif star==2:
                self.d.click(0.401, 0.296)
            elif star==3:
                self.d.click(0.50, 0.296)
            elif star==4:
                self.d.click(0.593, 0.295)
            elif star==5:
                self.d.click(0.689, 0.296)
        if self.device_type=='simulator':
            if star==1:
                self.d.click(0.35, 0.221)
            elif star==2:
                self.d.click(0.424, 0.222)
            elif star==3:
                self.d.click(0.501, 0.222)
            elif star==4:
                self.d.click(0.572, 0.221) 
            elif star==5:
                self.d.click(0.649, 0.22)

    def share(self):
        """
        点击分享，将分享链接粘贴到剪贴板
        """
        # self.d.swipe(21, 1533, 21, 800) # 往下滑一点，防止分享按钮不在屏幕中
        self.d(resourceId="com.baidu.tieba:id/share_num_img").click(timeout=30)
        self.d.xpath('//android.view.ViewGroup/android.widget.LinearLayout[6]/android.widget.ImageView[1]').click()

    def url_save(self,subject,url,filename=''):
        """
        将分享的链接写入文件
        params:
        {
            subject[str]:主题
            url[str]:分享链接
        }
        """
        filename = filename if filename else self.savename
        if not url:
            return
        curr_dir = os.path.dirname(__file__)
        filename = os.path.join(curr_dir,'out',filename)
        with open(filename, 'a+',encoding='utf-8') as f:
            f.write(subject+' '+url+'\n')

    def log(self,subject,comment,filename=''):
        """
        生成日志文件
        params:
        {
            subject[str]:
            comment[str]:要写入日志的内容
        }
        """
        filename = filename if filename else self.logname
        curr_dir = os.path.dirname(__file__)
        filename = os.path.join(curr_dir,'log',filename)
        with open(filename, 'a+',encoding='utf-8') as f:
            f.write(subject+' '+comment+'\n')

    def prepare_next(self):
        """
        点飞的时候，试图找回去，回到搜索界面
        """
        while True:
            if self.d(text='谷歌安装器').exists(): 
                self.log("寻路程序",'回到了桌面')
                self.d.app_start('com.baidu.tieba')
                time.sleep(1)
            if self.d(resourceId="com.baidu.tieba:id/search").exists():
                self.log('寻路程序','已回到首页')
                self.d(resourceId="com.baidu.tieba:id/search").click()
                time.sleep(1)
                return
            if self.d(resourceId="com.baidu.tieba:id/home_bt_search_del").exists(): 
                self.log("寻路程序",'找到灰叉')
                self.d(resourceId="com.baidu.tieba:id/home_bt_search_del").click()# 点击灰叉，准备下一次搜索:
                time.sleep(1)
                return
            if self.d(text='不保存').exists(): 
                self.log("寻路程序",'不保存')
                self.d(text='不保存').click() 
                time.sleep(0.5)
            if self.d(text='知道啦').exists(): 
                self.log("寻路程序",'知道啦')
                self.d(text='知道啦').click() 
                time.sleep(1)
            self.d.press("back")
            self.log('寻路程序','点击返回')
            time.sleep(1)
    
    def save_veri_code_image(self):
        image = self.d.screenshot()
        image.save('screenshot.jpg')
        ImageCroper.crop_and_save(image,self.device_type,name=self.username)

    def ocr(self):
        box_name = self.username+'temp.jpg'
        self.save_veri_code_image()
        while not os.path.exists(box_name):
            time.sleep(0.5)
        
        code = self.codecracker.get_code(box_name)
        os.remove(box_name) # 用完删除，防止下一次识别了上一次的图片
        if code['words_result']:
            return code['words_result'][0]['words']
        else:
            return ''
        
    def veryfycode_pass(self):
        while self._in_verify_code_page():
            result = self.ocr()
            self.d(resourceId='com.baidu.tieba:id/input').set_text(result)
            print('验证码识别结果：'+result)
            self.d(resourceId="com.baidu.tieba:id/right_textview").click() # 点击发帖
            time.sleep(1)

    def _in_verify_code_page(self):
        time.sleep(0.5)
        return self.d(text='点击验证码图片换一张').exists()

    def recover_comment(self,max_count=10):
        """
        申诉被删的帖
        在帖子回收站启动
        """
        count = 0
        while self.d(text='申请恢复').exists() or not self.d(text='暂无更多').exists():
            # 跳出的条件：刷到“暂无更多”（到底了） and 没有“申请恢复”
            if not self.d(text='申请恢复').exists():
               self.d.swipe(0.532, 0.609, 0.513, 0.271) # 往下滑动
               continue
            time.sleep(0.5)
            self.d(text='申请恢复').click()
            time.sleep(1.5)
            
            self.d(resourceId='reason').click()
            self.d.send_keys('参加贴吧百万内容活动，被系统误封。。')
            time.sleep(1)
            self.d(resourceId='apply').click()
            time.sleep(1)
            
            time.sleep(1)
            count+=1
            if count == max_count:
                break
        print('申请数量:{}'.format(count))


if __name__ == "__main__":
    t = TiebaBot(device='127.0.0.1:62001')
    # t.save_veri_code_image()
    # t.ocr()
    t.veryfycode_pass()