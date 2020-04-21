# -*- coding: utf-8 -*-
# @Time      :2020/4/5 下午 04:45
# @File      :Timer.py
import datetime
import os
import time


def timer():
    while True:
        #构造明天0.时间
        now = datetime.datetime.now()+datetime.timedelta(days=1)
        time_str = now.strftime('%Y-%m-%d 18:0:0')
        #计算差值
        date = time.strptime(time_str, "%Y-%m-%d %H:%M:%S")
        localtime = time.localtime(time.time())
        need_sleep = time.mktime(date) - time.mktime(localtime)
        #打印及计算
        print("=" * 50)
        print("=" * 50)
        print('下次运行时间：',time.strftime('%Y-%m-%d %H:%M:%S',date),'剩余秒数：%d'%(need_sleep))
        time.sleep(need_sleep)

        run()

def run():
    os.system("python mgd_report.py")

run()
timer()

