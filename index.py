#coding=utf-8
import yaml
import requests
import json
import random
import time
import random
import datetime
from todayLoginService import TodayLoginService
from actions.autoSign import AutoSign
from tencentcloud.common import credential
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.sms.v20210111 import sms_client, models
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile

def getYmlConfig(yaml_file='config.yml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)

def main():
    # timeNow = datetime.datetime.now()
    # # 当前日期
    # today = timeNow.strftime('%Y%m%d%H%M%S')
    # # 昨天
    # yesterday = (timeNow - datetime.timedelta(days=1)).strftime('%Y%m%d%H%M%S')
    # # 二十天前
    # twentyDaysAgo = (timeNow - datetime.timedelta(days=20)).strftime('%Y%m%d%H%M%S')
    # print(datetime.timedelta())
    # exit()
    print("#############################################################################################\n")
    global config, wqd, wtb, qdyc, qdycmd, tbyc, tbycmd, wqdmd, wtbmd, grdx, tjjg, jcjg,total
    grdx = []
    wqd = 0; wtb = 0; qdyc = 0; tbyc = 0;total = 0
    qdycmd = ''; tbycmd = ''; wqdmd = ''; wtbmd = ''; tjjg = ''; jcjg = ''
    config = getYmlConfig('xcfg.yml')
    cfg = getYmlConfig()
    for user in cfg['users'] :
        getList(user, 6)
        getList(user)
        #统计结果短信提醒
        #if config.get('resultel') != None :
         #   ntime = time.strftime("%H:%M", time.localtime())
          #  mbp = [ntime, str(wqd), str(qdyc), str(qdycmd[:-1]), str(wtb), str(tbyc), str(tbycmd[:-1])]
           # sendSms(config.get('resultel'), "1077300", mbp)
        #统计结果qq私聊处理        
        wqdm = f'未签到{wqd}人：{wqdmd[:-1]}'
        wtbm = f'未填表{wtb}人：{wtbmd[:-1]}'
        if wqd == 0 : wqdm = '每日签到、健康监测已全部完成！'
        if total == 0 : wtbm = '信息收集已全部完成！'
        sqmsg = f'统计结果：\n\n{wqdm}\n\n{wtbm}\n\n{tjjg}\n\n{jcjg}'
        print("汇总消息如下：\n\n", sqmsg + "\n\n#########################################################\n")
            #sendQmsgChan(config['resultqq'], sqmsg, config['resultqqtype'])
        #邮箱、QQ提醒发送处理 可自行修改为sms短信
        print("是否对上述对象使用邮箱通知： 【1】是   【其他任意值】否\n")
        if input('输入你的选择并回车：')=="1":
            for gp in config['groups'] :
                for i in range(0, len(grdx)) :
                    if gp['group'].get('major') != None :
                        if gp['group'].get('major') == grdx[i]['major'] :
                            sendqqemail(grdx[i]['name'],grdx[i]['qqemail'], grdx[i]['task'])
                            continue
                    else :
                        sendqqemail(grdx[i]['name'],grdx[i]['qqemail'], grdx[i]['task'])
            print("完成邮箱通知")
        else:
            print("\n==》您选择不进行邮箱通知\n")
        print("是否对上述对象使用QQ私聊通知： 【1】是   【其他任意值】否\n")
        if input('输入你的选择并回车：')=="1":
            for gp in config['groups'] :
                for i in range(0, len(grdx)) :
                    if gp['group'].get('major') != None :
                        if gp['group'].get('major') == grdx[i]['major'] :
                            sendQQ(grdx[i]['qq'],grdx[i]['name'],grdx[i]['task'])
                            continue
                    else :
                        sendQQ(grdx[i]['qq'],grdx[i]['name'],grdx[i]['task'])
            print("完成QQ私聊通知")
            input('')
        else:
            print("\n==》您选择不进行QQ私聊，程序结束\n")
            input('')
            exit()
def getMOD(sign):
    headers = sign.session.headers
    headers['Content-Type'] = 'application/json'
    url = f'{sign.host}wec-counselor-sign-apps/stu/sign/getStuSignInfosInOneDay'
    res = sign.session.post(url, headers=headers, data=json.dumps({}), verify=False, allow_redirects=False)
    i = 0
    while str(res.headers.get('Set-Cookie')).rfind('MOD_AUTH_CAS') == -1 :
        res = sign.session.get(res.headers["location"], headers=headers, verify=False, allow_redirects=False)
        i += 1
        if i > 6 :
            print("重定向次数异常")
            exit()
    return res.headers["Set-Cookie"]

def prsList(list, title, qmsg, group):
    global mdc, wqdmd, wtbmd, grdx, qq
    with open(config['studentjsonfile'], 'r') as cs:
        csj = json.load(cs)
    for k in range(0, list['datas']['totalSize']):
        major = list['datas']['rows'][k]['major']
        Major = group['group'].get('major')
        if Major != None and Major != major:
            continue
        name = list['datas']['rows'][k]['name']
        num = list['datas']['rows'][k]['userId']
        tel = list['datas']['rows'][k]['mobile']
        for j in range(0, len(csj)) :
            if csj[j]['userId'] == num :
                qq = csj[j]['qq']
                qqemail=qq+"@qq.com"
                break
            elif j == len(csj)-1 :#-1，否则只能匹配到名单内
                qq = ""
                qqemail=""
        if mdc == 4 :
            wtbmd = wtbmd + name + '，'
        else :
            wqdmd = wqdmd + name + '，'
        lsgrdx = {}
        rw = ''
        if mdc == 4 :
            rw = title
        else :
            rw = title
        lsgrdx = {'name':name, 'tel':tel, 'task':rw, 'major':major, 'qqemail':qqemail, 'qq':qq}
        add = 0
        for dh in grdx :
            add = 0
            if dh['tel'] == tel :
                dh['task'] = dh['task'] + ', ' + rw
                add = 1
                break
        if add == 0 : grdx.append(lsgrdx)
        for j in range(0, len(csj)) :
            if csj[j]['userId'] == num :
                qmsg = "{qmsg}    {name}(1)QQ={qq}\n".format(qmsg = qmsg, name = name, qq = csj[j]['qq'])
                break
            elif j == len(csj)-1 :#-1，否则只能匹配到名单内
                qmsg = "{qmsg}    {name}(0)\n".format(qmsg = qmsg, name = name)
    if Major != None :
        print("——专业筛选：",Major)
    print(title, "\n",(qmsg))
    #if group['group'].get('useQmsg') != None and group['group'].get('useQmsg'):
     #   sendQmsgChan(group['group'].get('qq'), qmsg, group['group']['qqtype'])
      #  time.sleep(6)

def getList(user, moduleCode = 4):
    global wqd, wqdmd, wtb, wtbmd, qdyc, qdycmd, tbyc, tbycmd, tjjg, mdc, jcjg,total
    mdc = moduleCode
    today = TodayLoginService(user['user'])
    today.login()
    sign = AutoSign(today, user['user'])
    MOD = getMOD(sign)
    headers = {
        'Host' : 'fzu.campusphere.net',
        'Accept' : 'application/json, text/plain, */*',
        'X-Requested-With' : 'XMLHttpRequest',
        'Accept-Language' : 'zh-CN,zh-Hans;q=0.9',
        'Content-Type' : 'application/json;charset=utf-8',
        'Origin' : 'https://fzu.campusphere.net',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (4708773888)cpdaily/9.0.8  wisedu/9.0.8',
        'Cookie' : MOD
    }
    #moduleCode：4表示信息收集，6表示签到
    data ='{"pageNumber":1,"pageSize":20,"moduleCode":"' + str(moduleCode) + '","creatorWid":"","signType":"","sortColumn":"","content":""}'
    url = f'{sign.host}wec-counselor-apps/counselor/homepage/getFollowsInProgress'
    res = requests.post(url, data=data, headers=headers, verify=False)
    resj = json.loads(res.text)
    wid = 0
    if len(resj) != 0 and resj['datas']['totalSize'] != 0 :
        for i in range(0, resj['datas']['totalSize']) :
            wid = resj['datas']['rows'][i]['pcUrl']
            #print(resj['datas']['rows'][i]['endTime'])
            #continue
            wid = wid.split('/')[5] #url可能会发生变动，后续可能需要进一步进行准确判断
            #wid = '106981'
            title = resj['datas']['rows'][i]['content']
            mon = datetime.datetime.now().timetuple().tm_mon
            day = datetime.datetime.now().timetuple().tm_mday
            md = f'{mon}月{day}日'
            et = datetime.datetime.now().today().strftime("%m-%d")
            #et = f'{mon}-{day}'
            if config['Judgmentdate'] :
                if resj['datas']['rows'][i]['endTime'].rfind(et) == -1 :
                    print(title, '截止时间：', resj['datas']['rows'][i]['endTime'],"\n")
                    print('#############################################################################################\n')
                    continue
            abnr = [] #注意测试变量初始化
            jcabnr = [] #注意测试变量初始化
            if moduleCode == config['sign']:
                data = '{"pageSize":1,"pageNumber":1,"taskWid":"' + str(wid) + '"}'
                url = f'{sign.host}wec-counselor-sign-apps/sign/counselor/querySignTaskDayStatistic'
                res0 = requests.post(url, data = data, headers = headers, verify = False).json()
                twid = res0['datas']['rows'][0]['signInstanceWid']
                data = '{"pageNumber":1,"pageSize":1000,"signStatus":2,"sortColumn":"userId asc","cls":"","clsName":"","grade":"","dept":"","deptName":"","major":"","isLate":"-1","majorName":"","qrcodeUserWid":"-1","hasChangeLog":"","isMalposition":"-1","extraFieldItemVos":[],"taskWid":"' + wid + '","taskInstanceWid":"' + twid + '"}'
                url = f'{sign.host}wec-counselor-sign-apps/sign/counselor/querySingleSignList'
                res1 = requests.post(url, data = data, headers = headers, verify = False).json()
                wqd += res1['datas']['unsignedNum']
                data1 = '{"pageNumber":1,"pageSize":500,"signStatus":1,"sortColumn":"userId asc","extraFieldItemVos":[{"wid":32161,"title":"午检体温 (必填)","description":"请如实填报","hasOtherItems":0,"extraFieldItem":"大于等于37.3度","extraFieldItemWid":73584,"isExtraFieldOtherItem":0,"fieldIndex":0}],"isLate":"-1","hasChangeLog":"","isMalposition":"-1","cls":"","clsName":"","dept":"","deptName":"","major":"","majorName":"","grade":"","qrcodeUserWid":"-1","taskWid":"' + wid + '","taskInstanceWid":"' + twid + '"}' 
                data1 = data1.encode("utf-8").decode("latin1")
                data2 = '{"pageNumber":1,"pageSize":20,"signStatus":1,"sortColumn":"userId asc","extraFieldItemVos":[{"wid":32162,"title":"是否有发热、咳嗽、乏力、呼吸困难等疑似症状(必填)","description":"请如实填报","hasOtherItems":0,"extraFieldItems":[{"content":"否","wid":73585,"isOtherItems":0,"isSelected":null,"isAbnormal":false},{"content":"是","wid":73586,"isOtherItems":0,"isSelected":null,"isAbnormal":true}],"extraFieldItem":"是","extraFieldItemWid":73586,"isExtraFieldOtherItem":0,"fieldIndex":1}],"isLate":"-1","hasChangeLog":"","isMalposition":"-1","cls":"","clsName":"","dept":"","deptName":"","major":"","majorName":"","grade":"","qrcodeUserWid":"-1","taskWid":"' + wid + '","taskInstanceWid":"' + twid + '"}' 
                data2 = data2.encode("utf-8").decode("latin1")
                Data = [data1, data2]
                url = 'https://fzu.campusphere.net/wec-counselor-sign-apps/sign/counselor/querySingleSignList'
                #jcabnr = [] #变量初始化移动到上层，注意测试
                if title.rfind('监测') != -1 :
                    for dti in range(0, len(Data)) :
                        jcycres = requests.post(url, data = Data[dti], headers = headers, verify = False).json()
                        if jcycres['datas']['totalSize'] != 0 :
                            for jci in range(0, jcycres['datas']['totalSize']) :
                                jcabnr.append(jcycres['datas']['rows'][jci]['name'])
                jcabnr = list(set(jcabnr))
                for yci in range(0, len(jcabnr)) :
                    qdycmd = qdycmd + jcabnr[yci] + '，'
                qdyc = len(jcabnr)
                if res1['datas']['totalSize'] != 0 :
                    for group in config['groups'] :
                        qmsg = "{title}，已签到{snum}人，未签到{unum}人：\n".format(title = title, snum = res1['datas']['signedNum'], unum = res1['datas']['unsignedNum'])
                        prsList(res1, title, qmsg, group)
                else :
                    print(title + '已全部完成！\n')
                if qdyc != 0 and title.rfind('监测') != -1 :
                    jcjg = f"{title}{len(jcabnr)}人异常：{qdycmd[:-1]}"
                    print(f"=====》》{title}{len(jcabnr)}人异常：{qdycmd[:-1]}\n")
                elif title.rfind('监测') != -1 :
                    jcjg = f"{title}没有出现异常情况！"
                    print(f"=====》》{title}没有出现异常情况！\n")
            elif moduleCode == 4 :
                # print(resj)
                # exit()
                if title.rfind(config['keyword']) == -1 : 
                    print(title, '截止时间：', resj['datas']['rows'][i]['endTime'],"不在筛选范围内","\n")
                    print('#############################################################################################\n')
                    continue #标题判断任务，如果匹配不到，则跳过此条数据
                data = '{"wid":"' + wid + '","isHandled":0,"isRead":-1,"content":"","pageNumber":1,"pageSize":1000}'
                url = f'{sign.host}wec-counselor-collector-apps/collector/notice/queryAllTarget'
                res = requests.post(url, headers = headers, data = data, verify = False).json()
                data = '{"pageNumber":1,"pageSize":10,"wid":"' + wid + '","photoPageSize":6,"textPageSize":10,"numberPageSize":10}' 
                url = f'{sign.host}wec-counselor-collector-apps/collector/statistics/getStatisticsByCollectorWid'
                res1 = requests.post(url, headers = headers, data = data, verify = False).json()
                tmp = 0
                big = 0
                # abnr = [] #变量初始化移动到上层，注意测试
                # 类型值输出
                # #取消以下代码注释以进行测试
                # for ft in res1['datas']['rows'] :
                #     print(ft['fieldType'])
                #     continue
                # exit()
                # #取消以上代码注释以进行测试
                for l in range(0, res1['datas']['totalSize']) :
                    if res1['datas']['rows'][l]['fieldType'] != 2 :
                        continue
                    xx = res1['datas']['rows'][l]['choiceTypeStatisticsList']
                    qtitle = res1['datas']['rows'][l]['title']
                    for mm in xx :
                        if mm['count'] != 0 :
                            tmp = mm['count']
                            if tmp > big :
                                big = tmp
                    for m in xx :
                        if m['count'] != 0 and m['count'] < big :
                            fwid = res1['datas']['rows'][l]['fieldWid']
                            cont = m.get('content')
                            #print(cont)
                            #continue
                            data = '{"fieldWid":"' + fwid + '","value":"' + cont + '","searchContent":"","collectorWid":"' + wid + '","isSchoolTask": "false","pageNumber":1,"pageSize":10}' 
                            data = data.encode("utf-8").decode("latin1")
                            url = f'{sign.host}wec-counselor-collector-apps/collector/statistics/getDetailByValue'
                            res2 = requests.post(url, data = data, headers = headers, verify = False).json()
                            #print(res2)
                            #continue
                            #f#or n in res['datas']['rows'] :#range(0, res2['datas']['totalSize']) :
                               # abname = n['name']#res2['datas']['rows'][n]['name']
                            for n in range(0, res2['datas']['totalSize']) :
                                abname = res2['datas']['rows'][n]['name']
                                abnr.append(abname)
                    big = 0
                    tmp = 0
                abnr = list(set(abnr))
                for p in range(0, len(abnr)) :
                    tbycmd = tbycmd + abnr[p] + '，'
                tbyc = len(abnr)+tbyc

                qmsg = "该任务，已提交{tnum}人，未提交{unum}人：\n".format(title = title, tnum = res['datas']['handledSize'], unum = res['datas']['unHandledSize'])
                wtb = res['datas']['unHandledSize']+wtb
                if wtb != 0 :
                    total = 1
                if res['datas']['totalSize'] != 0 :
                    for group in config['groups'] :
                        prsList(res, title, qmsg, group)
                else :
                    print(f'{title}已全部提交！\n')
                if len(abnr) != 0 :
                    tjjg = f"填表异常{tbyc}人：{tbycmd[:-1]}"
                    print(f"=====》》该任务{len(abnr)}人填表异常：{tbycmd[:-1]}\n")
                else :
                    tjjg = "信息收集没有出现异常情况！"
                    print("=====》》该任务没有出现异常情况！\n")
                # elif i == resj['datas']['totalSize']-1 :
            print('#############################################################################################\n')
    else :
        print("任务为空！\n")

def sendQmsgChan(qq, msg, type = 0):
    ttype = ['发送群消息到', '私聊']
    mtype = ['group', 'send']
    print(f'正在通过Qmsg酱{ttype[type]}{qq}')
    data={
        "msg" : str(msg),
        "qq" : str(qq)
    }
    url = f"https://qmsg.zendee.cn:443/{mtype[type]}/{config['QmsgKey']}"
    res = requests.post(url, data=data, verify = False)
    print(res.text)
    ##邮箱模块
def sendqqemail(name,qqemail,task):
    json={
    "mailto": qqemail,
    "mialsub": "今日校园未填提醒",
    "mailbody": f"<h1>任务列表：</h1>{task}"
    }
    url=config['emailurl']
    res = requests.post(url, json=json, verify = False)
    if res.status_code==200:
        print("==>》",name,"通知成功")
    else:
        print("==>》",name,"邮箱通知失败,请检查该邮箱是否收录入cs.text")
def sendQQ(qq,name,title):
    ##qq私聊内容  自行修改
    messagei = ["给你讲个笑话：\nKnock，Knock……\n—————— 填今日校园","看你骨骼精奇。有气冲破天灵，定是练武奇才，我就卖你本《今日校园填报指南》。只收你10块钱!","说你填今日校园又不听，听又不懂，懂又不做，做你又做错，错又不认，认又不改，改你又不服，不服你又不说，要我怎么办？","我房间里有有一些好康的(今日校园)，比游戏还刺激，还能教你登dua郎。要不要填一填？",f"{name}，你又在玩电动噢，休息一下吧，去填个今日校园好不好","填今日校园你不要，钱你也不要，你要什么啊。","武林中有两招绝学，一阳指和狮吼功，我用了整整三十年的时间，将两招并成了一整招。——填今日校园呀！","阿Sir，你没填今日校园已经很久了……","我：靓仔,今天是你还没填今日校园吧？\n你：今日什么？\n我：今日校园\n你：什么校园啊？\n我：今日校园啊！\n你：今日什么啊？\n我：行，靓仔你先凉快吧。","想当年我手拿着两把西瓜刀从南天门砍到蓬莱东路，砍了三天三夜眼睛都没眨一下。\n——三天三夜，你不没填今日校园吗？","走人生的路就像爬山一样，看起来走了许多冤枉的路，崎岖的路，但最终都要填今日校园。","如果做人没有填今日校园，那跟咸鱼有什么分别？","你真正是谁并不重要，重要的是你没填今日校园。",]
    rmessage = random.choice(messagei)
    print(f'正在通过QQ私聊{qq},{name}')
    url = f"http://127.0.0.1:5700/send_private_msg?user_id={qq}&message={rmessage}"
    url2 = f"http://127.0.0.1:5700/send_private_msg?user_id={qq}&message={title}"
    res = requests.post(url2,verify = False)
    time.sleep(0.5)
    res = requests.post(url,verify = False)
    print(res.text)
    time.sleep(0.5)
##########################################################
##以下为腾讯云的短信通知模块自行探索修改（50元1000条） 一般修改必填项即可
##########################################################
def sendSms(telnumber, templateid, templateparamset) :
    print('\n正在发送短信到', telnumber)
    try:
        secretId = '' ##API访问密钥（必填）
        secretKey = ''##API访问密钥（必填）
        cred = credential.Credential(secretId, secretKey)
        httpProfile = HttpProfile()
        httpProfile.reqMethod = "POST"  # post请求(默认为post请求)
        httpProfile.reqTimeout = 30    # 请求超时时间，单位为秒(默认60秒)
        httpProfile.endpoint = "sms.tencentcloudapi.com"  # 指定接入地域域名(默认就近接入)
        clientProfile = ClientProfile()
        clientProfile.signMethod = "TC3-HMAC-SHA256"  # 指定签名算法
        clientProfile.language = "en-US"
        clientProfile.httpProfile = httpProfile
        client = sms_client.SmsClient(cred, "ap-guangzhou", clientProfile)
        req = models.SendSmsRequest()
        req.SmsSdkAppId = "1111111111"     ##应用ID（必填）
        req.SignName = "****公众号"  ##签名名称  例："昔日校园"（必填）
        req.ExtendCode = ""
        req.SessionContext = "xxx"##上下这3个不清楚  不修改就行
        req.SenderId = ""
        req.PhoneNumberSet = [telnumber]#["+8613024111111"]
        req.TemplateId = templateid#"1071476"
        req.TemplateParamSet = templateparamset#["1", "abc", '2', 'qwe', '3', 'asd', '4', 'zxc']
        resp = client.SendSms(req)
        print("短信发送结果：", resp, "\n")
    except TencentCloudSDKException as err:
        print("短信接口错误信息：\n", err, "\n")

# 阿里云的入口函数
def handler(event, context):
    main()

# 腾讯云的入口函数
def main_handler(event, context):
    main()
    return 'ok'

if __name__ == '__main__':
    main()