import ctypes
import datetime
import os
import platform
from pprint import pprint

import psutil
import zipfile

import pythoncom
import requests

from django.core.paginator import Paginator

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from nodes.models import Node, TaskNode, CompressNode, Monitor_node
from rest_framework.permissions import IsAuthenticated
from nodes.serializers import NodeSerializers, TaskNodeSerializers

from wallets.models import MyAccount
from django.contrib.auth import get_user_model
from RPC import conDeliverNode
import download_tool


class NodeViewSet(mixins.ListModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.CreateModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    serializer_class = NodeSerializers

    def get_queryset(self):
        queryset = Node.objects.all()
        if self.request.user.is_active:
            now = datetime.datetime.now()
            # start = now - datetime.timedelta(seconds=30)
            # queryset = queryset.filter(user=self.request.user, update_time__gt=start)
            queryset = queryset.filter(user=self.request.user)
        # for element in queryset:
        return queryset


class HeartViewSet(APIView):
    # serializer_class = NodeSerializers
    # queryset = Node.objects.all().order_by("-id")

    # permission_classes = (IsAuthenticated,)

    # @action(methods=['post'], detail=True)
    def post(self, request):
        node_id = int(request.data.get('node_id'))
        user_id = int(request.data.get('user_id'))
        name = request.data.get('name')
        category = request.data.get('category')
        path = request.data.get('path')

        path = 'node_file' + path.split('node_file')[-1] + '\\node.exe'
        print(path)
        ip = request.stream.META.get("REMOTE_ADDR")
        node = Node.objects.filter(node_id=node_id)
        if node.exists():
            node = node.first()
            node.update_time = datetime.datetime.now()
            node.state = 'open'
            node.save()
        else:
            # node_id 与user绑定
            conDeliverNode.registerNode(node_id, user_id)
            Node.objects.create(node_id=node_id, name=name, category=category, user_id=user_id, ip=ip, path=path,
                                state='open')
        return Response({'state': 'ok'}, status=status.HTTP_201_CREATED)


# 节点 开启 关闭 删除操作
class NodeOpViewSet(APIView):
    def post(self, request):
        data = request.data.get('data')
        operate = data.get('operate')
        node_s = data.get('nodes')
        # if node_s:
        #     node_s = eval(node_s)
        if operate == 'open':
            for node in node_s:
                node_id = node.get('node_id')
                node = Node.objects.filter(node_id=node_id)
                if node.exists():
                    node = node.first()
                    path = node.path
                    reply = download_tool.open_node(path, request.user.id)
                    node.state = 'open'
                    node.save()
            return Response({'state': 'ok'}, status=status.HTTP_200_OK)
        elif operate == 'close':
            for node in node_s:
                node_id = node.get('node_id')
                node = Node.objects.filter(node_id=node_id)
                if node.exists():
                    download_tool.close_node(node.first().path)
                    node_ = node.first()
                    node_.unit_price = 2
                    node_.state = 'close'
                    node_.save()
            return Response({'state': 'ok'}, status=status.HTTP_200_OK)

        elif operate == 'delete':
            for node in node_s:
                node_id = node.get('node_id')
                node = Node.objects.filter(node_id=node_id)
                if node.exists():
                    node = node.first()
                    path = node.path
                    try:

                        download_tool.delete_node(path)
                    except Exception as e:
                        print(e)
                    node.delete()

            return Response({'state': 'ok'}, status=status.HTTP_200_OK)

        return Response({'state': 'err'}, status=status.HTTP_200_OK)


class NodeDownLoadViewSet(APIView):
    def post(self, request):
        url = request.data.get('url')
        try:
            download_tool.download(url)
            return Response({'state': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'state': 'err'}, status=status.HTTP_200_OK)

    def get(self, request):
        url = request.query_params.dict()["url"]
        try:
            status = download_tool.get_download_state(url)
            return Response({'status': status})
        except:
            return Response({'status': 'err'})


class NodeCreateViewSet(APIView):
    def post(self, request):
        node_type = request.data.get('node_type')
        num = int(request.data.get('num'))
        # user_id = request.user.user_id
        user_id = 31
        try:
            download_tool.unzip(f'./node_store/{node_type}.zip', user_id, num=num)

            return Response({'state': 'ok'}, status=status.HTTP_200_OK)
        except:
            return Response({'state': 'err'}, status=status.HTTP_200_OK)


class NodeTypeViewSet(APIView):
    def get(self, request):
        return Response(download_tool.get_node_type(), status=status.HTTP_200_OK)


class NodeNumManageViewSet(APIView):
    def get(self, request):
        data = {'total': 20, 'rows':
            [

                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': '语义分析', 'num': 2598, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': '语义分析', 'num': 2598, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': '语义分析', 'num': 2598, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': '语义分析', 'num': 2598, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},
                {'node_type': 'google搜索', 'num': 3456, 'occ_space': '0.5G', 'free_space': '156G'},

            ]
                }
        return Response(data, status=status.HTTP_200_OK)


