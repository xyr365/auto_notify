<h1 align="center">fzu-auto_notify</h1>

# 功能

1. 已经实现的功能
    - [x] 统计签到/信息收集完成情况
    - [x] 签到/填报异常名单统计
    - [x] 进行QQ私聊通知（依赖于cq）
    - [x] 进行邮箱通知
    - [x] 腾讯云短信通知（自行申请，付费1000条/50元）
2. 正在测试中的功能
    - [x] 异常名单通知
<p align="center"><img src="https://github.com/xyr365/auto_notify/blob/main/IMG/total.png?raw=true"/></p>

> 你可能需要这些东西👇

1. 在辅导猫特殊关注辅导员，获取助教权限（需获得辅导员同意）

![step1](https://github.com/xyr365/auto_notify/blob/main/IMG/fo.png?raw=true)

2. 构建自己的邮件发送API，

    如果你需要使用邮箱通知的话需要用到[API申请](https://mp.weixin.qq.com/s?__biz=MzA3NzMwNjM0MA==&mid=2649807321&idx=1&sn=35710d5df1f778b83f2a38c8e7a0ddf9&chksm=87507952b027f0444cfdfd03e7bc8d992ead5cdc2ddaa787d8405ea5f49412581693fa4617e9&mpshare=1&scene=23&srcid=10071p9HrVkTV194DXVtDeWz&sharer_sharetime=1633540006916&sharer_shareid=cde0c199d9f6ce11f7bcb010f1564c15#rd)进行相关申请
    JSON=
            {
            "mailto": "",
            "mialsub": "",
            "mailbody": ""
            }

3. 使用CQ进行私聊通知提醒
    [使用该项目](https://github.com/Mrs4s/go-cqhttp)登陆拥有好友关系的QQ进行私聊提醒，qq只要登陆就行，没什么其他设置要求
