import json

import requests
from django.http import JsonResponse
from django.shortcuts import render, redirect
from rest_framework.response import Response
# Create your views here.
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.utils import jwt_decode_handler

from accounts.models import UserProfile
from tasks.models import SearchHistory


class IndexView(APIView):
    def get(self, request):
        return render(request, "index.html")


class LoginView(APIView):
    def get(self, request):
        return render(request, 'login.html')


class RegisterView(APIView):
    def get(self, request):
        return render(request, 'register.html')


class TaskpubView(APIView):
    def get(self, request):
        return render(request, 'task_pub.html')

class TasklistView(APIView):
    def get(self, request):
        return render(request, 'tasklist.html')

class MyorderView(APIView):
    def get(self, request):
        return render(request, 'myorder.html')

class PersonaldataView(APIView):
    def get(self, request):
        return render(request, 'personaldata.html')

class MynodeView(APIView):
    def get(self, request):
        return render(request, 'mynode.html')

class ChangepasswdView(APIView):
    def get(self, request):
        return render(request, 'changepasswd.html')

class WalletView(APIView):
    def get(self, request):
        return render(request, 'wallet.html')

class StatisticsView(APIView):
    def get(self, request):
        return render(request, 'statistic.html')

class DownloadView(APIView):
    def get(self, request):
        return render(request, 'download_node.html')

class BlockChainView(APIView):
    def get(self, request):
        return render(request, 'blockchain.html')

class ParticularView(APIView):
    def get(self, request):

        return render(request, 'particular1.html')

class MapView(APIView):
    def get(self,request):
        server_ip_port = '127.0.0.1:9112'
        s = requests.session()
        s.keep_alive = False
        r = s.get("http://" + server_ip_port + "/map?is_app=1")# 发送搜索结果
        print()
        return Response(json.loads(r.text))


class TypeNodeView(APIView):
    def post(self,request):
        server_ip_port = '127.0.0.1:9112'
        type = request.data.get('type')
        s = requests.session()
        s.keep_alive = False
        data = {'N_type':type}
        r = s.post("http://" + server_ip_port + "/task/typetonode/", data=data)
        response = json.loads(r.text)
        print()
        return Response(response)

class SearchNodeView(APIView):
    def post(self,request):
        server_ip_port = '127.0.0.1:9112'
        type = request.data.get('data')
        s = requests.session()
        s.keep_alive = False
        data = {'N_name':type}
        r = s.post("http://" + server_ip_port + "/task/nametoallnode/", data=data)
        response = json.loads(r.text)
        print()
        return Response(response)

class SearchHistoryView(APIView):

    def get(self,request):
        token = request.query_params.get('token')
        is_app = request.query_params.get('is_app')

        print(token)
        # 顶一个空数组来接收token解析后的值
        toke_user = jwt_decode_handler(token)
        user_id = toke_user.get('user_id')
        historys = SearchHistory.objects.filter(user_id=user_id).all()
        history_list = set()
        for i in historys:
            history_list.add(i.search_key)
        print('111111',toke_user)
        if is_app==1 or is_app=='1':
            return Response({'history_list':list(history_list)})
        return render(request,'searchHistory.html',{'history_list':list(history_list)})


