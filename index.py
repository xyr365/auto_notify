#coding=utf-8
import yaml
import requests
import json
import random
import time
import random
import datetime
from urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
def getYmlConfig(yaml_file='config.yml'):
    file = open(yaml_file, 'r', encoding="utf-8")
    file_data = file.read()
    file.close()
    config = yaml.load(file_data, Loader=yaml.FullLoader)
    return dict(config)

def main():
    print("#############################################################################################\n")
    global config, wqd, wtb, qdyc, qdycmd, tbyc, tbycmd, wqdmd, wtbmd, grdx, tjjg, jcjg,total,ycmdhz
    grdx = []
    ycmdhz = []
    wqd = 0; wtb = 0; qdyc = 0; tbyc = 0;total = 0
    qdycmd = ''; tbycmd = ''; wqdmd = ''; wtbmd = ''; tjjg = ''; jcjg = ''
    config = getYmlConfig('config.yml')
    getList(6)
    getList()
    #统计结果qq私聊处理
    wqdm = f'==》未签到 {wqd} 人：\n   {wqdmd[:-1]}'
    wtbm = f'==》未填表 {wtb} 人：\n   {wtbmd[:-1]}'
    if wqd == 0 : wqdm = '每日签到、健康监测已全部完成！'
    if total == 0 : wtbm = '信息收集已全部完成！'
    sqmsg = f'{wqdm}\n\n{wtbm}\n\n{tjjg}\n\n{jcjg}'
    print("※========》汇总消息如下《========※\n\n", sqmsg + "\n\n#########################################################\n")
        #sendQmsgChan(config['resultqq'], sqmsg, config['resultqqtype'])
    #短信发送处理
    print("是否使用邮箱通知： 【1】是   【其他任意值】否\n")
    if input('输入你的选择并回车：')=="1":
        for gp in config['groups'] :
            print("即将进行未填提醒本次通知有",len(grdx),"人")
            for i in range(0, len(grdx)) :
                if gp['group'].get('major') != None :
                    if gp['group'].get('major') == grdx[i]['major'] :
                        mbnr = [grdx[i]['name'], grdx[i]['task']]
                        if grdx[i]['qq'] != "":
                            sendqqemail(grdx[i]['name'],grdx[i]['qqemail'], grdx[i]['task'],"未填任务列表")
                        else:
                            print(grdx[i]['name'],"这位无QQ使用短信通知")
                        continue
                else :
                    mbnr = [grdx[i]['name'], grdx[i]['task']]
                    if grdx[i]['qq'] != "":
                        sendqqemail(grdx[i]['name'],grdx[i]['qqemail'], grdx[i]['task'],"未填任务列表")
                    else:
                        print(grdx[i]['name'],"这位无QQ使用短信通知")
            print("完成未填邮箱通知，即将进行异常通知")
            print("即将进行异常提醒本次通知有",len(ycmdhz),"人")
            for i in range(0, len(ycmdhz)) :
                if gp['group'].get('major') != None :
                    if gp['group'].get('major') == ycmdhz[i]['major'] :
                        mbnr = [ycmdhz[i]['name'], ycmdhz[i]['task']]
                        if ycmdhz[i]['qq'] != "":
                            sendqqemail(ycmdhz[i]['name'],ycmdhz[i]['qqemail'], ycmdhz[i]['task'],"填表异常提醒")
                        else:
                            print(ycmdhz[i]['name'],"这位无QQ使用短信通知")

                        continue
                else :
                    mbnr = [ycmdhz[i]['name'], ycmdhz[i]['task']]
                    if ycmdhz[i]['qq'] != "":
                        sendqqemail(ycmdhz[i]['name'],ycmdhz[i]['qqemail'], ycmdhz[i]['task'],"填表异常提醒")
                    else:
                        print(ycmdhz[i]['name'],"这位无QQ使用短信通知")

        print("完成邮箱通知")
    else:
        print("\n==》您选择不进行邮箱通知\n")
    print("是否使用QQ私聊通知： 【1】是   【其他任意值】否\n")
    if input('输入你的选择并回车：')=="1":
        for gp in config['groups'] :
            for i in range(0, len(grdx)) :
                if gp['group'].get('major') != None :
                    if gp['group'].get('major') == grdx[i]['major'] :
                        sendQQ(grdx[i]['qq'],grdx[i]['name'],grdx[i]['task'])
                        continue
                else :
                    sendQQ(grdx[i]['qq'],grdx[i]['name'],grdx[i]['task'])
        for i in range(0, len(ycmdhz)) :
            if gp['group'].get('major') != None :
                if gp['group'].get('major') == ycmdhz[i]['major'] :
                    if ycmdhz[i]['qq'] != "":
                        sendQQ2(ycmdhz[i]['qq'],"name",ycmdhz[i]['task']+"填写异常，请核查。")
                    else:
                        print(ycmdhz[i]['name'],"这个B无QQ")
                    continue
            else :
                if ycmdhz[i]['qq'] != "":
                    sendQQ2(ycmdhz[i]['qq'],"name",ycmdhz[i]['task']+"填写异常，请核查。")
                else:
                    print(ycmdhz[i]['name'],"这个B无QQ")
        print("完成QQ私聊通知")
        input('')
    else:
        print("\n==》您选择不进行QQ私聊，程序结束\n")
        input('')
        exit()


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
            if title.rfind("摸排"):
                rw = title
            else:
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
    print((qmsg))
    #if group['group'].get('useQmsg') != None and group['group'].get('useQmsg'):
     #   sendQmsgChan(group['group'].get('qq'), qmsg, group['group']['qqtype'])
      #  time.sleep(6)
