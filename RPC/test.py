# coding:utf-8
# _author_:Junjie
# date:2019/10/21
import json

import requests

def change_status(node_status,node_type,num=0): # node_status: exit 或者 open
    deliver_node_ip = '192.168.3.32'
    deliver_node_port = '8000'
    r = requests.post("http://" + deliver_node_ip + ":" + deliver_node_port + "/node_status",
                      data={"node_status": node_status, "node_type": node_type,"number":num})
    print()
    response = json.loads(r.text)
    print(response)



def get_ststua():
    r = requests.post("http://119.3.50.104:9100/check_all_node_status/")
    response = json.loads(r.text)
    print(response)

change_status("open","bbbb",5)
# change_status("exit","aaaa")
# get_ststua()