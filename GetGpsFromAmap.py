# -*- coding: utf-8 -*-
# @Time      :2020/4/2 下午 08:08
# @File      :getGpsFromAmap.py
import requests
import json

class GetGpsFromAmap:
    '''
    使用高德api进行地址搜索
    请先填写__apiKey,可以通过https://lbs.amap.com/api/获得
    构造对象后可以使用getAnswer搜索并获得答案，
    getAddress等获得细答案的函数必须使用在setInfo或者getAnswer后使用，否则没有答案。
    '''
    def __init__(self,keyWords:str,city:str):
        self.__apiKey = ""
        #self.apiName = "get_gps"

        self._keyWords = keyWords
        self._city = city

        self.__baseUrl = r"https://restapi.amap.com/v3/place/text?key={}&keywords={}&city={}&extensions=base"
        self._url = self.__baseUrl.format(self.__apiKey, self._keyWords, self._city)

        self.allAnswers = {}
        #直接调用搜索
        self.getAnswer()

    def setInfo(self,keyWords:str,city:str):
        '''
        重新设置查询信息并查找
        :param keyWords:查询关键字
        :param city:信息
        :return:返回一个字典，是第一个答案
        '''
        self._keyWords = keyWords
        self._city = city
        self._url = self.__baseUrl.format(self.__apiKey, self._keyWords, self._city)
        return self.getAnswer()


    def getAnswer(self,whichOne=0):
        '''
        搜索并返回选择的答案,默认为第一个
        :return: 返回一个字典
        '''
        request = requests.get(url=self._url)
        request = json.loads(request.text)
        self.allAnswers = request["pois"]
        return request["pois"][whichOne]

    def getAddress(self,whichOne=0):
        '''
        获得上一个搜索到地址
        :return: 返回str
        '''
        self._judgeAnswer()
        return self.allAnswers[whichOne]["address"]

    def getGps(self,whichOne=0):
        '''
        获得上一个搜索到的gps
        :return: 返回字符串列表e.z['121.32484','31.12224']
        '''
        self._judgeAnswer()
        location = (self.allAnswers[whichOne]["location"]).split(",")
        return location

    def getFindName(self,whichOne=0):
        '''
        获得上一个搜索的答案
        :param whichOne:
        :return:
        '''
        self._judgeAnswer()
        return self.allAnswers[whichOne]["name"]

    def getProvinceCityDistrict(self,whichOne=0):
        '''
        获得省市区
        :return:返回一个list,[省,市,区]
        '''
        self._judgeAnswer()
        return [self.allAnswers[whichOne]["pname"],
                self.allAnswers[whichOne]["cityname"],
                self.allAnswers[whichOne]["adname"]]

    def _judgeAnswer(self):
        if not self.allAnswers:
            raise RuntimeError("没有答案，需要先通过setInfo/getAnswer获得答案")


getGps = GetGpsFromAmap("美兰湖","上海")
answer = getGps.getAnswer()
a = getGps.getAddress()
b = getGps.getGps()
c = getGps.getFindName()
d = getGps.getProvinceCityDistrict()
print(a+b+c+d) 


