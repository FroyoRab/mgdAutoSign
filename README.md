# 蘑菇钉自动签到

## 流程

1. 填写资料问卷：http://froyorab.mikecrm.com/JymazWh
2. 等待明天`18:01:00`后查看自己是否已经签到

## 注意

- 如果发现哪天自己没签到请记得联系我。
- 暂时只能同时签到上班和下班。
- 地址栏注意格式，签到是要上报gps定位的，靠的是高德的地址查找定位，所以麻烦写一个找得到的地址。

---

> 蘑菇丁app的每天自动签到。
> **需要我写的另一个高德地图的文件一起使用**
>
> - 使用方法
>
>   ```python
>   import moguding_sign
>   moguding_sign.mgd_sign().set_accountInfo(account,password,address,city)
>   mgd.run()
>   #之后可以重复使用set_accountInfo()后调用run()不需要重复创建类对象
>   ```
>
>   自己觉得备注写的蛮全的了_(:_」∠)_ 不写其他的了

**源码在项目里都有**
