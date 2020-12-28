import os
import subprocess
import time
import win32api
import win32process
import zipfile
from win32api import ShellExecute

import requests



running_node = {}


def get_node_type():
    nodetype = []
    dirdiles = os.listdir('node_store')
    for i in dirdiles:
        if i.endswith('.zip'):
            nodetype.append(os.path.splitext(i)[0])
    return nodetype

def down_demo(url, filename):


    print('开始下载!')
    s = requests.session()
    r = s.get(url,)
    with open(filename, 'wb') as f:
        f.write(r.content)
        f.close()
    print('下载完成!')


def unzip(zippath,user_id,num=1,filepath='node_file'):
    '''
    修改zip
    if zinfo.flag_bits & 0x800:
                # UTF-8 filename
                fname_str = fname.decode("utf-8")
            else:
                # fname_str = fname.decode("cp437")
                # todo:我添加的
                fname_str = fname.decode("gbk")

    if flags & 0x800:
                # UTF-8 file names extension
                filename = filename.decode('utf-8')
            else:
                # Historical ZIP filename encoding
                # filename = filename.decode('cp437')
                # todo:我添加的
                filename = filename.decode('gbk')
    :param zippath:
    :param filepath:
    :return:
    '''
    filename = os.path.basename(zippath).split('.')[0]
    for i in range(num):
        t = i
        while 1:
            if os.path.exists(f'{filepath}/{filename}_{t}'):
                t+=1
            else:
                break
        z = zipfile.ZipFile(zippath, 'r')
        z.extractall(path=f"{filepath}/{filename}_{t}")
        z.close()
        path = f"{filepath}\\{filename}_{t}\\node.exe"
        open_node(path,user_id)
        return path










def open_node(filepath,user_id):
    import os
    cur_path = os.getcwd()
    if os.path.exists(filepath):
        dir = os.path.dirname(filepath)
        os.chdir(dir)
        handle = win32process.CreateProcess(os.path.basename(filepath), str(user_id), None, None, 0, win32process.CREATE_NO_WINDOW, None, None,
                                            win32process.STARTUPINFO())
        global running_node
        running_node[filepath] = handle

        os.chdir(cur_path)


        return handle
    return
        # # 创建进程
    # p = subprocess.Popen(filepath, shell=False)
    # # 获得 pid
    # pid = p.pid
    # 监听
    # glan = psutil.Process(pid)

def delete_node(node_path):
    import os
    import shutil
    close_node(node_path)
    rootdir = os.path.dirname(node_path)
    filelist = os.listdir(rootdir)  # 列出该目录下的所有文件名
    for f in filelist:
        filepath = os.path.join(rootdir, f)  # 将文件名映射成绝对路劲
        if os.path.isfile(filepath):  # 判断该文件是否为文件或者文件夹
            os.remove(filepath)  # 若为文件，则直接删除
            # print(str(filepath) + " removed!")
        elif os.path.isdir(filepath):
            shutil.rmtree(filepath, True)  # 若为文件夹，则删除该文件夹及文件夹内所有文件
            # print("dir " + str(filepath) + " removed!")
    shutil.rmtree(rootdir, True)  # 最后删除img总文件夹

def close_node(node_path):

    global running_node
    handle = running_node.get(node_path)
    if not handle:
        return

    # win32process.TerminateProcess(handle[0],0)



    pid = handle[2]
    # 本函数用于中止传入pid所对应的进程
    if os.name == 'nt':
        # Windows系统
        cmd = 'taskkill /pid ' + str(pid) + ' /f'
        try:
            os.system(cmd)
            print(pid, 'killed')
        except Exception as e:
            print(e)
    elif os.name == 'posix':
        # Linux系统
        cmd = 'kill ' + str(pid)
        try:
            os.system(cmd)
            print(pid, 'killed')
        except Exception as e:
            print(e)
    else:
        print('Undefined os.name')





def drop_rub():
    root_path = 'node_file'
    node_file_list = os.listdir(root_path)
    for f in node_file_list:
        filepath = os.path.join(root_path, f)
        if os.path.isdir(filepath):
            is_delete = True
            for i in os.listdir(filepath):
                if i.endswith('.exe'):
                    is_delete = False
                    break
            if is_delete:
                # print(filepath)
                delete_node(filepath+'\\1')


import time
from pySmartDL import SmartDL


downloadTask = {}

def get_download_state(url):
    '''
    通过下载的url 得到下载任务状态
    :param url: 下载url
    :return: None=没有当前url下载任务 如果下载完成 返回文件路径 下载未完成 返回-1
    '''
    global downloadTask
    task_obj = downloadTask.get(url)
    if task_obj:
        if task_obj.isFinished():
            del downloadTask[url]
            return task_obj.dest
        return -1


def download(url,path='node_store'):
    obj = SmartDL(url, path,progress_bar=False)
    obj.start(blocking=False)

    global downloadTask
    downloadTask[url] = obj
    return 0
    # while not obj.isFinished():
    #         print("Speed: %s" % obj.get_speed(human=True))
    #         print("Already downloaded: %s" % obj.get_dl_size(human=True))
    #         print("Eta: %s" % obj.get_eta(human=True))
    #         print("Progress: %d%%" % (obj.get_progress()*100))
    #         print("Progress bar: %s" % obj.get_progress_bar())
    #         print("Status: %s" % obj.get_status())
    #         print("\n"*2+"="*50+"\n"*2)
    #         time.sleep(0.2)
    #
    # if obj.isSuccessful():
    #         print("downloaded file to '%s'" % obj.get_dest())
    #         print("download task took %ss" % obj.get_dl_time(human=True))
    #         print("File hashes:")
    #         print(" * MD5: %s" % obj.get_data_hash('md5'))
    #         print(" * SHA1: %s" % obj.get_data_hash('sha1'))
    #         print(" * SHA256: %s" % obj.get_data_hash('sha256'))
    # else:
    #         print("There were some errors:")
    #         for e in obj.get_errors():
    #                 print(str(e))




if __name__ == '__main__':



    # 下载测试
    url = 'https://qd.myapp.com/myapp/qqteam/pcqq/PCQQ2020.exe'

    download(url)

    while True:
        state = get_download_state(url)
        time.sleep(0.5)
        print(state)
        if state and state != -1:
            break
    print(downloadTask)


    #解压测试
    unzip('node_store/db_node.zip',31)




# print(get_node_type())

# drop_rub()

# path = 'node_file/db_node/node.exe'
# pid = open_node(path)
# time.sleep(20)
# close_node(path)
