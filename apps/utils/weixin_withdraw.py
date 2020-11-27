# -*- coding:utf-8 -*-

import hashlib
import random
import string
import time
import re


class WeChatWithdraw:
    def __init__(self, wx_app_id, wx_mch_id, wx_api_key):
        self.wx_app_id = wx_app_id
        self.wx_mch_id = wx_mch_id
        self.wx_api_key = wx_api_key

    def sign(self, raw):
        raw = [(k, str(raw[k]) if isinstance(raw[k], (int, float)) else raw[k]) for k in sorted(raw.keys())]
        s = "&".join("=".join(kv) for kv in raw if kv[1])
        s += "&key={0}".format(self.wx_api_key)
        return hashlib.md5(self.to_utf8(s)).hexdigest().upper()

    def to_xml(self, raw):
        s = ""
        for k, v in raw.items():
            s += "<{0}>{1}</{0}>".format(k, self._to_utf8(str(v)), k)
        return "<xml>{0}</xml>".format(s)

    def withdraw_serial_number(self):
        return '{0}{1}{2}'.format(self.wx_mch_id, time.strftime('%Y%m%d', time.localtime(time.time())),
                                  self.random_num())

    @staticmethod
    def to_utf8(raw):
        return raw.encode("utf-8") if isinstance(raw, str) else raw

    @staticmethod
    def _to_utf8(raw):
        return raw.encode("utf-8") if re.match("[\u4e00-\u9fa5]+", raw) else raw

    @staticmethod
    def nonce_str(length=32):
        char = string.ascii_letters + string.digits
        return "".join(random.choice(char) for _ in range(length))

    @staticmethod
    def random_num(length=10):
        digit_list = list(string.digits)
        random.shuffle(digit_list)
        return "".join(digit_list[:length])




if __name__ == '__main__':
    raw_ = {"1": "time", "2": 3}
    a = WeChatWithdraw(1, 2, 4)
    print(a.to_xml({'appid': 'wxd930ea5d5a258f4f', 'mch_id': '10000100', 'device_info': '1000', 'body': 'test', 'nonce_str': 'ibuaiVcKdpRxkhJA', 'sign': '9A0A8659F005D6984697E2CA0A9CF3B7'}))
    print(a.sign({'appid': 'wxd930ea5d5a258f4f', 'mch_id': '10000100', 'device_info': '1000', 'body': 'test', 'nonce_str': 'ibuaiVcKdpRxkhJA', 'sign': '9A0A8659F005D6984697E2CA0A9CF3B7'}))