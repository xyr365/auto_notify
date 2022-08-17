<h1 align="center">🏳️‍🌈fzu-auto_notify🏳️‍🌈</h1>
 ####本人非科班出身纯属兴趣，代码水平低，各位大佬就看个乐。
 
 ###由于毕业没有账号用于测试，程序可能存在错误。
    

## 👑项目说明

#### 欢迎进群交流QQ：182396855
    
# 👑功能

1. 已经实现的功能
    - [x] 统计签到/信息收集完成情况
    - [x] 签到/填报异常名单统计
    - [x] 进行QQ私聊通知（依赖于cq）
    - [x] 进行邮箱通知
    - [x] 腾讯云短信通知（自行申请购买，1000条/50元）默认移除，需自行修改。
2. 正在测试中的功能
    - [x] 查寝（没账号）
<p align="center"><img src="https://github.com/xyr365/auto_notify/blob/main/IMG/total.png?raw=true"/></p>

# 你可能需要这些东西👇


1. 在辅导猫特殊关注辅导员，获取助教权限（需获得辅导员同意）

![step1](https://github.com/xyr365/auto_notify/blob/main/IMG/fo.png?raw=true)

2. 构建自己的邮件发送API，短信通知要钱，邮箱有概率进垃圾箱，建议使用QQ

    如果你需要使用邮箱通知的话需要用到[API申请](https://mp.weixin.qq.com/s?__biz=MzA3NzMwNjM0MA==&mid=2649807321&idx=1&sn=35710d5df1f778b83f2a38c8e7a0ddf9&chksm=87507952b027f0444cfdfd03e7bc8d992ead5cdc2ddaa787d8405ea5f49412581693fa4617e9&mpshare=1&scene=23&srcid=10071p9HrVkTV194DXVtDeWz&sharer_sharetime=1633540006916&sharer_shareid=cde0c199d9f6ce11f7bcb010f1564c15#rd)进行相关申请
    JSON=
            {
            "mailto": "",
            "mialsub": "",
            "mailbody": ""
            }

3. 使用CQ进行私聊通知提醒
    [使用该项目](https://github.com/Mrs4s/go-cqhttp)登陆拥有好友关系的QQ进行私聊提醒，qq只要登陆就行，没什么其他设置要求

## ✅关于cookie
浏览器,打开辅导猫登录-F12-网络-标头中找。cookie 程序大约10分钟左右运行一次可以保证长期有效
![step1](https://github.com/xyr365/auto_notify/blob/main/IMG/fo.png?raw=true)

    
## ✅关于QQ群@未填人员
   由于我自己使用的已经被我改得乱七八糟，就不修改仓库代码了，以下是QQ群@的示例

        if resj['code'] == '0':
        csj = ''
        with open('cs.txt', 'r') as cs:
            csj = json.load(cs)
        t = "每日一报，已提交{tnum}人，未提交{unum}人：\n"
        names = t.format(tnum = resj['datas']['handledSize'], unum = resj['datas']['unHandledSize'])
        qmsg = names
        for i in range(0, resj['datas']['totalSize']):
            name = resj['datas']['rows'][i]['name']
            num = resj['datas']['rows'][i]['userId']
            for k in range(0, len(csj)) :
                if csj[k]['userId'] == num :
                    names = names + name  + "(1), "
                    qmsg = "{qmsg}    {name}(1)[CQ:at,qq={qq}]\n".format(qmsg = qmsg, name = name, qq = csj[k]['qq'])
                    break
                elif k == len(csj)-1 :
                    names = names + name + "(0), "
                    #qmsg = qmsg + name + "(0)"
                    qmsg = "{qmsg}    {name}(0)\n".format(qmsg = qmsg, name = name)
        print(qmsg)
        sendQmsgChan(qmsg)
    
   CQ的请求地址
    
    http://127.0.0.1:5700/send_group_msg?group_id=797362564&message={qmsg}
    
## ✅关于使用
1. 催报任务仅限信息收集、签到。由于签到任务万年不变写的比较死，信息收集部分各位可以根据自身需求更改通知方式
