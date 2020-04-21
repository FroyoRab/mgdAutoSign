# -*- coding: utf-8 -*-
# @Time      :2020/4/1 下午 05:02
# @File      :moguding_sign.py
import datetime
import json
import GetGpsFromAmap

import requests


class mgd_sign:
    def __init__(self):
        self.url_pre = r"https://api.moguding.net:9000"
        self.user_agent = 'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; Android SDK built for x86 Build/KK) ' \
                     'AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30'
        #用户名密码token
        self.user = ""
        self.password = ""
        self.token = ""
        self.address = ""
        self.findAddress = ""
        # 省市区
        self.province = ""
        self.city = ""
        self.country = ""
        #经纬度
        self.longitude = ""
        self.latitude = ""
        #实习计划id
        self.planId = "f93a290c90a38ef2605dcff5f669f7a4"

    def __refresh(self):
        '''
        刷新头信息，data信息等
        :return:
        '''
        self.login_data = {
            "phone": self.user,
            "uuid": "",
            "password": self.password,
            "loginType": "android"
        }

        self.sign_data = {
            "address": self.address,
            "description": "",
            "device": "Android",
            "province": self.province,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "planId": self.planId,
            "type": "START",
            "city": self.city,
            "country": self.country
        }

        self.header = {
            'Host': 'api.moguding.net:9000',  # host地址
            'User-Agent': self.user_agent,
            'roleKey': 'student',
            'Authorization': self.token,
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Content-Type': 'application/json; charset=UTF-8',
            'Connection': 'close',
            'Cache-Control': 'no-cache'
        }

    def set_accountInfo(self,user_name,password,address:str,city:str):
        '''
        设置用户信息，签到信息
        :param user_name: 账号
        :param password: 密码
        :param address: 地址
        :param city: 城市
        :return:
        '''
        self.user = user_name
        self.password = password
        self.address = address
        search_req = GetGpsFromAmap.GetGpsFromAmap(address, city)
        self.findAddress = search_req.getAddress()
        pcc = search_req.getProvinceCityDistrict()
        # 省市区
        self.province = pcc[0]
        self.city = pcc[1]
        self.country = pcc[2]
        gps = search_req.getGps()
        #经纬度
        self.longitude = gps[0]
        self.latitude = gps[1]
        self.__refresh()

    def __login(self):
        '''
        登陆并设置token
        :return:
        '''
        # 代理服务器
        # proxies = {"https": "http://127.0.0.1:8080"}
        # response = requests.post(
        #     url=self.url_pre + '/session/user/v1/login',
        #     json=self.login_data,
        #     headers=self.header,
        #     proxies=proxies,
        #     verify=False
        # )
        response = requests.post(
            url=self.url_pre + '/session/user/v1/login',
            json=self.login_data,
            headers=self.header
        )
        response_dict = json.loads(response.text)
        #判断返回码，返回消息
        if response_dict["code"]==200 and response_dict["msg"]=='success':
            response_data = response_dict["data"]["orgJson"]
            #提取姓名学号
            #print(response_data["userName"]+':'+response_data["studentNumber"])
            if response_dict["data"]["token"]:
                #设置token
                self.token = response_dict["data"]["token"]
                print(response_data["userName"]+"登陆成功!",end="")
                #print("token:"+self.token)
                self.__refresh()
                print("签到地址：" + self.findAddress)
                return
        else:
            print(response.text)
            raise RuntimeError("登陆失败"+str(self.user))

    def __get_planId(self):
        '''
        获得实习计划，并选择最后的那个id
        :return:
        '''
        data = {
            'state':""
        }
        # 代理服务器
        # proxies = {"https": "http://127.0.0.1:8080"}
        # response = requests.post(
        #     url=self.url_pre + '/practice/plan/v1/getPlanByStu',
        #     json=data,
        #     headers=self.header,
        #     proxies=proxies,
        #     verify=False
        # )
        response = requests.post(
            url=self.url_pre + '/practice/plan/v1/getPlanByStu',
            json=data,
            headers=self.header
        )

        response_dict = json.loads(response.text)
        #判断返回码，返回消息
        if response_dict["code"]==200 and response_dict["msg"]=='success':
            response_data = response_dict["data"][-1]
            if response_data["planId"]:
                #设置planid
                self.planId = response_data["planId"]
                print("实习计划id获取成功！ 实习计划名："+response_data["planName"])
                self.__refresh()
                return

        print(response.text)
        raise RuntimeError("获取planId失败")

    def __sign_in(self,select:int):
        '''
        签到
        :param select: 0为START,1为END
        :return:
        '''
        if select==1:
            self.sign_data["type"]="END"
        else :
            self.sign_data["type"]="START"
        # 代理服务器
        # proxies = {"https": "http://127.0.0.1:8080"}
        # response = requests.post(
        #     url=self.url_pre + '/attendence/clock/v1/save',
        #     json=self.sign_data,
        #     headers=self.header,
        #     proxies=proxies,
        #     verify=False
        # )
        response = requests.post(
            url=self.url_pre + '/attendence/clock/v1/save',
            json=self.sign_data,
            headers=self.header
        )
        response_dict = json.loads(response.text)
        #response_data = response_dict["data"]["orgJson"]
        #判断返回码，返回消息
        if response_dict["code"]==200 and response_dict["msg"]=='success':
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),end=" : ")
            if select==1:
                print("下班√")
                return
            else:
                print("上班√",end=" —— ")
                return

        print(response.text)
        raise RuntimeError("签到失败")

    def run(self):
        '''
        请先使用set_accountInfo设置信息
        :param select: 上班为0，下班为1
        :return:
        '''
        try:
            self.__login()
            self.__get_planId()
            self.__sign_in(0)
            self.__sign_in(1)
        except Exception as err:
            print(err)