#!/usr/bin/env python3
# coding:utf-8
# @Author: yumu
# @Date:   2020-04-15
# @Email:   yumusb@foxmail.com
# @Last Modified by:   yumu
# @Last Modified time: 2020-04-16
import logging
import traceback

# 支付需要用到的
from alipay.aop.api.AlipayClientConfig import AlipayClientConfig
from alipay.aop.api.DefaultAlipayClient import DefaultAlipayClient
from alipay.aop.api.domain.AlipayTradePayModel import AlipayTradePayModel
from alipay.aop.api.request.AlipayTradePayRequest import AlipayTradePayRequest
from alipay.aop.api.response.AlipayTradePayResponse import AlipayTradePayResponse


# 扫码需要用到的
from io import BytesIO
from time import sleep,time
from picamera import PiCamera
from PIL import Image
from pyzbar.pyzbar import decode

def scan():
    stream = BytesIO()
    camera = PiCamera()
    camera.start_preview()
    sleep(2)
    #camera.capture('new.jpg') 保存图片，利于查看效果
    camera.capture(stream, format='jpeg')
    # "Rewind" the stream to the beginning so we can read its content
    stream.seek(0)
    image = Image.open(stream)
    camera.close()
    try:
        decodedata=decode(image)
        if(len(decodedata)==0):
            return ""
            #未解码出数据，结果集长度为0
        userinfo=decodedata[0].data
        if(len(userinfo)==18):
            return userinfo
        else:
            print(f"{userinfo}不是正确的收款码")
            # userinfo 是18位数字，且以28开头。
            return ""
    except Exception as e:
        print(traceback.format_exc())
        return ""

def pay(userinfo):
    """
    设置配置，包括支付宝网关地址、app_id、应用私钥、支付宝公钥等，其他配置值可以查看AlipayClientConfig的定义。
    """
    alipay_client_config = AlipayClientConfig()
    alipay_client_config.server_url = 'https://openapi.alipay.com/gateway.do'
    alipay_client_config.app_id = '' # appid
    alipay_client_config.app_private_key = '' # 用户私钥
    alipay_client_config.alipay_public_key = '' # 支付宝公钥（填入用户私钥，返回的支付宝公钥，而不是上面用户私钥对应的公钥，如果不会配置的话可以看我另一项目中的文档 https://github.com/yumusb/alipay-f2fpay/tree/master/%E5%AF%86%E9%92%A5%E5%AF%B9%E7%94%9F%E6%88%90%E4%B8%8E%E8%AE%BE%E7%BD%AE%E6%95%99%E7%A8%8B）

    """
    得到客户端对象。
    注意，一个alipay_client_config对象对应一个DefaultAlipayClient，定义DefaultAlipayClient对象后，alipay_client_config不得修改，如果想使用不同的配置，请定义不同的DefaultAlipayClient。
    logger参数用于打印日志，不传则不打印，建议传递。
    """
    #client = DefaultAlipayClient(alipay_client_config=alipay_client_config, logger=logger)
    client = DefaultAlipayClient(alipay_client_config=alipay_client_config)
    """
    系统接口示例：alipay.trade.pay
    """
    # 对照接口文档，构造请求对象
    model = AlipayTradePayModel()
    model.auth_code = userinfo
    model.subject = "Test" # 订单标题
    model.out_trade_no = time() # 订单账号
    model.scene = "bar_code"
    model.total_amount = 0.01 # 订单金额
    request = AlipayTradePayRequest(biz_model=model)
    response_content = None
    try:
        response_content = client.execute(request)
    except Exception as e:
        print(traceback.format_exc())
    if not response_content:
        print("failed execute")
    else:
        response = AlipayTradePayResponse()
        # 解析响应结果
        response.parse_response_content(response_content)
        #print(response.body)
        #返回结果集，如果不能成功支付的话，建议输出以排错
        if response.is_success():
            # 如果业务成功，则通过respnse属性获取需要的值
            print("get response trade_no:" + response.trade_no)
        else:
            # 如果业务失败，则从错误码中可以得知错误情况，具体错误码信息可以查看接口文档
            print(response.code + "," + response.msg + "," + response.sub_code + "," + response.sub_msg)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    filemode='a',)
logger = logging.getLogger('')


if __name__ == '__main__':
    i=1
    while True:
        print(f"第{i}次识别尝试,请展示付款码")
        userinfo=scan()
        i=i+1
        if(len(userinfo)==18):
            pay(userinfo.decode())
            exit()