def getList(moduleCode = 4):
    global wqd, wqdmd, wtb, wtbmd, qdyc, qdycmd, tbyc, tbycmd, tjjg, mdc, jcjg,total
    mdc = moduleCode
    MOD = config["Cookie"]
    headers = {
        'Host' : f'{config["SchoolHost"]}',
        'Accept' : 'application/json, text/plain, */*',
        'X-Requested-With' : 'XMLHttpRequest',
        'Accept-Language' : 'zh-CN,zh-Hans;q=0.9',
        'Content-Type' : 'application/json;charset=utf-8',
        'Origin' : f'https://{config["SchoolHost"]}',
        'User-Agent' : 'Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 (4708773888)cpdaily/9.0.8  wisedu/9.0.8',
        'Cookie' : MOD
    }
    #moduleCode：4表示信息收集，6表示签到
    data ='{"pageNumber":1,"pageSize":20,"moduleCode":"' + str(moduleCode) + '","creatorWid":"","signType":"","sortColumn":"","content":""}'
    url = f'https://{config["SchoolHost"]}/wec-counselor-apps/counselor/homepage/getFollowsInProgress'
    res = requests.post(url, data=data, headers=headers, verify=False)
    resj = json.loads(res.text)
    wid = 0
    with open(config['studentjsonfile'], 'r') as cs:
        csj = json.load(cs)
    if len(resj) != 0 and resj['datas']['totalSize'] != 0 :
        for i in range(0, resj['datas']['totalSize']) :
            wid = resj['datas']['rows'][i]['pcUrl']
            tbycmdsigle=""
            #print(resj['datas']['rows'][i]['endTime'])
            #continue
            wid = wid.split('/')[5] #url可能会发生变动，后续可能需要进一步进行准确判断
            #wid = '106981'
            title = resj['datas']['rows'][i]['content']
            mon = datetime.datetime.now().timetuple().tm_mon
            day = datetime.datetime.now().timetuple().tm_mday
            et = datetime.datetime.now().today().strftime("%m-%d")
            if title.rfind(config["signkeyword"]) >= 0: 
                    print(title, '截止时间：', resj['datas']['rows'][i]['endTime'],"不在筛选范围内","\n")
                    print('#############################################################################################\n')
                    continue
            #et = f'{mon}-{day}'
            print("=》任务名称：",title, '\n=》截止时间：', resj['datas']['rows'][i]['endTime'])
            if resj['datas']['rows'][i]['progressBarPercent'] ==0:
                print(title, '截止时间：', resj['datas']['rows'][i]['endTime'],"任务未发布","\n")
                continue
            if config['Judgmentdate'] :
                if resj['datas']['rows'][i]['endTime'].rfind(et) == -1 :
                    print('#############################################################################################\n')
                    continue
            abnr = [] #注意测试变量初始化
            jcabnr = [] #注意测试变量初始化
            if moduleCode == 6:
                data = '{"pageSize":1,"pageNumber":1,"taskWid":"' + str(wid) + '"}'
                url = f'{config["SchoolHost"]}/wec-counselor-sign-apps/sign/counselor/querySignTaskDayStatistic'
                res0 = requests.post(url, data = data, headers = headers, verify = False).json()
                twid = res0['datas']['rows'][0]['signInstanceWid']
                data = '{"pageNumber":1,"pageSize":1000,"signStatus":2,"sortColumn":"userId asc","cls":"","clsName":"","grade":"","dept":"","deptName":"","major":"","isLate":"-1","majorName":"","qrcodeUserWid":"-1","hasChangeLog":"","isMalposition":"-1","extraFieldItemVos":[],"taskWid":"' + wid + '","taskInstanceWid":"' + twid + '"}'
                url = f'{config["SchoolHost"]}/wec-counselor-sign-apps/sign/counselor/querySingleSignList'
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
                                name = jcycres['datas']['rows'][jci]['name']
                                tel = jcycres['datas']['rows'][jci]['mobile']
                                rw = title
                                major = jcycres['datas']['rows'][jci]['major']
                                for j in range(0, len(csj)) :
                                    if csj[j]['userId'] == jcycres['datas']['rows'][jci]['userId'] :
                                        qq = csj[j]['qq']
                                        qqemail=qq+"@qq.com"
                                        break
                                    elif j == len(csj)-1 :#-1，否则只能匹配到名单内
                                        qq = ""
                                        qqemail=""
                                ycmd = {}
                                ycmd = {'name':name, 'tel':tel, 'task':rw, 'major':major, 'qqemail':qqemail, 'qq':qq}
                                ycmdhz.append(ycmd)
                                jcabnr.append(jcycres['datas']['rows'][jci]['name'])
                jcabnr = list(set(jcabnr))
                for yci in range(0, len(jcabnr)) :
                    qdycmd = qdycmd + jcabnr[yci] + '，'
                qdyc = len(jcabnr)
                if res1['datas']['totalSize'] != 0 :
                    for group in config['groups'] :
                        qmsg = "{title}，已签到 {snum} 人，未签到 {unum} 人：\n".format(title = title, snum = res1['datas']['signedNum'], unum = res1['datas']['unsignedNum'])
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
                #print(resj)
                #exit()
                if title.rfind(config["keyword1"]) == -1 and title.rfind(config["keyword2"])== -1: 
                    print(title, '截止时间：', resj['datas']['rows'][i]['endTime'],"不在筛选范围内","\n")
                    print('#############################################################################################\n')
                    continue #标题判断任务，如果匹配不到，则跳过此条数据
                #if title.rfind("config['keyword']") == -1 : 
                 #   print(title, '截止时间：', resj['datas']['rows'][i]['endTime'],"不在筛选范围内","\n")
                  #  print('#############################################################################################\n')
                   # continue #标题判断任务，如果匹配不到，则跳过此条数据
                #新加参数instanceWid
                insurl = f'{config["SchoolHost"]}/wec-counselor-collector-apps/collector/notice/detailCollector'
                insdata = '{"wid":"' + wid + '"}'
                insres = requests.post(insurl, headers = headers, data = insdata, verify = False).json()
                inswid = insres['datas']['rows'][0]['instanceWid']
                if inswid == None :
                    inswid = ''
                #这里是为填表，应该
                #data = '{"wid":"' + wid + '","isHandled":0,"isRead":-1,"content":"","pageNumber":1,"pageSize":1000}'
                data = '{"isRead":"-1","sortColumn":"userId asc","isHandled":"0","wid":"' + wid + '","instanceWid":"' + inswid + '","content":"","pageNumber":1,"pageSize":1000}'
                url = f'{config["SchoolHost"]}/wec-counselor-collector-apps/collector/notice/queryAllTarget'
                res = requests.post(url, headers = headers, data = data, verify = False).json()
                #这里是已填写异常处理
                data = '{"pageNumber":1,"pageSize":100,"wid":"' + wid + '","instanceWid":"' + inswid + '","photoPageSize":6,"textPageSize":10,"numberPageSize":100}' 
                url = f'{config["SchoolHost"]}/wec-counselor-collector-apps/collector/statistics/getStatisticsByCollectorWid'
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
                            if inswid == "" :
                                inswid = 'null'
                            #print(cont)
                            #continue
                            data = '{"fieldWid":"' + fwid + '","value":"' + cont + '","searchContent":"","collectorWid":"' + wid + '","isSchoolTask": "false","pageNumber":1,"pageSize":1000,"instanceWid":'+ inswid +'}' 
                            data = data.encode("utf-8").decode("latin1")
                            url = f'{config["SchoolHost"]}/wec-counselor-collector-apps/collector/statistics/getDetailByValue'
                            res2 = requests.post(url, data = data, headers = headers, verify = False).json()
                            #continue
                            #f#or n in res['datas']['rows'] :#range(0, res2['datas']['totalSize']) :
                               # abname = n['name']#res2['datas']['rows'][n]['name']
                            for n in range(0, res2['datas']['totalSize']) :
                                abname = res2['datas']['rows'][n]['name']
                                name = res2['datas']['rows'][n]['name']
                                tel = res2['datas']['rows'][n]['mobile']
                                rw = title
                                major = res2['datas']['rows'][n]['major']
                                for j in range(0, len(csj)) :
                                    if csj[j]['userId'] == res2['datas']['rows'][n]['userId'] :
                                        qq = csj[j]['qq']
                                        qqemail=qq+"@qq.com"
                                        break
                                    elif j == len(csj)-1 :#-1，否则只能匹配到名单内
                                        qq = ""
                                        qqemail=""
                                ycmd = {}
                                ycmd = {'name':name, 'tel':tel, 'task':rw, 'major':major, 'qqemail':qqemail, 'qq':qq}
                                ycmdhz.append(ycmd)
                                abnr.append(abname)
                    big = 0
                    tmp = 0
                abnr = list(set(abnr))
                for p in range(0, len(abnr)) :
                    tbycmd = tbycmd + abnr[p] + '，'
                    tbycmdsigle=tbycmdsigle+abnr[p] + '，'
                tbyc = len(abnr)+tbyc
                qmsg = "该任务，已提交 {tnum} 人，未提交 {unum} 人：\n".format(title = title, tnum = res['datas']['handledSize'], unum = res['datas']['unHandledSize'])
                wtb = res['datas']['unHandledSize']+wtb
                if wtb != 0 :
                    total = 1
                if res['datas']['totalSize'] != 0 :
                    for group in config['groups'] :
                        prsList(res, title, qmsg, group)
                else :
                    print(f'{title}已全部提交！\n')
                if len(abnr) != 0 :
                    tjjg = f"填表异常 {tbyc} 人：{tbycmd[:-1]}"
                    print(f"=====》》该任务 {len(abnr)} 人填表异常：{tbycmdsigle[:-1]}\n")
                else :
                    print("=====》》该任务没有出现异常情况！\n")
                if tbyc == 0:
                    tjjg = "信息收集没有出现异常情况！"
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
def sendqqemail(name,qqemail,task,type):
    json={
    "mailto": qqemail,
    "mialsub": "今日校园提醒",
    "mailbody": f"<h1>{type}：</h1>{task}\n\n\n\n\n\n\n\n\n\n<h2>福州大学是国家“双一流”建设高校、国家“211工程”重点建设大学、福建省人民政府与国家教育部共建高校。学校创建于1958年，现已发展成为一所以工为主、理工结合，理、工、经、管、文、法、艺等多学科协调发展的重点大学。</h2>"
    }
    url="微软邮箱接口"
    #微软邮箱接口
    res = requests.post(url, json=json, verify = False)
    if res.status_code==200:
        print("==>》",name,"通知成功")
    else:
        print("==>》",name,"邮箱通知失败,请检查该邮箱是否收录入cs.text")
