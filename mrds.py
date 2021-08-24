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

# 推送配置1 
corpid = os.environ["CORPID"]
agentid = os.environ["AGENTID"]
corpsecret = os.environ["CORPSECRET"]
pushusr = os.environ["PUSHUSR"]
img_url = os.environ["IMG_URL"]
coolpushurl = os.environ["COOLPUSHURL"]

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
       con=sel.xpath('normalize-space(//div[@id="EU-group-beastwarrens-hunts"])')
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
       zspp = ((datetime.datetime.now()+ datetime.timedelta(hours=104)).isocalendar()[1] % 12) + 3 #周数取12余+3

       if (zspp>12): 
           zspp = zspp - 12             
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
        msg = data +"\n\n剧场："+strJc  +"\n\n镜子："+strJz +"\n\n执事者金色宝箱："+strJsbx +"\n\n"+strQtx

    #企业微信推送
    current_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')   
    msg = msg.replace('\n\n', '\n')
    push = WXPusher(pushusr,msg)
    push.send_message()

    #POST发布文章
    conurl = "http://baimiao.work/action/import"
    conttext="大使任务：\n"+data +"\n\n\n\n世界BOSS(明日)：\n"+strBoss +"\n\n\n\n泊星剧场(明日)：\n"+strJc+"\n\n\n\n周常任务(明日)：\n"+strZc+"\n\n\n\n噬渊爬塔(明日)：\n"+ strPt+"\n\n\n\n全谱系驱魔师(明日)：\n"+strQtx+"\n\n\n\n执事者金色宝箱(明日)：\n"+strJsbx+"\n\n\n\n噬渊狩猎小队(明日)：\n"+strSlxd+"\n\n\n\n温西尔镜子(明日)：\n"+strJz+"\n\n\n\n世界事件(明日)：\n"+strSjsj+"\n\n\n\n名望上限(明日)：\n"+strMwsx+"\n\n\n\n勇气上限(明日)：\n"+strYqsx+"\n\n\n\n大秘境词缀(明日)：\n"+strCzinfo;
    contdata = {"title":"大使任务 更新时间(UTC+8):"+current_time,"text":conttext,"key":"ob7hww6fs2e4xo9lltzewcpok5","mid":array([6])}
    requests.post(url=conurl,data=contdata)
    
    print(conttext)
    return true
 
def main_handler(event, context):
    return run()

# 企业微信推送
class WXPusher:
    def __init__(self, usr=None, desp=None):
        self.base_url = 'https://qyapi.weixin.qq.com/cgi-bin/gettoken?'
        self.req_url = 'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token='
        self.media_url = 'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={access_token}&type=file'
        self.corpid = corpid     # 填写企业ID
        self.corpsecret = corpsecret     # 应用Secret
        self.agentid = int(agentid)          # 填写应用ID，是个整型常数,就是应用AgentId
        self.img_url = img_url
        if usr is None:
            usr = '@all'
        self.title = '白描描描描描描描描描描提供：'
        self.usr = usr
        self.msg = desp

    def get_access_token(self):
        urls = self.base_url + 'corpid=' + self.corpid + '&corpsecret=' + self.corpsecret
        resp = requests.get(urls).json()
        access_token = resp['access_token']
        return access_token

    #上传临时素材,返回素材id
    def get_ShortTimeMedia(self):
        url = self.media_url
        ask_url = url.format(access_token = self.get_access_token())
        f = requests.get(self.img_url).content
        r = requests.post(ask_url,files={'file':f},json=True)
        return json.loads(r.text)['media_id']

    def send_message(self):
        data = self.get_message()
        req_urls = self.req_url + self.get_access_token()
        res = requests.post(url=req_urls, data=data)
        print(res.text)

    def get_message(self):
        data = {
            "touser": self.usr,
            "toparty": "@all",
            "totag": "@all",
            "msgtype": "news",
            "agentid": self.agentid,
            "news" : {
              "articles" : [{
                   "title" : self.title,
                   "description" : self.msg,
                   "url" : "",
                   "picurl" : self.img_url
                }]
            },
            "safe":0,
            "enable_id_trans": 0,
            "enable_duplicate_check": 0,
            "duplicate_check_interval": 1800
        }
        data = json.dumps(data)
        return data

# 本地运行用这个,也用于Cron任务触发
run()
