# coding:utf-8
# _author_:Junjie
# date:2019/6/21
import datetime
import hashlib
import os
import re
import threading
import time
import uuid
from os import mkdir

import requests
import json
from decimal import Decimal
from RPC.config import command_head
from RPC.setting import command_node_ip, command_node_port
from ListSet import ListSet

# _thread_id_ = 0
mid_result_dict = {}
lock = threading.RLock()
result_list = []
requests.adapters.DEFAULT_RETRIES = 15
s = requests.session()
s.keep_alive = False


deliver_node_ip = '127.0.0.1'
deliver_node_port = '9100'


def create_task_id():
    return str(uuid.uuid1())

def changeBack(word):
    return word

def change(word):
    return word



def run_task(t):
    # print(t)
    destinip = '127.0.0.1'
    destinport = '9100'
    send_time = datetime.datetime.now()
    content = str(t)
    start = time.time()
    info = {'head': command_head['send_db_task'], 'content': content,
            'destinip': destinip, 'destinport': destinport, 'send_time': send_time}

    data = {}

    head = changeBack(info.get('head'))
    # global result_list
    if head == command_head['send_sim_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'sim_' + hashlib.sha256(task_id).hexdigest()
        searResltList = info.get('searResltList')
        conten2bI = info.get('conten2bI')
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_sim_task'], 'task_id': task_id, 'searResltList': searResltList,
                'conten2bI': conten2bI, 'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_sim_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_search_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'search_' + hashlib.sha256(task_id).hexdigest()
        searchlist = info.get('searchlist')
        keywordslist = info.get('keywordsList')
        destinip = info.get('destinip')
        destinport = info.get('destinport')

        info = {'head': command_head['send_search_task'], 'task_id': task_id, 'searchlist': searchlist,
                'keywordsList': keywordslist, 'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_search_task']
        data['task_id'] = task_id

        # result_list[task_id] = ''
        # r = requests.post("http://119.3.50.104:9100/set_task", data=info)
    elif head == command_head['send_textparse_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'textparse_' + hashlib.sha256(task_id).hexdigest()
        content = info.get('content')
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_textparse_task'], 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_textparse_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
        # r = requests.post("http://119.3.50.104:9100/set_task", data=info)
    elif head == command_head['send_deal_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'deal_' + hashlib.sha256(task_id).hexdigest()
        sentList = info.get('sentList')
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_deal_task'], 'task_id': task_id, 'sentList': sentList,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_deal_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_image_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'image_' + hashlib.sha256(task_id).hexdigest()
        # image = info.get("uploadfile")
        image = info.get("uploadfile")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_image_task'], 'task_id': task_id,
                'destinip': destinip, 'destinport': destinport, 'uploadfile': image}

        data['head'] = command_head['response_image_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_linkin_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'linkin_' + hashlib.sha256(task_id).hexdigest()
        url = info.get("url")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_linkin_task'], 'task_id': task_id, 'url': url,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_linkin_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_whois_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'whois_' + hashlib.sha256(task_id).hexdigest()
        key = info.get("searchkey")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_whois_task'], 'task_id': task_id, 'searchkey': key,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_whois_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_checkmate_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'checkmate_' + hashlib.sha256(task_id).hexdigest()
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        city = info.get("city")
        location = info.get("location")
        sex = info.get("sex")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_checkmate_task'], 'task_id': task_id, 'first_name': first_name,
                'last_name': last_name, 'city': city, 'location': location, 'sex': sex,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_checkmate_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_domain_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'domain_' + hashlib.sha256(task_id).hexdigest()
        key = info.get("searchkey")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_domain_task'], 'task_id': task_id, 'searchkey': key,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_domain_task']
        data['task_id'] = task_id
    elif head == command_head['send_beenverified_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'beenver_' + hashlib.sha256(task_id).hexdigest()
        first_name = info.get("first_name")
        last_name = info.get("last_name")
        city = info.get("city")
        location = info.get("location")
        age = info.get("age")
        middle_name = info.get("middle_name")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_beenverified_task'], 'task_id': task_id, 'first_name': first_name,
                'last_name': last_name, 'city': city, 'location': location, 'age': age, 'middle_name': middle_name,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_beenverified_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_qqSpider_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'qqSpider_' + hashlib.sha256(task_id).hexdigest()
        qq = info.get("qq")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_qqSpider_task'], 'task_id': task_id, 'qq': qq,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_qqSpider_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_facebook_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'facebook_' + hashlib.sha256(task_id).hexdigest()
        name = info.get("name")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_facebook_task'], 'task_id': task_id, 'name': name,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_facebook_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_wechat_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'wechat_' + hashlib.sha256(task_id).hexdigest()
        number = info.get("number")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_wechat_task'], 'task_id': task_id, 'number': number,
                'destinip': destinip, 'destinport': destinport}
        data['head'] = command_head['response_wechat_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_search2_task']:  # 本地一个真实函数，如sendSimTask_test任务测试节点发送过来的参数
        task_id = str(create_task_id()).encode()  # 生成任务id
        task_id = 'search2_' + hashlib.sha256(task_id).hexdigest()  # 任务id前增加任务头
        search_word = info.get("search_word")  # 获取本地传过来的任务值
        destinip = info.get('destinip')  # 通知任务节点最重返回结果到的ip，现在暂时是固定在106上的
        destinport = info.get('destinport')
        total_page = info.get('total_page')
        info = {'head': change(command_head['send_search2_task']), 'task_id': task_id, 'search_word': search_word,
                'total_page': total_page,
                'destinip': destinip, 'destinport': destinport}  # 构造发给106的信息格式
        data['head'] = change(command_head['response_search2_task'])  # 构造返回给测试节点的消息内容，向测试节点表明，收到了任务
        data['task_id'] = task_id  # 向测试节点表明，收到了任务，以及对应的任务id，只有凭借这个task_id，索取任务执行结果
    elif head == command_head[
        'evtrelner_task_request']:  # 本地一个真实函数，如sendSimTask_test任务测试节点发送过来的参数，开始编写面向evtrelner的解析
        task_id = str(create_task_id()).encode()  # 生成任务id
        task_id = 'evtrelner_' + hashlib.sha256(task_id).hexdigest()  # 任务id前增加任务头　'evtrelner'
        # 进入参数解析，暂时保持与搜索任务的参数名一致，没有更改
        search_word = info.get("search_word")  # 获取本地传过来的任务值
        destinip = info.get('destinip')  # 通知任务节点最重返回结果到的ip，现在暂时是固定在106上的
        destinport = info.get('destinport')
        info = {'head': command_head['evtrelner_task_request'], 'task_id': task_id, 'search_word': search_word,
                'destinip': destinip, 'destinport': destinport}  # 构造发给106的信息格式
        data['head'] = command_head['response_evtrelner_task']  # 构造返回给测试节点的消息内容，向测试节点表明，收到了任务
        data['task_id'] = task_id  # 向测试节点表明，收到了任务，以及对应的任务id，只有凭借这个task_id，索取任务执行结果
        # result_list[task_id] = ''
    elif head == command_head['send_nlp_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'nlp_' + hashlib.sha256(task_id).hexdigest()
        allevtList = info.get("allevtList")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_nlp_task'], 'task_id': task_id, 'allevtList': allevtList,
                'destinip': destinip, 'destinport': destinport}
        print(allevtList)
        data['head'] = command_head['response_nlp_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_jinri_task_1']:
        task_id = str(create_task_id()).encode()
        task_id = 'jinri_1_' + hashlib.sha256(task_id).hexdigest()
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_jinri_task_1'], 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = command_head['response_jinri_task_1']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_jinri_task_2']:
        task_id = str(create_task_id()).encode()
        task_id = 'jinri_2_' + hashlib.sha256(task_id).hexdigest()
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_jinri_task_2'], 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = command_head['response_jinri_task_2']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_jinri_task_3']:
        task_id = str(create_task_id()).encode()
        task_id = 'jinri_3_' + hashlib.sha256(task_id).hexdigest()
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_jinri_task_3'], 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = command_head['response_jinri_task_3']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_ltp_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'ltp_' + hashlib.sha256(task_id).hexdigest()
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_ltp_task'], 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = command_head['response_ltp_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_stan_nlp_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'stan_nlp_' + hashlib.sha256(task_id).hexdigest()
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': command_head['send_stan_nlp_task'], 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = command_head['response_stan_nlp_task']
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_ln_anly_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'ln_anly_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_ln_anly_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_ln_anly_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_ie_anly_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'ie_anly_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_ie_anly_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_ie_anly_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_ie_anly_node2_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'ie_anly_node2_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_ie_anly_node2_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_ie_anly_node2_task'])
        data['task_id'] = task_id
    elif head == command_head['send_pl_anly_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'pl_anly_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_pl_anly_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_pl_anly_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_subj3_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'subj3_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_subj3_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_subj3_node_task'])
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_test_stage0_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'test_stage0_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_test_stage0_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_test_stage0_node_task'])
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_gen_ds_strcut_4_rel_9_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'gen_ds_strcut_4_rel_9_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_gen_ds_strcut_4_rel_9_node_task']), 'task_id': task_id,
                'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_gen_ds_strcut_4_rel_9_node_task'])
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_rel_extraction_0_13_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'rel_extraction_0_13_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_rel_extraction_0_13_node_task']), 'task_id': task_id,
                'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_rel_extraction_0_13_node_task'])
        data['task_id'] = task_id

    elif head == command_head['send_rel_get_revised_15_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'rel_get_revised_15_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_rel_get_revised_15_node_task']), 'task_id': task_id,
                'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_rel_get_revised_15_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_rel_get_revised_14_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'rel_get_revised_14_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_rel_get_revised_14_node_task']), 'task_id': task_id,
                'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_rel_get_revised_14_node_task'])
        data['task_id'] = task_id
        # result_list[task_id] = ''
    elif head == command_head['send_stage2_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'stage2_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_stage2_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_stage2_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_anly_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'anly_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        search_id = info.get("search_id")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_anly_node_task']), 'task_id': task_id, 'content': content,
                'search_id': search_id,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_anly_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_baidu_image_node_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'baidu_image_node_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_baidu_image_node_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_baidu_image_node_task'])
        data['task_id'] = task_id
    elif head == command_head['send_pre_wash_node22_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'pre_wash_node22_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_pre_wash_node22_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_pre_wash_node22_task'])
        data['task_id'] = task_id
    elif head == command_head['send_dianping_dish_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'dianping_dish_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_dianping_dish_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_dianping_dish_task'])
        data['task_id'] = task_id
    elif head == command_head['send_jinri_task_6']:
        task_id = str(create_task_id()).encode()
        task_id = 'jinri6_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_jinri_task_6']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_jinri_task_6'])
        data['task_id'] = task_id
    elif head == command_head['send_db_task']:
        task_id = str(create_task_id()).encode()
        task_id = 'db_' + hashlib.sha256(task_id).hexdigest()
        task_id = change(task_id)
        content = info.get("content")
        destinip = info.get('destinip')
        destinport = info.get('destinport')
        info = {'head': change(command_head['send_db_task']), 'task_id': task_id, 'content': content,
                'destinip': destinip, 'destinport': destinport}
        print(content)
        data['head'] = change(command_head['response_db_task'])
        data['task_id'] = task_id
    else:
        data['head'] = change(command_head['command_error'])
        info = []
        # return json.dumps(data, ensure_ascii=False)

    while True:
        try:
            # r = requests.post("http://119.3.50.104:9100/set_task", data=info)  # 向106发送任务
            r = requests.post("http://" + deliver_node_ip + ":" + deliver_node_port + "/set_task",
                              data=info)  # 向106发送任务
            break
        except:
            time.sleep(5)
    # r = requests.post("http://119.3.50.104:9100/set_task", data=info)# 向106发送任务
    response = json.loads(r.text)  # 106返回受到任务的确认



    # print('send set_task time' + str(time.asctime()))
    # r = s.post("http://" + command_node_ip + ":" + command_node_port + "/set_task", data=info)
    #
    #
    # response = json.loads(r.text)
    # print('finish set_task time' + str(time.asctime()))
    # print(response)


    elapsed = str((time.time() - start))
    print('send task time')
    print(elapsed)

    if response.get('head')== 'error':
        print()
    result = ''
    if response['head'] == command_head['response_db_task']:
        task_id = response['task_id']

        while True:
            try:
                start_take_db_result = time.time()
                info = {'head': command_head['take_db_result'], 'task_id': task_id}
                print('send take_final_result time' + str(time.asctime()))
                r = s.post("http://" + deliver_node_ip + ":" + deliver_node_port + "/take_final_result", data=info)
                response = json.loads(r.text)
                print('finish take_final_result time' + str(time.asctime()))
                elapsed = str((time.time() - start_take_db_result))
                print('take_final_result time')
                print(elapsed)

                if response['head'] == command_head['final_db_result']:
                    result = eval(response['result']['content'])
                    # print(result)
                    start = time.time()


                    print('send ack_get_result time' + str(time.asctime()))




                    r = s.post("http://" + deliver_node_ip + ":" + deliver_node_port + "/ack_get_result",
                               data=info)
                    response = json.loads(r.text)
                    # print(response)
                    if response == {'head': 'error'}:
                        print()
                    print('finish ack_get_result time' + str(time.asctime()))
                    elapsed = str((time.time() - start))
                    print('ack_get_result time')
                    print(elapsed)
                    break
            except Exception as e:
                print(e)
                pass
            # time.sleep(0.1)

        # elapsed = str((time.time() - start_ack))
        # print('take_final_result time + ack_time')
        # print(elapsed)
    else:
        print('指令出错')
    print()
    return result


class forThread(threading.Thread):
    global lock

    def __init__(self, function, content, thread_id_para):
        threading.Thread.__init__(self)
        self.content = content
        self.function = function
        self._thread_id_ = thread_id_para

    def run(self):
        # 打印时间 带 id
        # start = time.time()
        # print('run begin time ' + str(start))
        global mid_result_dict
        result = run_task({'function': self.function, 'parameter': [self.content]})

        if lock.acquire():
            mid_result_dict[self._thread_id_] = result  # get_ident()
            lock.release()
        # 打印时间 带 id
        # elapsed = str((time.time() - start))
        # print('run finish duration   ' + str(elapsed))


def call_function_node(function_name_, content_li):
    function_name = function_name_
    global mid_result_dict
    global result_list
    result_list = []
    mid_result_dict = {}

    start0 = time.time()
    thread_id_list = []
    thread_list = []
    count = 0
    # global _thread_id_
    _thread_id_ = 0
    # start = time.time()
    # print('start threading  ' + str(start))
    for i in content_li:
        thread1 = forThread(function_name, [i], _thread_id_)
        _thread_id_ += 1
        thread_list.append(thread1)
        thread1.start()
        thread_id_list.append(thread1._thread_id_)
        count += 1
        # print(count)
    # elapsed = str((time.time() - start))
    # print('thrading finish duration   ' + str(elapsed))
    # 打印时间
    # start = time.time()
    # print('start join  ' + str(start))
    for i in thread_list:
        i.join()
    # 打印时间
    # elapsed = str((time.time() - start))
    # print('join finish duration   ' + str(elapsed))
    # start = time.time()
    # print('start result    ' + str(start))
    for i in thread_id_list:
        result_list.append(mid_result_dict[i])
    # elapsed = str((time.time() - start))
    # print('result finish duration   ' + str(elapsed))

    elapsed = str((time.time() - start0))
    print(elapsed)
    # print(result_list)
    return result_list, elapsed





def search(key_word,suser_id):
    print('task in search is :' + str(key_word))
    # destinip = '106.15.177.58'
    destinip = deliver_node_ip
    destinport = deliver_node_port
    task_id = str(create_task_id()).encode()  # 生成任务id
    task_id = 'search2_' + hashlib.sha256(task_id).hexdigest()  # 任务id前增加任务头
    # total_page = result_total_page(key_word)# 调试关闭
    total_page = 1
    info = {'head': change(command_head['send_search2_task']),'task_id':task_id,'search_word':str(key_word),'total_page':total_page,'destinip':destinip,'destinport':destinport}
    if suser_id:
        info['suser_id'] = suser_id
    while True:
        try:
            r = requests.post("http://"+destinip+":"+destinport+"/set_task", data=info)  # 指令节点发送任务
            break
        except:
            pass
    response = json.loads(r.text)
    print(response)
    result = ''
    if changeBack(response['head']) == command_head['response_search2_task']:
        task_id = response['task_id']
        while True:
            try:
                # if time.time() - create_time >over_time:
                #     return 'over_time'
                info = {'head':change(command_head['take_search2_result']),'task_id':task_id}
                print('ask for result by command node')
                r = requests.post("http://"+destinip+":"+destinport+"/take_final_result",timeout=10, data=info)
                response = json.loads(r.text)
                print('result received by command node')
                if response['head']=='no result':
                    time.sleep(1)
                    continue

                if changeBack(response['head']) == command_head['final_search2_result']:  # 获取搜索结果
                    print('response[\'result\'] is:----'+response['result']+'--------')
                    result = str(ListSet(eval(response['result'].replace('\ufeff',''))).content)# 去重
                    print('effective result received !!!!!!!!!!!!!')
                    return result
            except Exception as e:
                print(e)
                pass
            time.sleep(10)
    # time.sleep(60)
    # deal(key_word, key_sentece, more_sentence, path) # 对搜索结果进行处理





def search_inthread(key_word,suser_id=None):
    class search_Thread(threading.Thread):
        def __init__(self, key_word):
            threading.Thread.__init__(self)
            self.key_word = key_word
            self.suser_id = suser_id

        def run(self):
            result = search(self.key_word,self.suser_id)
            print(result)
            file_name = re.sub('[\/:*?"<>|]','-',self.key_word)
            dir_path = 'store/baiduSearch'
            if not os.path.exists(dir_path):
                os.makedirs(dir_path)
            with open(f'store/baiduSearch/{file_name}.json','w',encoding='utf8') as f:
                f.write(json.dumps(result,ensure_ascii=False))
    thread1 = search_Thread(key_word)
    thread1.start()

if __name__ == '__main__':
    # for i in range(1000):
    #     print('index:'+str(i))
    #     data = [{"email": str(i+11000)+'@qq.com'},{'domain':0},{'can_event_review':0}]
    #
    #     table_name = "ts_user"
    #     data1 = {
    #         "table": table_name,
    #         "data": str(data)
    #     }
    #     result = call_function_node('db_insert', [data1])

    data1 = {
        "field": "*",
        "table": "ts_user",
        "order": 'uid desc',
        "where": 'null',
        "limit": '0,20'
    }


    result = call_function_node('db_find_all', [data1])
    print(result)
