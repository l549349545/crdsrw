# 爬一哈每日大使任务 
import requests
import re
import json
from lxml import etree
import time
import os
import datetime
from numpy import array
from dsConfig import d
from czConfig import cz

# 源URL配置
url = 'https://cn.wowhead.com/'

def set_default(obj):
    if isinstance(obj, set):
         return list(obj)
    raise TypeError

def run():
    try:
       r = requests.get(url, timeout=30)
       time.sleep(1)
       r.raise_for_status() #如果状态不是200，引发HTTPError异常#
       r.encoding = r.apparent_encoding
       #data = compile.findall(r.text)
       #data = r.text
       sel=etree.HTML(r.text)    
       
       #获取全谱系驱魔师
       con=sel.xpath('normalize-space(//div[@id="EU-group-familyExorcist"])')
       strQtx = ''
       for i in con:
        strQtx += i
       strQtx = strQtx +"\n\n"
       con=sel.xpath('normalize-space(//div[@id="EU-group-familiar"])')
       for i in con:
        strQtx += i
       strQtx = strQtx +"\n\n"
       con=sel.xpath('normalize-space(//div[@id="EU-group-menagerie"])')
       for i in con:
        strQtx += i
        
       #获取执事者金色宝箱
       con=sel.xpath('normalize-space(//div[@id="EU-group-steward-of-the-day"])')
       strJsbx = ''
       for i in con:
        strJsbx += i
        
       #获取噬渊狩猎小队
       con=sel.xpath('normalize-space(//div[@id="EU-group-beastwarrens-hunts-line-0"])')
       strSlxd = ''
       for i in con:
        strSlxd += i
        
       #获取镜子
       con=sel.xpath('normalize-space(//div[@id="EU-group-venthyr-broken-mirrors"])')
       strJz = ''
       for i in con:
        strJz += i
        
       #获取世界事件
       con=sel.xpath('normalize-space(//div[@id="EU-group-holiday"])')
       strSjsj = ''
       for i in con:
        strSjsj += i
        
       #获取名望上限
       con=sel.xpath('normalize-space(//div[@id="EU-group-renown"])')
       strMwsx = ''
       for i in con:
        strMwsx += i

       #获取勇气上限
       con=sel.xpath('normalize-space(//div[@id="EU-group-valor"])')
       strYqsx = ''
       for i in con:
        strYqsx += i

        #获取词缀
       zspp = ((datetime.datetime.now()+ datetime.timedelta(hours=104)).isocalendar()[1] % 12) + 3 #周数取12余+2       
       if (zspp == 9):
           zspp_next='A'
       elif (zspp == 10):
           zspp='A' 
           zspp_next='B'
       elif zspp == 11: 
           zspp='B' 
           zspp_next='C'
       elif zspp == 12:
           zspp='C' 
           zspp_next='1'
       else:
           zspp_next = zspp + 1
       strCzinfo = "本周："+str(zspp)+"\n下周："+str(zspp_next)

       for key in cz:
        strCzinfo = strCzinfo.replace(key, cz[key])

       #获取世界BOSS
       con=sel.xpath('normalize-space(//div[@id="EU-group-epiceliteworldsl"])')
       strBoss = ''
       for i in con:
        strBoss += i
        
       #获取本周爬塔
       con=sel.xpath('normalize-space(//div[@id="EU-group-torghast-wings"])')
       strPt = ''
       for i in con:
        strPt += i
        
       #获取剧场
       con=sel.xpath('normalize-space(//div[@id="EU-group-star-lake-amphitheater"])')
       strJc = ''
       for i in con:
        strJc += i
        
       #获取突袭
       #con=sel.xpath('//*[@id="main-contents"]/div[6]/div/div/div[7]/div[35]')
       strTx = ''
       #for i in con:
        #strTx += i
        
       #获取周长
       con=sel.xpath('normalize-space(//div[@id="EU-group-weekly-quest-sl"])')
       strZc = ''
       for i in con:
        strZc += i

       #获取大使任务
       con=sel.xpath('normalize-space(//div[@id="EU-group-calling-quests"])')
       string = ''
       for i in con:
        string += i

       string = string.replace(";", ";\n")
       string = re.sub("\".*\"",'',string)
       string = re.sub("\(.*\);",'',string)
       string = string.replace("\n })", "")
       string = string.replace("使命任务 ", "使命任务\n")
       string = re.sub("\(.*\);",'',string)

       if "分钟" in string:
           strHour = '1'
       else:
           strHour = re.findall('\d{1,2}小时', string)[0]
       sTime = int(re.findall('\d{1,2}', strHour)[0])
       sTime = sTime + 16
       string = re.sub("\d{1,2}小时",str(sTime)+"小时",string)   
       string = re.sub("\d{1,2}分钟",str(sTime)+"小时",string)   
       sTime = sTime + 24
       string = string.replace("1天", str(sTime) + "小时") 
       sTime = sTime + 24
       if sTime > 80 :
        string = string.replace("2天", "(明日大使)" + str(sTime) + "小时") 
       else: 
        string = string.replace("2天", "(今日可接)" + str(sTime) + "小时") 

       string = string.replace("\n ", "\n")
       for key in d:
        string = string.replace(key, d[key])

       data = string
    except Exception as err:
        msg = '发生错误',err
    else:
        msg = data + "\n\n突袭：" + strTx +"\n\n剧场："+strJc  +"\n\n温西尔镜子："+strJz +"\n\n执事者金色宝箱："+strJsbx +"\n\n"+strQtx

    msg = msg.replace('\n\n', '\n')
    
    #保存本地json    
    current_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')   
    retmsg=data+ "更新时间(UTC+8):"+current_time
    strBoss=strBoss + "\n更新时间(UTC+8):"+current_time
    strJc=strJc + "\n更新时间(UTC+8):"+current_time
    strZc=strZc + "\n更新时间(UTC+8):"+current_time    
    strPt=strPt+ "\n更新时间(UTC+8):"+current_time 
    strQtx=strQtx+ "\n更新时间(UTC+8):"+current_time 
    strJsbx=strJsbx+ "\n更新时间(UTC+8):"+current_time 
    strSlxd=strSlxd+ "\n更新时间(UTC+8):"+current_time 
    strJz=strJz+ "\n更新时间(UTC+8):"+current_time 
    strSjsj=strSjsj+ "\n更新时间(UTC+8):"+current_time 
    strMwsx=strMwsx+ "\n更新时间(UTC+8):"+current_time 
    strYqsx=strYqsx+ "\n更新时间(UTC+8):"+current_time 
    strCzinfo=strCzinfo+ "\n更新时间(UTC+8):"+current_time
    strTx=strTx+ "\n更新时间(UTC+8):"+current_time
        
    model = {'DSRW':"大使任务：\n"+retmsg,
             'SJBS':"世界BOSS(明日)：\n"+strBoss,
             'BXJC':"泊星剧场(明日)：\n"+strJc,
             'ZCRW':"周常任务(明日)：\n"+strZc,
             'SYPT':"噬渊爬塔(明日)：\n"+strPt,
             'QPXQMS':"全谱系驱魔师(明日)：\n"+strQtx,
             'ZSZJSBX':"执事者金色宝箱(明日)：\n"+strJsbx,
             'SYSLXD':"噬渊狩猎小队(明日)：\n"+strSlxd,
             'WXEJZ':"温西尔镜子(明日)：\n"+strJz,
             'SJSJ':"世界事件(明日)：\n"+strSjsj,
             'MWSX':"名望上限(明日)：\n"+strMwsx,
             'YQSX':"勇气上限(明日)：\n"+strYqsx,
             'DMJCZ':"大秘境词缀：\n"+strCzinfo,
             'SYTX':"噬渊突袭(明日)：\n"+strTx}
    with open("./hmm.json",'w',encoding='utf-8') as json_file:
       json.dump(model,json_file,ensure_ascii=False, default=set_default)
    
    return msg
 
def main_handler(event, context):
    return run()

# 本地运行用这个,也用于Cron任务触发
run()