class NodeRunManageViewSet(APIView):
    def get(self, request):
        nodes = Node.objects.all()
        node_type_list = []
        data_list = []
        for node in nodes:
            if node.category not in node_type_list:
                node_type_list.append(node.category)
        for node_category in node_type_list:
            nodes_ = Node.objects.filter(category=node_category)
            nodes_run = nodes_.filter(state='open')
            data_dict = {
                'node_type': node_category,
                'node_num': nodes_.count(),
                'run_num': nodes_run.count()
            }
            data_list.append(data_dict)
        data = {
            'total': len(data_list),
            'rows': data_list
        }

        return Response(data, status=status.HTTP_200_OK)

    def put(self, request):
        action = request.data.get('action')
        node_type = request.data.get('node_type')
        num = request.data.get('num')
        user_id = request.user.id
        if action == 'open':
            node_closed = Node.objects.filter(state='close')
            if int(num) <= node_closed.count():
                compressnode = CompressNode.objects.get(node_type=node_type)
                for i in range(int(num)):
                    download_tool.open_node(node_closed[i].path, user_id)
                    node_closed[i].update(state='open')
                    # node_closed[i].save()
                compressnode.node_num += int(num)
                compressnode.save()
                data = {
                    'state': 0,
                    'msg': '开启' + num + '个节点'
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'state': 1,
                    'msg': '节点数量错误'
                }
                return Response(data, status=status.HTTP_200_OK)
        elif action == 'close':
            node_opend = Node.objects.filter(state='close')
            if int(num) <= node_opend.count():
                compressnode = CompressNode.objects.get(node_type=node_type)
                for i in range(int(num)):
                    download_tool.close_node(node_opend[i].path)
                    node_opend[i].state = 'close'
                    node_opend[i].save()
                compressnode.node_num -= int(num)
                compressnode.save()
                data = {
                    'msg': '关闭' + num + '个节点'
                }
                return Response(data, status=status.HTTP_200_OK)
            else:
                data = {
                    'msg': '节点数量错误'
                }
                return Response(data, status=status.HTTP_200_OK)


