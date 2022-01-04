<h1 align="center">🏳️‍🌈fzu-auto_notify🏳️‍🌈</h1>
<h1 align="center">🏳️‍🌈有空再更新🏳️‍🌈</h1>
        基于[@ZimoLoveShuang][@thriving123]项目，开发的今日校园任务催报脚本，本人非计算机专业纯属兴趣，代码水平低，各位大佬就看个乐。
    另外本人因能力以及精力有限，可能无法适配其他学校以及进行更新，望各位海涵。
    

## 👑项目说明

本项目严禁用于收费相关业务，您可以借助本项目进行二次开发或者完善
#### 欢迎进群交流QQ：182396855
#### 虽然不懂星星能干嘛，但大哥们给个star吧🙏
    
# 👑功能

1. 已经实现的功能
    - [x] 统计签到/信息收集完成情况
    - [x] 签到/填报异常名单统计
    - [x] 进行QQ私聊通知（依赖于cq）
    - [x] 进行邮箱通知
    - [x] 腾讯云短信通知（自行申请购买，1000条/50元）默认移除，需自行修改。
2. 正在测试中的功能
    - [x] 异常名单通知
<p align="center"><img src="https://github.com/xyr365/auto_notify/blob/main/IMG/total.png?raw=true"/></p>

# 你可能需要这些东西👇


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

## ✅关于依赖
   安装依赖：到这一步，您就可以开始执行以下命令开始安装依赖了。在`cmd`中~~输入~~粘贴上以下代码按回车即可安装依赖

    pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple
    
   到这一步，可能会缺少腾讯云sdk依赖。在`cmd`中~~输入~~粘贴上以下代码按回车即可安装依赖
    
    pip install -i https://mirrors.tencent.com/pypi/simple/ --upgrade tencentcloud-sdk-python
    
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
1. FZU的cas登陆失效，我目前使用CK运行，辅导猫网页登陆F12即可获取MOD_auth需要定时运行保活。
2. 可使用Releases中的打包版本，无需python环境以及相关依赖
3. config.yml文件中配置账号、密码、学校。
4. cs.txt文件中输入学号、QQ（注意josn格式）,用于邮箱、QQ私聊通知
5. xcfg.yml中进行相关详细相关设置。（任务筛选等）
6. 若使用短信通知，则手机号码从今日校园直接获得
7. 至于部署服务器使用，由于腾讯阿里大部分IP均被今日校园封禁，需要使用到代理，需要各位各显神通了。
8. 催报任务仅限信息收集、签到。由于签到任务万年不变写的比较死，信息收集部分各位可以根据自身需求更改通知方式
9. QQ邮箱通知内容加上通知者名称不易被识别为垃圾邮件。
10. python index.py         enjoy it！