def sendQQ(qq,name,title):
    messagei = ["给你讲个笑话：\nKnock，Knock……\n—————— 填今日校园","填个今日校园吧，如果填好的话，留你一命。","看你骨骼精奇。有气冲破天灵，定是练武奇才，我就卖你本《今日校园填报指南》。只收你10块钱!","还不填？所以爱会消失的对吗？","我最讨厌跟我说对不起的人，有本事就填今日校园啊。",f"{name}，你又在玩电动噢，休息一下吧，去填个今日校园好不好","填今日校园你不要，钱你也不要，你要什么啊。","武林中有两招绝学，一阳指和狮吼功，我用了整整三十年的时间，将两招并成了一整招。——填今日校园呀！","阿Sir，你没填今日校园已经很久了……","我们是在不断地被否定中成长的，甚至有时候就会相信那些在脑袋里面，说你没填今日校园的那些人，那些声音是真的。","我也诚心的相信，解决你最好的方法是填今日校园。","走人生的路就像爬山一样，看起来走了许多冤枉的路，崎岖的路，但最终都要填今日校园。","如果做人没有填今日校园，那跟咸鱼有什么分别？","你真正是谁并不重要，重要的是你没填今日校园。","“你知道什么样的病人最难痊愈吗？”\n“没有病识感的病人。”\n他们明明生病了，却不觉得自己有病。他们明明可能错了，却坚信自己对。\n同理。\n你知道什么样的人最讨厌吗？\n没有意识到到自己没填今日校园的人。","为什么是你\n可能，因为你没填今日校园吧"]
    rmessage = random.choice(messagei)
    print(f'正在通过QQ私聊{qq},{name}')
    url = f"http://127.0.0.1:5700/send_private_msg?user_id={qq}&message={rmessage}"
    url2 = f"http://127.0.0.1:5700/send_private_msg?user_id={qq}&message={title}"
    res = requests.post(url2,verify = False)
    time.sleep(0.5)
    res = requests.post(url,verify = False)
    print(res.text)
    time.sleep(0.5)
def sendQQ2(qq,name,title):
    print(f'正在通过QQ私聊{qq},{name}')
    url2 = f"http://127.0.0.1:5700/send_private_msg?user_id={qq}&message={title}"
    res = requests.post(url2,verify = False)
    print(res.text)
    time.sleep(0.5)

# 阿里云的入口函数
def handler(event, context):
    main()

# 腾讯云的入口函数
def main_handler(event, context):
    main()
    return 'ok'

if __name__ == '__main__':
    main()