class TaskNodeViewsSet(mixins.CreateModelMixin,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       viewsets.GenericViewSet,
                       mixins.ListModelMixin):
    serializer_class = TaskNodeSerializers

    def get_queryset(self):
        queryset = TaskNode.objects.all()
        if self.request.user.is_active:
            queryset = queryset.filter(node__user=self.request.user)
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        need_plus_revenue = serializer.data.get("this_time_revenue")
        node = Node.objects.get(id=int(serializer.data.get("node")))
        myaccount = MyAccount.objects.filter(user=node.user).first()
        myaccount.balance = float(myaccount.balance) + need_plus_revenue
        myaccount.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class Node_Management_List(APIView):

    def check_memory(self, path):
        i = 0
        for dirpath, dirname, filename in os.walk(path):
            for ii in filename:
                i += os.path.getsize(os.path.join(dirpath, ii))
            memory = i / 1024. / 1024.
            return float(format(memory, '.5f'))

    def get_free_space_mb(self, folder):
        """ Return folder/drive free space (in bytes)
        """
        if platform.system() == 'Windows':
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(ctypes.c_wchar_p(folder), None, None, ctypes.pointer(free_bytes))
            return free_bytes.value / 1024 / 1024 / 1024.
        else:
            st = os.statvfs(folder)
            return st.f_bavail * st.f_frsize / 1024 / 1024 / 1024.

    def get(self, request):
        compressnodes = CompressNode.objects.all()
        # for compressnode in compressnodes
        nodes = Node.objects.all()
        node_type_list = []
        data_list = []

        for node in nodes:
            if node.category not in node_type_list:
                node_type_list.append(node.category)
        for node_category in node_type_list:
            occupancy_space = 0
            surplus_space = 0
            nodes_ = Node.objects.filter(category=node_category)
            count = nodes_.count()
            for node_ in nodes_:
                path = node_.path.replace('\\node.exe', '')
                path_ = node_.path.split('\\')[0]
                occupancy_space += self.check_memory(path) if self.check_memory(path) else 0
                surplus_space = self.get_free_space_mb(path_)
            if occupancy_space > 1024:
                occupancy_space_ = format(occupancy_space / 1024, '.5f') + 'GB'
            else:
                occupancy_space_ = format(occupancy_space, '.5f') + 'MB'
            if surplus_space < 0:
                surplus_space_ = format(surplus_space * 1024, ',5f') + 'GB'
            else:
                surplus_space_ = format(surplus_space, '.5f') + "GB"
            node_dict = {
                'node_type': node_category,
                'num': count,
                'occ_space': occupancy_space_,
                'free_space': surplus_space_,
            }
            data_list.append(node_dict)
        data = {
            'total': len(data_list),
            'rows': data_list
        }
        return Response(data, status=status.HTTP_200_OK)

    def post(self, request):
        # todo: 添加节点
        num = int(request.data.get('num'))
        node_type = request.data.get('node_type')
        user_id = request.user.id
        free_space = request.data.get('free_space')
        compressnode = CompressNode.objects.get(node_type=node_type)
        node = Node.objects.filter(category=node_type).first()
        z = zipfile.ZipFile(compressnode.node_path, "r")
        size = 0
        if free_space[-2:] == 'MB':
            for filename in z.namelist():
                print(filename)
                bytes = z.read(filename)
                size += len(bytes) / 1024 / 1024
        if free_space[-2:] == 'GB':
            for filename in z.namelist():
                print(filename)
                bytes = z.read(filename)
                size += len(bytes) / 1024 / 1024 / 1014
        size = float(format(size, '.5f'))
        size = size * int(num)
        if size < float(free_space[:-2]):
            for i in range(num):
                path = download_tool.unzip(zippath=compressnode.node_path, user_id=user_id)
            compressnode.node_num += int(num)
            compressnode.save()
            data = {
                'state': 0,
                'msg': f'{num}个节点添加成功'
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            data = {
                'state': 1,
                'msg': '磁盘空间不足，请修改增加节点数量'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)

    def delete(self, request):
        # todo: 删除节点
        node_type = request.data.get('node_type')
        user_id = request.user.id
        num = request.data.get('num')
        compressnode = CompressNode.objects.get(node_type=node_type)
        node = Node.objects.filter(category=node_type).order_by('-update_time')
        if int(num) <= compressnode.node_num:
            for i in range(int(num)):
                download_tool.delete_node(node[i].path)
                # os.remove(node[i].path)
                # os.rmdir(node[i].path.replace('\\node.exe',''))
                node[i].delete()
            compressnode.node_num -= int(num)
            compressnode.save()
            data = {
                'state': 0,
                'msg': f'{num}个节点删除完成'
            }
            return Response(data, status=status.HTTP_200_OK)
        else:
            data = {
                'state': 1,
                'msg': '节点数量错误'
            }
            return Response(data, status=status.HTTP_204_NO_CONTENT)


class Open_node(APIView):
    def post(self, request):
        pass


class NodeStatistic(APIView):
    def get(self, request):
        node_money = {
            "rel_get_revised14_node": 5,
            "test": 9,
            "ie_anly_node": 9,
            "test1": 7,
            "rel_get_revised15_node": 6,
            "baidu_image_node": 6,
            "googleSearch": 8,
            "rel_get_revised_node": 7,
            "db": 10,
            "ie": 9,
            "jinri_6": 7,
            "subj3_node": 10,
            "google_translate": 7,
            "ie_anly_node2": 10,
            "pre_wash_node22": 7,
            "test_stage0_node": 7,
            "pl_anly_node": 8,
            "stage0_node": 7,
            "stage2_node": 6,
            "anly_node": 6,
            "dazhongdianpin": 6,
            "pl": 9,
            "baiduSearch": 6,
            "dianping_dish": 7,
            "ln_anly_node": 7,
            "gen_ds_strcut_node": 10,
            "rel_extraction_node": 5,
            "ln": 5
        }
        return_list = []
        return_data = {}
        offset = request.query_params.get('offset')
        limit = request.query_params.get('limit')
        # user_id=31
        if offset and limit:
            if offset == '0':
                page = 1
            else:
                page = int(int(offset) / int(limit)) + 1
        else:
            page = 1
        data = {
            "page": page,
            "page_num": limit
        }
        content = requests.post('http://www.heiyunworld.com:90/task/allnode/', data=data)
        # content = requests.post('http://127.0.0.1:8000/task/allnode/', data=data)
        if content:
            node = eval(content.content.decode('utf-8'))
            return_data['total'] = node['num_pages']
            for n in node['nodes']:
                if n['N_type'] == '':
                    pass
                else:
                    if node_money['{}'.format(n['N_type'])] * n['N_complete'] > 0:
                        money = node_money['{}'.format(n['N_type'])] * n['N_complete']
                        n['money'] = '+' + str(money) + '元'
                    else:
                        pass
                return_list.append(n)
        return_data['rows'] = return_list
        print(return_data)
        print('这里是全局')
        return Response(return_data)


class IndividualStatistic(APIView):
    def get(self, request):
        node_money = {
            "rel_get_revised14_node": 5,
            "test": 9,
            "ie_anly_node": 9,
            "test1": 7,
            "rel_get_revised15_node": 6,
            "baidu_image_node": 6,
            "googleSearch": 8,
            "rel_get_revised_node": 7,
            "db": 10,
            "ie": 9,
            "jinri_6": 7,
            "subj3_node": 10,
            "google_translate": 7,
            "ie_anly_node2": 10,
            "pre_wash_node22": 7,
            "test_stage0_node": 7,
            "pl_anly_node": 8,
            "stage0_node": 7,
            "stage2_node": 6,
            "anly_node": 6,
            "dazhongdianpin": 6,
            "pl": 9,
            "baiduSearch": 6,
            "dianping_dish": 7,
            "ln_anly_node": 7,
            "gen_ds_strcut_node": 10,
            "rel_extraction_node": 5,
            "ln": 5
        }
        return_list = []
        return_data = {}
        offset = request.query_params.get('offset')
        limit = request.query_params.get('limit')
        if offset and limit:
            if offset == '0':
                page = 1
            else:
                page = int(int(offset) / int(limit)) + 1
        else:
            page = 1
        user_id = request.query_params.dict()["uid"]

        # user_id = 32
        if user_id:
            local_node_id_list = []
            local_node = Paginator(Node.objects.filter(user_id=user_id).values('node_id'), int(limit))
            posts = local_node.page(number=page)  # 这个num就是实现当前第几页
            return_data['total'] = local_node.count  # 返回总页数
            for local in posts:
                local_node_id_list.append(local['node_id'])
            data = {
                "id": str(local_node_id_list)
            }
            content = requests.post('http://www.heiyunworld.com:90/task/get_node_info_by_id/', data=data)
            # content = requests.post('http://127.0.0.1:8000/task/get_node_info_by_id/', data=data)
            if content:
                node = eval(content.content.decode('utf-8'))
                for n in node:
                    if n['N_type'] == '':
                        pass
                    else:
                        if node_money['{}'.format(n['N_type'])] * n['N_complete'] > 0:
                            money = node_money['{}'.format(n['N_type'])] * n['N_complete']
                            n['money'] = '+' + str(money) + '元'
                        else:
                            pass
                    return_list.append(n)
        return_data['rows'] = return_list
        print('这里是本地')
        print(return_data)
        return Response(return_data)


class AllDownloadNode(APIView):
    def get(self, request):
        nodes = Node.objects.all()
        print('1111111111111')
        s_nodes = NodeSerializers(nodes, many=True).data
        s_list = []
        for s in s_nodes:
            d = {}
            d["category"] = s["category"]
            d["hardware"] = "CPU:3.0GHz;内存:4GB"
            d["size"] = "0.5G"
            d["unit_price"] = s["unit_price"]
            d["require_percent"] = "355/5000"
            d["md5"] = "SADCDE4521"
            d["user"] = s["user"]["username"]
            d["create_time"] = s["create_time"]
            d["security_authentication"] = "ISO认证"
            d["system"] = "Windows 2007"
            d["url"] = "http://119.3.50.104:10001/file/1.png"
            s_list.append(d)

        print(s_list)
        return Response(s_list)


class AlreadyDownloadNode(APIView):
    def get(self, request):
        id = request.query_params.dict()["uid"]
        nodes = Node.objects.filter(user_id=id)
        print('2222222222222')
        s_nodes = NodeSerializers(nodes, many=True).data
        s_list = []
        for s in s_nodes:
            d = {}
            d["category"] = s["category"]
            d["hardware"] = "CPU:3.0GHz;内存:4GB"
            d["size"] = "0.5G"
            d["unit_price"] = s["unit_price"]
            d["require_percent"] = "355/5000"
            d["md5"] = "SADCDE4521"
            d["user"] = s["user"]["username"]
            d["create_time"] = s["create_time"]
            d["security_authentication"] = "ISO认证"
            d["system"] = "Windows 2007"
            s_list.append(d)

        print(s_list)
        return Response(s_list)






# 节点检索及统计查询(不用了)
class Statistics(APIView):
    def get(self, request):
        node_money = {
            "rel_get_revised14_node": 5,
            "test": 9,
            "ie_anly_node": 9,
            "test1": 7,
            "rel_get_revised15_node": 6,
            "baidu_image_node": 6,
            "googleSearch": 8,
            "rel_get_revised_node": 7,
            "db": 10,
            "ie": 9,
            "jinri_6": 7,
            "subj3_node": 10,
            "google_translate": 7,
            "ie_anly_node2": 10,
            "pre_wash_node22": 7,
            "test_stage0_node": 7,
            "pl_anly_node": 8,
            "stage0_node": 7,
            "stage2_node": 6,
            "anly_node": 6,
            "dazhongdianpin": 6,
            "pl": 9,
            "baiduSearch": 6,
            "dianping_dish": 7,
            "ln_anly_node": 7,
            "gen_ds_strcut_node": 10,
            "rel_extraction_node": 5,
            "ln": 5
        }
        return_list = []
        user_id = request.query_params.dict()["uid"]
        # user_id = 32
        if user_id:
            local_node_id_list = []
            local_node = Node.objects.filter(user_id=user_id).values('node_id')
            for local in local_node:
                local_node_id_list.append(local['node_id'])
            data = {
                "id": str(local_node_id_list)
            }
            content = requests.post('http://www.heiyunworld.com:90/task/get_node_info_by_id/', data=data)
            # content = requests.post('http://127.0.0.1:8000/task/get_node_info_by_id/', data=data)
            if content:
                node = eval(content.content.decode('utf-8'))
                for n in node:
                    n['money'] = node_money['{}'.format(n['N_type'])] * n['N_complete']
                    return_list.append(n)
        return Response(return_list)





class Set_cpu_or_mem(APIView):
    def get(self,request):
        monitor=Monitor_node.objects.first()
        data = {
            'status':200,
            'cpu':monitor.max_cpu,
            'mem':monitor.max_memory
        }
        return Response(data)
    def post(self,request):
        num = request.data.get('num')
        monitor=Monitor_node.objects.first()
        if request.data.get('action') == 'cpu':
            monitor.max_cpu = num
            monitor.save()
        if request.data.get('action') == 'mem':
            monitor.max_memory=num
            monitor.save()
        data = {
            'status':200
        }
        return Response(data)

def selecr_monitor():
    if not Monitor_node.objects.exists():
        Monitor_node.objects.create(
            max_cpu=35,
            max_memory=35
        )
selecr_monitor()




##通过thread 实现django中
import threading
import time
#查看node.exe所占cpu
class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        pythoncom.CoInitialize()
        while True:
            import wmi
            wmiInterface = wmi.WMI()
            running_node = download_tool.running_node
            cpu_percent = 0
            mem_percent = 0
            can_use_cpu = Monitor_node.objects.first().max_cpu
            can_use_memory =Monitor_node.objects.first().max_memory
            node_list = wmiInterface.Win32_Process(name="node.exe")
            cpu_dict = {}
            mem_dict = {}
            # wmiInterface.Win32_PhysicalMemory()
            if node_list:
                for process in node_list:
                    pid = process.ProcessID
                    p = psutil.Process(pid)
                    cpu_dict[pid]=p.cpu_percent()
                    mem_dict[pid] = p.memory_percent()
                    cpu_percent += p.cpu_percent()###cpu
                    mem_percent += p.memory_percent()###内存
                    # print(cpu_percent,mem_percent)
                # pprint(cpu_dict)
                # pprint(mem_dict)
                if cpu_percent>can_use_cpu or  mem_percent>can_use_memory:
                    max_cpu_pid = list(cpu_dict.keys())[list(cpu_dict.values()).index(max(cpu_dict.values()))]
                    for node_path in running_node:
                        node_pid = running_node[node_path]
                        if node_pid == max_cpu_pid:
                            import subprocess
                            print(running_node[node_path])
                            subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i" % max_cpu_pid, shell=True)
                            node = Node.objects.get(path=node_path)
                            node.state='close'
                            node.save()
                            time.sleep(1)
                        else:
                            continue
                if mem_percent>can_use_memory:
                    max_mem_pid = list(mem_dict.keys())[list(mem_dict.values()).index(max(mem_dict.values()))]
                    for node_path in running_node:
                        node_pid = running_node[node_path]
                        if node_pid == max_mem_pid:
                            import subprocess
                            print(running_node[node_path])
                            subprocess.Popen("cmd.exe /k taskkill /F /T /PID %i" % max_mem_pid, shell=True)
                            node = Node.objects.get(path=node_path)
                            node.state='close'
                            node.save()
                            time.sleep(1)
                        else:
                            continue
        pythoncom.CoUninitialize()


t = MyThread()
t.start()

