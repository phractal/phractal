# import time
#
# import psutil
# from django.test import TestCase
# import time
# import wmi
# from psutil import long
#
#
# # Create your tests here.
# _timer = getattr(time, 'monotonic', time.time)
# num_cpus = psutil.cpu_count() or 1
# node_list = wmiInterface.Win32_Process(name="dwm.exe")
# wmiInterface.Win32_PhysicalMemory()
# cpu_userd = 0
# if node_list:
#     for process in node_list:
#         pid = process.ProcessID
#         p = psutil.Process(pid)
#         cpu_percent = p.cpu_percent()  ###cpu
#         mem_percent = p.memory_percent()  ###内存
#         print(cpu_percent, mem_percent)
#
# # def timer():
# #     return _timer() * num_cpus
#
# dict1= {'1':1,'2':2}
# for dict2 in dict1:
#     print(dict2)
# # pid_cpuinfo = {}
# #
# #
# # def GetProcessCPU_Pre(id):
# #     p = psutil.Process(id)
# #     pt = p.cpu_times()
# #     st1, pt1_0, pt1_1 = timer(), pt.user, pt.system  # new
# #     st0, pt0_0, pt0_1 = pid_cpuinfo.get(id, (0, 0, 0))  # old
# #
# #     delta_proc = (pt1_0 - pt0_0) + (pt1_1 - pt0_1)
# #     delta_time = st1 - st0
# #     try:
# #         cpus_percent = ((delta_proc / delta_time) * 100)
# #     except:
# #         cpus_percent = 0.0
# #
# #     pid_cpuinfo[id] = [st1, pt1_0, pt1_1]
# #     return "{:.2f}".format(cpus_percent)
# # print(wmiInterface.Win32_Process(name="node.exe"),1111111111111111111)
# # for process in wmiInterface.Win32_Process(name="redis-server.exe"):
# #         id = process.ProcessID
# #         res = GetProcessCPU_Pre(id)
# #         print(res)
#
#
#
#
# # process_info = {}
# # while True:  # Change the looping condition
# #     for process in wmiInterface.Win32_Process(name="chrome.exe"):
# #         id = process.ProcessID
# #         for p in wmiInterface.Win32_PerfRawData_PerfProc_Process(IDProcess=id):
# #             n1, d1 = long(p.PercentProcessorTime), long(p.Timestamp_Sys100NS)
# #             n0, d0 = process_info.get(id, (0, 0))
# #             try:
# #                 percent_processor_time = (float(n1 - n0) / float(d1 - d0)) * 100.0
# #             except ZeroDivisionError:
# #                 percent_processor_time = 0.0
# #             process_info[id] = (n1, d1)
# #
# #             print(id, process.Caption, str(percent_processor_time))
cpu_dict={1:3,2:2,}
max_cpu_pid = list(cpu_dict.keys())[list(cpu_dict.values()).index(max(cpu_dict.values()))]
print(max_cpu_pid)