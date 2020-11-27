import requests
import json
from urllib import parse
import http.client


class YunPian(object):
    """
    :param: apikey: 用户唯一标识，控制台获取
            mobile: 接收的手机号，支持单号码发送
            text: 已审核短信模板
    :return: {"code": code, "msg": text（成功或者错误信息）, "count": 计费条数}

    """

    def __init__(self, api_key):
        self.api_key = api_key
        self.single_send_url = "https://sms.yunpian.com/v2/sms/single_send.json"

    def send_sms(self, code, mobile):
        # 需要传递的参数
        parmas = {
            "apikey": self.api_key,
            "mobile": mobile,
            "text": "您的验证码是{code}。如非本人操作，请忽略本短信".format(code=code)
        }

        response = requests.post(self.single_send_url, data=parmas)
        re_dict = json.loads(response.text)
        return re_dict


class IHuyi(object):
    """
        :param: apikey: 互亿无线apikey
                apiid: 账户id
                mobile: 接收的手机号，支持单号码发送
                text: "您的验证码是：121254。请不要把验证码泄露给其他人。"
        :return: {"code": code, "msg": text（成功或者错误信息）, "count": 计费条数}

        """

    def __init__(self, apiid="C95643544", api_key="8b4587218bc7cacdfd228dd8b25d3d75"):
        self.api_key = api_key
        self.apiid = apiid
        self.host = "106.ihuyi.com"
        self.sms_send_uri = "/webservice/sms.php?method=Submit"

    def send_sms(self, code, mobile):
        text = "您的验证码是：{code}。请不要把验证码泄露给其他人。".format(code=code)
        params = parse.urlencode(
            {'account': self.apiid, 'password': self.api_key, 'content': text, 'mobile': mobile, 'format': 'json'})
        headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}
        conn = http.client.HTTPConnection(self.host, port=80, timeout=30)
        conn.request("POST", self.sms_send_uri, params, headers)
        response = conn.getresponse()
        response_str = response.read()
        conn.close()
        return response_str


if __name__ == "__main__":
    ihuyi = IHuyi()
    ihuyi.send_sms("123456", 17739462355)
