import requests
import hashlib
import random
import time
from random import Random
from bs4 import BeautifulSoup


APP_ID = 'wx34ab6ee729131856'   # 网站id
MCH_ID = '1543940791'    # 商户号
API_KEY = 'R1YMmmrlyoDPRIhukY5yyBsGTD071sck'  # 微信秘钥


def wxpay(amount, out_trade_no):
    nonce_str = random_str()  # 随机字符串32位

    order_dict = {
        'appid': APP_ID,
        'mch_id': MCH_ID,
        'nonce_str': nonce_str,
        'body': '黑云信息科技'.encode("utf-8"),
        # 'body': '黑云信息科技',
        'out_trade_no': out_trade_no,
        'total_fee': amount,
        'notify_url': 'www.heiyunworld.com/payment.post',
        'trade_type': 'NATIVE',
    }
    print(order_dict)
    order_sign = get_sign(order_dict, API_KEY)
    # 将sign加入请求数据中settings.
    order_dict['sign'] = order_sign
    # 转为xml格式
    order_xml = trans_dict_to_xml(order_dict)
    print(order_xml)
    # 请求下单接口
    res = requests.post(url='https://api.mch.weixin.qq.com/pay/unifiedorder', data=order_xml)
    # 将返回数据转为字典
    res_dict = trans_xml_to_dict(res.content)
    if res_dict.get('return_code') == 'SUCCESS':  # 如果请求成功
        print(res_dict.get('code_url'))
        code_url = res_dict.get("code_url")
        return {"status": "success", "code_url": code_url, "sign": order_sign}
    else:
        return {"status": "fail"}


def trans_dict_to_xml(data_dict):
    data_xml = []
    for k in sorted(data_dict.keys()):  # 遍历字典排序后的key
        v = data_dict.get(k)  # 取出字典中key对应的value
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml))  # 返回XML


# XML转字典
def trans_xml_to_dict(data_xml):
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict





def get_sign(data_dict, key):  # 签名函数，参数为签名的数据和密钥
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    md5 = hashlib.md5()  # 使用MD5加密模式
    md5.update(params_str.encode())  # 将参数字符串传入
    sign = md5.hexdigest().upper()  # 完成加密并转为大写
    return sign


# 生成订单号
def order_num(package_id=random.randint(999, 9999), user_id=random.randint(999, 9999)):
    # 商品id后2位+下单时间的年月日12+用户2后四位+随机数4位
    local_time = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))[2:]
    result = str(package_id)[-2:] + local_time + str(user_id)[-2:] + str(random.randint(1000, 9999))
    return result


# 生成随机字符串
def random_str(randomlength=32):
    str = ''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(randomlength):
        str += chars[random.randint(0, length)]
    return str


if __name__ == '__main__':
    print(wxpay(1))