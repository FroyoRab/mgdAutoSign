# -*- coding: utf-8 -*-
# @Time      :2020/4/3 下午 08:22
# @File      :GetExlFromMikeCRM.py
import os

import requests
import json
from urllib import parse

class GetExl:
    def __init__(self,exlId:str):
        '''
        注意填写account:用户名
              password1:密码1
              password2:密码2  这两个密码可以通过mike登陆时抓包得到，chrome的F12应该就能做到
        :param exlId: 问卷id 可以在表单的收集反馈页面查看url结尾的数字得到。
        '''
        self.__account = ""
        self.__password1 = ""
        self.__password2 = ""
        self.__exlId = exlId
        self.__url = r"https://cn.mikecrm.com"
        self.__cookies = ""
        self.file_name = ""
        self.__login()

    def __refresh(self):
        #构建登陆包
        self.__login_data = {
            "al":1,
            "a":self.__account,
            "p1":self.__password1,
            "p2":self.__password2
        }
        self.__login_data = "d="+parse.quote(json.dumps({"cvs":self.__login_data}))

        self.__getExl_data = {
            "i":self.__exlId
        }
        self.__getExl_data = "d="+parse.quote(json.dumps({"cvs":self.__getExl_data}))

        self.__login_header = {
            "Host":"cn.mikecrm.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
            "Accept":"application/json, text/javascript, */*; q=0.01",
            "Accept-Language":"zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding":"gzip, deflate",
            "Content-Type":"application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With":"XMLHttpRequest",
            "Referer":"https://cn.mikecrm.com/login.php"
        }
        self.__getExl_header = {
            "Host": "cn.mikecrm.com",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://cn.mikecrm.com/login.php"
        }


    def __login(self):
        self.__refresh()
        # 代理服务器
        #proxies = {"https": "http://127.0.0.1:8080"}
        #response = requests.post(
        #    url = self.__url + "/handler/web/login/handleLogin.php",
        #    data = self.__login_data,
        #    headers = self.__login_header,
        #    proxies=proxies,
        #    verify=False,
        #)
        response = requests.post(
            url = self.__url + "/handler/web/login/handleLogin.php",
            data = self.__login_data,
            headers = self.__login_header,
        )
        res_info = json.loads(response.text)
        if response.status_code==200 and res_info["n"]=="Froyo":
            print(res_info["clSld"]+" 麦克表单登陆成功！正在下载表单……")
            self.__cookies = response.cookies
            self.__get_exl()
            return
        raise RuntimeError("登陆失败！")


    def __get_exl(self):
        self.__refresh()
        # 代理服务器
        #proxies = {"https": "http://127.0.0.1:8080"}
        #response = requests.post(
        #    url = self.__url + "/handler/web/form_submit/handleDownloadAndExport.php",
        #    data = self.__getExl_data,
        #    headers = self.__getExl_header,
        #    proxies=proxies,
        #    cookies = self.cookies,
        #    verify=False,
        #)
        response = requests.post(
            url = self.__url + "/handler/web/form_submit/handleDownloadAndExport.php",
            data = self.__getExl_data,
            headers = self.__getExl_header,
            cookies=self.__cookies
        )
        res_info = json.loads(response.text)
        file_name = res_info["fn"]
        real_name = res_info["frn"]
        self.__download_exl(real_name, file_name)

    def __download_exl(self, real_name, fire_name):
        data = {
            "fn":fire_name,
            "frn":real_name,
        }
        data = {
            "cvs":data
        }
        #urldecode过的拼接过的url
        url = self.__url+"/_DOWNLOAD_EXPORTED/"+\
        "{frn}?d={data}".format(frn=parse.quote(real_name),data=(json.dumps(data)))
        response = requests.get(url=url, cookies=self.__cookies)
        if response.status_code==200 and response.content!="":
            #self.__del_oldFile()
            self.file_name=real_name
            file = open(real_name,"wb")
            file.write(response.content)
            file.close()
            print("……"+real_name+" 下载成功！")
            print("="*30)
            return real_name
        raise RuntimeError("……下载失败！")

    def __del_oldFile(self):
        file_list = os.listdir(os.getcwd())
        for file_name in file_list:
            if file_name.find(".xls")!=-1:
                os.remove(file_name)
                print("……删除旧文件-"+file_name)
                return
        else:
            print("……未找到旧文件")

    def get_fileName(self):
        return self.file_name
