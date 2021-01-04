import cv2
import requests


class RotateVerifyCodeCraker():
    def download_img(self,url):
        html = requests.get(url)
        with open('rotateverifycode.jpg', 'wb') as file:
            file.write(html.content)

    def load_img(self,img_path):
        self.img = cv2.imread(img_path)


if __name__ == "__main__":
    url = 'https://passport.baidu.com/viewlog/img?id=3336-eI8QHJKZjimyIbanpadyBjy1beR79uZRMThC3hZPwf2PTPN68%2Byv9PLkMPkV9N7E5%2BI6mWWIP4bt0NvfP2gkp7f%2BH5VTkmA946Cu6wUHzhJMYdF0Ey9zk1tqes2iLPUY2hshCsXWozothoHJPw%2Fc26qx8lHlR2bMCOcXhA%2FtvOIMarrl4R1xzeoac6e6701tua5J9I%2F6rF1nW2rZcz5nIf1EHTQIou0q1CRzjS9ZAYYChJREj122wWEe4Xl63HCJG9pQZJcczROtXr7jKIEFQZCYgDMS%2FO%2B3OE1A6WhcSBjHgsDaQBaKoZxNZ0g0unLRZbFNSkrrNfM97FaMnDcL4%2BXKyYJGZLBmxnqKHOqzbIM%3D&ak=2ef521ec36290baed33d66de9b16f625&tk=71516ulU0aGpaJRt04I7lwYOkh8K8duXPVby27qHWQYA3vD7wbzEqBzUgMOl%2BucwKaeqBkJsAwQShqAMNfjjBv7jNvgWbaenECF%2BRHu%2FvLk5bs2FKhyRxq%2Bn5pRagodNgoCx'
    r= RotateVerifyCodeCraker()
    r.download_img(url)