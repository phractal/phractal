from pySmartDL import SmartDL


url = "https://qd.myapp.com/myapp/qqteam/pcqq/PCQQ2020.exe"
dest = "node_store" # or '~/Downloads/' on linux

# obj = SmartDL(url, dest)
# obj.start()
# # [*] 0.23 Mb / 0.37 Mb @ 88.00Kb/s [##########--------] [60%, 2s left]
# print('1111111111111111')
# path = obj.get_dest()
# print(path)









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


url = 'https://qd.myapp.com/myapp/qqteam/pcqq/PCQQ2020.exe'


download(url)

while True:
    state = get_download_state(url)
    time.sleep(0.5)
    print(state)
    if state and state != -1:
        break
print(downloadTask)
