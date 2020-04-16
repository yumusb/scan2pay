# scan2pay

## 介绍

本项目代码是利用树莓派+摄像头模块+支付宝当面付来实现扫码枪功能。

演示截图：

![演示截图](https://cdn.jsdelivr.net/gh/yumusb/blog_img@latest/upload/2020/04/01.gif)

本文基本上是对支付宝SDK和其他模块demo的拼合，仅仅达到支付功能。可以帮助初学者理解相关功能。如果需要用在正式环境中，还需要大幅修改。

## 使用

```python3
git clone https://github.com/yumusb/scan2pay.git
#克隆该仓库
cd scan2pay/
pip3 install -r requirements.txt
#安装所需依赖库

#检查配置选项（注释写的比较多，可以先去支付宝文档理解大致支付流程，然后连接摄像头测试是否连接成功，再进行扫码支付测试）
python3 main.py
#开始支付
```

## 链接

+ 支付宝当面付产品文档 https://opendocs.alipay.com/open/194/
+ 支付宝支付SDK-Python https://github.com/alipay/alipay-sdk-python-all
+ picamera模块文档 https://picamera.readthedocs.io/en/release-1.13/recipes1.html

## 关于

+ 捐献 http://33.al/donate
+ 博客 http://33.al