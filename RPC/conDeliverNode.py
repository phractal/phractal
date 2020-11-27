
import requests
import json
deliver_node_ip = '192.168.3.32'
deliver_node_port = '9100'




def registerAccount(user):
    try:
        response = requests.post(f"http://{deliver_node_ip}:{deliver_node_port}/user_register", data=user)
        response = json.loads(response.text)
        return response.get('global_id',None)
    except Exception as e:
        print(e)


def registerNode(node_id,user_id):
    print(f'node_id--------{node_id}--user_id---------{user_id}')









