import datetime
import threading
import time

import pymysql
import hashlib
import uuid
import random

mysql_conn = pymysql.connect(user='root',  # 用户名
                           password='123456',  # 密码
                           db='kanban',  # 数据库名
                           host='192.168.3.32',  # 地址
                           port=3306,
                           cursorclass=pymysql.cursors.DictCursor,
                           charset='utf8')


def hash(nonce):

    message = hashlib.sha256()
    message.update(str(nonce).encode('utf-8'))

    return message.hexdigest()


def insert_into_blocktask(t):
    sql = """insert into tasks_blocktask(identify, status, block_belong, create_time, receiver, poster,
    transaction1, task_num, task_price, op_num, input_data)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

        """
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql, t)  # 执行数据插入
        mysql_conn.commit()  # 提交记录
    except Exception as e:
        print(e)
        mysql_conn.rollback()

def insert_into_block(t):
    sql = """insert into tasks_block(block_out_time, content_task_num, hash, f_hash, miner, size,
        op_num, reward, additional_data, block_depth)VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)

            """
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql, t)  # 执行数据插入
        mysql_conn.commit()  # 提交记录
    except Exception as e:
        print(e)
        mysql_conn.rollback()








def insert_into_account(t):
    sql = """insert into tasks_blockacount(acount_hash, balence ,task_num)VALUES (%s, %s, %s)"""
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql, t)  # 执行数据插入
        mysql_conn.commit()  # 提交记录
    except Exception as e:
        print(e)
        mysql_conn.rollback()

s = set()

def get_user():
    sql = """select acount_hash from tasks_blockacount"""
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql)  # 执行数据插入
        results = mysql_cursor.fetchall()
        for i in results:
            s.add(i.get('acount_hash'))

    except Exception as e:
        print(e)
        mysql_conn.rollback()

def get_user_balance(account):
    sql = f"select balence from tasks_blockacount where acount_hash='{account}'"
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql)  # 执行数据插入
        result = mysql_cursor.fetchone()
        return float(result.get('balence'))
    except Exception as e:
        print(e)
        mysql_conn.rollback()

def maketransaction(num,poster,receiver):
    sql = f"""select balence from tasks_blockacount where acount_hash='{poster}'"""
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql)  # 执行数据插入
        result = mysql_cursor.fetchone()
        result = float(result.get('balence'))
        sql1 = f"""update tasks_blockacount set balence='{round(result-num,4)}' where acount_hash='{poster}'"""
        mysql_cursor.execute(sql1)  # 执行数据插入
        mysql_conn.commit()  # 提交记录
    except Exception as e:
        print(e)
        mysql_conn.rollback()

    sql = f"""select balence from tasks_blockacount where acount_hash='{receiver}'"""
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql)  # 执行数据插入
        result = mysql_cursor.fetchone()
        result = float(result.get('balence'))
        sql1 = f"""update tasks_blockacount set balence='{round(result+num,4)}' where acount_hash='{receiver}'"""
        mysql_cursor.execute(sql1)  # 执行数据插入
        mysql_conn.commit()  # 提交记录
    except Exception as e:
        print(e)
        mysql_conn.rollback()

def add_money(num,account):
    sql = f"""select balence from tasks_blockacount where acount_hash='{account}'"""
    mysql_cursor = mysql_conn.cursor()
    try:
        mysql_cursor.execute(sql)  # 执行数据插入
        result = mysql_cursor.fetchone()
        result = float(result.get('balence'))
        sql1 = f"""update tasks_blockacount set balence='{round(result+num,4)}' where acount_hash='{account}'"""
        mysql_cursor.execute(sql1)  # 执行数据插入
        mysql_conn.commit()  # 提交记录
    except Exception as e:
        print(e)
        mysql_conn.rollback()



get_user()

print()
def create_account():
    identify = hash(uuid.uuid4().hex)
    t3 = (identify, 30 ,0)
    s.add(identify)
    insert_into_account(t3)
    for i in range(30):
        identify = hash(uuid.uuid4().hex)
        t3 = (identify, 0 ,0)
        s.add(identify)
        insert_into_account(t3)
    while True:
        identify = hash(uuid.uuid4().hex)
        t3 = (identify, 0 ,0)
        s.add(identify)
        insert_into_account(t3)
        time.sleep(50)

a = threading.Thread(target=create_account)
a.start()
time.sleep(1)


def add_account_tasknum():
    while True:
        mysql_conn = pymysql.connect(user='root',  # 用户名
                                     password='123456',  # 密码
                                     db='kanban',  # 数据库名
                                     host='192.168.3.32',  # 地址
                                     port=3306,
                                     cursorclass=pymysql.cursors.DictCursor,
                                     charset='utf8')
        sql = """select * from tasks_blockacount"""
        mysql_cursor = mysql_conn.cursor()
        try:
            mysql_cursor.execute(sql)
            results = mysql_cursor.fetchall()
            for i in results:
                sql2 = f"""update tasks_blockacount set task_num='{i['task_num']+random.randint(0,10)}' where id='{i['id']}'"""
                mysql_cursor.execute(sql2)
            mysql_conn.commit()
        except Exception as e:
            print(e)
            mysql_conn.rollback()
        time.sleep(random.randint(5,10))
        mysql_conn.close()




b = threading.Thread(target=add_account_tasknum)
b.start()
















i = 1
while True:
    time.sleep(5)
    print('1111111111111111')
    j = random.randint(1, 20)
    for l in range(j):
        identify = uuid.uuid4().hex
        status = 0
        block_belong = i
        create_time = datetime.datetime.now()
        receiver = random.sample(list(s),1)[0]

        while True:
            poster = random.sample(list(s),1)[0]
            if receiver != poster:
                poster_balance = get_user_balance(poster)
                if poster_balance != 0:
                    break
        task_num = str(random.random()) + " NTA"
        task_price = str(random.random()) + " NTA"
        op_num = random.randint(1, 1024)
        transaction = round(random.uniform(0, poster_balance),4)

        input_data = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5))
        t = (identify, status, block_belong, create_time, receiver, poster, transaction, task_num, task_price, op_num, input_data)
        insert_into_blocktask(t)
        maketransaction(transaction, poster, receiver)
        print()


    block_out_time = datetime.datetime.now()
    deal_content = random.randint(1, 80)
    op_num = random.randint(1, 1024)
    hashcode = hash(str(transaction) + str(deal_content) + str(op_num))
    f_hash = hash(transaction)
    miner = random.sample(list(s),1)[0]




    size = transaction + deal_content
    reward_1 = round(random.uniform(30.0,50.0),4)
    reward = str(reward_1) + " NTA"
    additional_data = ''.join(random.sample(['z','y','x','w','v','u','t','s','r','q','p','o','n','m','l','k','j','i','h','g','f','e','d','c','b','a'], 5))


    #---------------------------------
    deal_content = random.randint(20,40)
    #---------------------------------

    block_depth = i
    t2 = (block_out_time, deal_content, hashcode, f_hash, miner, size,
        op_num, reward, additional_data, block_depth)
    insert_into_block(t2)
    add_money(reward_1,miner)





    i += 1
    sce = random.randint(1, 5)
    time.sleep(sce)