class SearchResultView(APIView):
    def get(self,request):
        search_key = request.query_params.get('key')
        page = request.query_params.get('page')
        token = request.query_params.get('token')
        is_app = request.query_params.get('is_app')
        print(token)
        # key = '杨子江'
        s = requests.session()
        s.keep_alive = False
        server_ip_port = '127.0.0.1:9112'
        if page:
            r = s.get("http://" + server_ip_port + "/client_search/"+search_key+"/?page="+str(page))  # 发送搜索结果
        else:
            r = s.get("http://" + server_ip_port + "/client_search/" + search_key + "/")
        response = json.loads(r.text)
        print(response)
        toke_user = jwt_decode_handler(token)
        user_id = toke_user.get('user_id')
        historys = SearchHistory.objects.filter(user_id=user_id).all()
        history_list = []
        for i in historys:
            history_list.append(i.search_key)
        response['history_list'] = history_list
        user = UserProfile.objects.filter(id=user_id).first()
        if search_key not in history_list:
            sh = SearchHistory(user=user,search_key=search_key)
            sh.save()
        if response.get('has_result')==False:
            if is_app == 1 or is_app == '1':
                return Response(response)
            return render(request, 'searchHistory.html', response)
        else:
            words_intersection = {}
            words_intersection_len = {}
            for key,value in eval(response['words_intersection']).items():
                new_value = {}
                new_value_len = {}
                already_node = set()
                already_node.add(search_key)  # 将搜索关键词从already_node中去除，不然图谱显示时会出错。
                for key2,value2 in value.items():
                    value2 = list(set(value2))
                    value2_dict = {}
                    for i in value2:
                        i = i.strip()
                        if i and not i in already_node:
                            value2_dict[i] = i
                            already_node.add(i)
                    if value2_dict and not key2 == 'OTHERS':  # 屏蔽others标签
                        new_value[key2] = value2_dict
                    if key2 == 'LOCATION':
                        new_value_len['LOCATION_LEN'] = [' ' for i in range(len(value2_dict))]  # 根据标签数量创建其连线
                    elif key2 == 'ORGANIZATION':
                        new_value_len['ORGANIZATION_LEN'] = [' ' for i in range(len(value2_dict))]
                    # elif key2 == 'OTHERS':
                    #     new_value_len['OTHERS_LEN'] = [' ' for i in range(len(value2_dict))]
                    elif key2 == 'PERSON':
                        new_value_len['PERSON_LEN'] = [' ' for i in range(len(value2_dict))]
                    elif key2 == 'ALL':
                        new_value_len['ALL_LEN'] = [' ' for i in range(len(value2_dict))]
                words_intersection[key] = new_value
                words_intersection_len[key] = new_value_len
            response['words_intersection'] = words_intersection
            response['words_intersection_len'] = words_intersection_len
            response['has_result'] = True
            if is_app == 1 or is_app == '1':
                return Response(response)
            return render(request,'search.html',response)

    def post(self,request):
        print(request.data)
        task_id = request.data.get('task_id')
        words_intersection = request.data.get('words_intersection')
        words_intersection_len = request.data.get('words_intersection_len')
        key_word = request.data.get('key_word')
        s = requests.session()
        s.keep_alive = False
        server_ip_port = '127.0.0.1:9112'
        data = {}
        data['selected_list'] = request.data.get('selected_list')
        data['task_id'] = task_id
        data['key_word'] = key_word
        data['words_intersection'] = words_intersection
        data['words_intersection_len'] = words_intersection_len
        try:
            r = s.post("http://" + server_ip_port + "/client_search2/" + key_word + "/page=1",data=data)
            response = json.loads(r.text)
            # response = {}
            response['task_id'] = task_id
            response['current_page'] = 1
            # response['words_intersection'] = words_intersection
            # response['words_intersection_len'] = words_intersection_len
            return render(request, 'search_result.html', response)
            # return JsonResponse(response)
        except:
            print(server_ip_port)
            print(key_word)
            print(data)
            return render(request, 'searchHistory.html', {'has_result':False})


class SearchResultSelectedView(APIView):
    def post(self,request):
        print(request.data)
        task_id = request.data.get('task_id')
        page = request.data.get('page')
        words_intersection = request.data.get('words_intersection')
        words_intersection_len = request.data.get('words_intersection_len')
        key_word = request.data.get('key_word')
        s = requests.session()
        s.keep_alive = False
        server_ip_port = '127.0.0.1:9112'
        data = {}
        data['selected_list'] = request.data.get('selected_list')
        data['task_id'] = task_id
        data['key_word'] = key_word
        data['words_intersection'] = words_intersection
        data['words_intersection_len'] = words_intersection_len
        try:
            r = s.post("http://" + server_ip_port + "/client_search2/" + key_word + "/page="+str(page), data=data)
            response = json.loads(r.text)
            # response = {}
            response['task_id'] = task_id
            # response['current_page'] = response['current_page']
            # response['words_intersection'] = words_intersection
            # response['words_intersection_len'] = words_intersection_len
            return render(request, 'search_result.html', response)
            # return JsonResponse(response)
        except:
            print(server_ip_port)
            print(key_word)
            print(data)

class SearchResultSelectedDetailView(APIView):
    def post(self,request):
        print(request.data)
        task_id = request.data.get('task_id')
        page = request.data.get('page')
        words_intersection = request.data.get('words_intersection')
        words_intersection_len = request.data.get('words_intersection_len')
        key_word = request.data.get('key_word')
        s = requests.session()
        s.keep_alive = False
        server_ip_port = '127.0.0.1:9112'
        data = {}
        data['detail_selected'] = eval(request.data.get('detail_selected'))
        # data['detail_selected'] = ['345&354&369&388&398&403&421&435&437&446&448&481&491','康奈尔大学']
        data['task_id'] = task_id
        data['key_word'] = key_word
        data['words_intersection'] = words_intersection
        data['words_intersection_len'] = words_intersection_len
        while True:
            try:
                r = s.get("http://" + server_ip_port + "/client_search2_tag/" + key_word + "/"+data['detail_selected'][1]+"/"+data['detail_selected'][0]+"page="+str(page), data=data)
                response = json.loads(r.text)
                # response = {}
                response['task_id'] = task_id
                # response['current_page'] = 1
                # response['words_intersection'] = words_intersection
                # response['words_intersection_len'] = words_intersection_len
                return render(request, 'search_result.html', response)
            except:
                print(server_ip_port)
                print(key_word)
                print(data)


class ChangepassworddView(APIView):
    def post(self, request):
        print(request.data)
        task_id = request.data.get('task_id')
        page = request.data.get('page')