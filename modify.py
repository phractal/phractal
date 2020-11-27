# -*- encoding:utf-8 -*-

import os

path = os.getcwd()

import os
from utils.weixin_pay import get_sign, API_KEY

# def modify_name(field, file_dir):
#     for root, dirs, files in os.walk(file_dir):
#         for file in files:
#             if "txt" in file:
#                 file.replace("txt", "")
#
#
# if __name__ == '__main__':
#     field = ""
#     modify_name(field, path)

xml_data = {'appid': 'wx34ab6ee729131856', 'bank_type': 'CFT', 'cash_fee': 1, 'fee_type': 'CNY', 'is_subscribe': 'N',
            'mch_id': 1543940791, 'nonce_str': 'JkaKMhNVulUjRmPUfNtZMVCGxGYkUrTc',
            'openid': 'ozf5W4zaNCtqg7sHabz4yl6zQwRk', 'out_trade_no': 2240156627936741111063, 'result_code': 'SUCCESS',
            'return_code': 'SUCCESS', 'sign': '0D3324FFF87883EAE15264693C44FE9E', 'time_end': 20190820133638,
            'total_fee': 1, 'trade_type': 'NATIVE', 'transaction_id': 4200000376201908203371447943}

back_sign = xml_data.pop("sign")
generate_sign = get_sign(xml_data, API_KEY)
# print(back_sign, generate_sign)

from xml.etree.cElementTree import Element, tostring


def dict_to_xml(d, tag="xml"):
    '''
    Turn a simple dict of key/value pairs into XML
    '''

    elem = Element(tag)
    for key, val in d.items():
        child = Element(key)
        child.text = str(val)
        elem.append(child)
    return elem


# print(tostring(dict_to_xml(d={"return_code": "SUCCESS", "return_msg": "OK"})))


def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]

            j -= 1

        arr[j + 1] = key
    print(arr)


def insertion_sort1(arr):
    for i in range(1, len(arr)):
        for j in range(i, 0, -1):
            if arr[j] < arr[j - 1]:
                arr[j - 1], arr[j] = arr[j], arr[j - 1]
    print(arr)


def selection_sort(arr):
    for i in range(len(arr)):
        min_idx = i
        for j in range(i + 1, len(arr)):
            if arr[j] < arr[min_idx]:
                min_idx = j

        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    print(arr)


# 冒泡排序 i 每次比较的第几次的次数
def bubble_sort(arr):
    for i in range(len(arr)):
        for j in range(len(arr) - i - 1):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    print(arr)


def bubble_sort1(arr):
    for i in range(len(arr) - 1, 0, -1):
        for j in range(i):
            if arr[j] < arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

    print(arr)


def quick_sort(arr):
    if len(arr) < 2:
        return arr
    mid = arr[len(arr) // 2]
    left, right = [], []
    arr.remove(mid)
    for item in arr:
        if item >= mid:
            right.append(item)
        else:
            left.append(item)
    return quick_sort(left) + [mid] + quick_sort(right)


def merge_sort(arr):
    if len(arr) < 2:
        return arr
    middle = len(arr) // 2
    left, right = arr[0:middle], arr[middle:]
    return merge(merge_sort(left), merge_sort(right))


def merge(left, right):
    result = []
    while left and right:
        if left[0] <= right[0]:
            result.append(left.pop(0))
        else:
            result.append(right.pop(0))
    while left:
        result.append(left.pop(0))
    while right:
        result.append(right.pop(0))
    return result


def jiecheng(x):
    if x == 0 or x == 1:
        return 1
    else:
        return x * jiecheng(x - 1)


def fibonacci(n):
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


def fibonacci1(n):
    a, b = 0, 1
    while n > 0:
        a, b = a + b, a
        n -= 1
        yield a


def fibonacci2():
    a, b = 0, 1
    while True:
        yield a
        a, b = a + b, a


def heapify(arr, n, i):
    if n < i:
        return
    max_ = i
    left = 2 * i + 1
    right = 2 * i + 2
    if left < n and arr[max_] < arr[left]:
        max_ = left
    if right < n and arr[max_] < arr[right]:
        max_ = right
    if max_ != i:
        arr[i], arr[max_] = arr[max_], arr[i]
        heapify(arr, n, max_)


# 排序
def heap_sort(arr):
    n = len(arr)
    for i in range(n, -1, -1):
        heapify(arr, n, i)
    for j in range(n - 1, 0, -1):
        arr[j], arr[0] = arr[0], arr[j]
        heapify(arr, j, 0)


if __name__ == '__main__':
    import time

    a = [1, 0, 6, 5, 4, 8, 12, 0]
    heap_sort(a)
    print(a)
    print(8 * 7 * 6 * 5 * 4 * 3 * 2)
