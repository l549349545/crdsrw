# 爬一哈每日大使任务 
import requests
import re
import json
from lxml import etree
import time
import os
import datetime

# 推送配置1 
corpid = os.environ["CORPID"]
agentid = os.environ["AGENTID"]
corpsecret = os.environ["CORPSECRET"]
pushusr = os.environ["PUSHUSR"]
img_url = os.environ["IMG_URL"]
coolpushurl = os.environ["COOLPUSHURL"]

# 源URL配置
url = 'https://cn.wowhead.com/'

# 名称字典
d = {'Rare Resources': "稀有资源：从暗影界的稀有怪物和宝箱中收集3枚掮客硬币"}
d.update({'Challenges in Maldraxxus': '玛卓克萨斯的挑战：击败玛卓克萨斯的强力劲敌'})
d.update({'A Call to Ardenweald': '炽蓝仙野的召唤：进度条儿'})
d.update({'Storm the Maw': '突袭噬渊：在噬渊消灭3个稀有或者特殊首领'})
d.update({'Training in Revendreth': '雷文德斯训练：与你的学徒在雷文德斯完成3个世界任务'})
d.update({'A Call to Maldraxxus': '玛卓克萨斯的召唤：进度条儿'})
d.update({'Aiding Ardenweald': '协助炽蓝仙野：在炽蓝仙野完成3个世界任务'})
d.update({'A Call to Revendreth': '雷文德斯的召唤:进度条儿'})
d.update({'Anima Salvage': '心能回收：从托加斯特，罪魂之塔收集150个心能余烬'})
d.update({'Aiding Maldraxxus': '协助玛卓克萨斯：在玛卓克萨斯完成3个世界任务'})
d.update({'A Calling in Bastion': '使命：晋升堡垒：在晋升堡垒完成3个世界任务'})
d.update({'A Call to Bastion': '晋升堡垒的召唤:进度条儿'})
d.update({'Aiding Bastion': '协助晋升堡垒：在晋升堡垒完成3个世界任务'})
d.update({'Troubles at Home': '家园的麻烦:保卫晋升堡垒 进度条儿'})
d.update({'Challenges in Bastion': '晋升堡垒的挑战：击败晋升堡垒的强力劲敌'})
d.update({'Challenges in Ardenweald': '炽蓝仙野的挑战:击败炽蓝仙野的强力劲敌'})
d.update({'Training in Maldraxxus': '玛卓克萨斯训练：与你的学徒在玛卓克萨斯完成3个世界任务'})
d.update({'Challenges in Revendreth': '雷文德斯的挑战：击败雷文德斯的强力劲敌'})
d.update({'Training in Ardenweald': '炽蓝仙野训练：与你的学徒在炽蓝仙野完成3个世界任务'})
d.update({'Training Our Forces': '训练部队：与你的学徒在晋升堡垒完成3个世界任务'})
d.update({'Aiding Revendreth': '协助雷文德斯：在雷文德斯完成3个世界任务'})
d.update({'Anima Appeal': '心能出现：在晋升堡垒的极乐堡的心能储备中存放600份心能'})
d.update({'Gildenite Grab': '钽金抢夺：从晋升堡垒的稀有怪物和宝箱中收集3份钽金'})
d.update({'A Source of Sorrowvine': '哀藤之源：从雷文德斯的稀有怪物和宝箱中收集3根哀藤'})
d.update({'A Wealth of Wealdwood': '仙枝的财富：从炽蓝仙野的稀有怪物和宝箱中收集3根仙枝'})
d.update({'Bonemetal Bonanza': '富产髓钢：从玛卓克萨斯的稀有怪物和宝箱中收集3份髓钢'})
d.update({'Training in Bastion': '晋升堡垒训练：在晋升堡垒完成3个世界任务'})
d.update({'A Calling in Ardenweald': '使命：炽蓝仙野：在炽蓝仙野完成3个世界任务'})

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
        msg = data

    #企业微信推送
    msg = msg.replace('\n\n', '\n')
    push = WXPusher(pushusr,msg)
    push.send_message()

    #酷推推送
    requests.get(coolpushurl, params={"c": "不愿意透露姓名的好心人王富贵提供\n"+data})
    
    strBoss=strBoss + "\n更新时间(UTC):"+datetime.datetime.strftime(datetime.datetime.now() ,'%Y-%m-%d %H:%M:%S')
    strJc=strJc + "\n更新时间(UTC):"+datetime.datetime.strftime(datetime.datetime.now() ,'%Y-%m-%d %H:%M:%S')
    strZc=strZc + "\n更新时间(UTC):"+datetime.datetime.strftime(datetime.datetime.now() ,'%Y-%m-%d %H:%M:%S')    
    retmsg=data+ "更新时间(UTC):"+datetime.datetime.strftime(datetime.datetime.now() ,'%Y-%m-%d %H:%M:%S')
    strPt=strPt+ "\n更新时间(UTC):"+datetime.datetime.strftime(datetime.datetime.now() ,'%Y-%m-%d %H:%M:%S')
    
    model={"大使任务：\n"+retmsg,"世界BOSS：\n"+strBoss,"泊星剧场：\n"+strJc,"周常任务：\n"+strZc,"噬渊爬塔：\n"+strPt} #数据
    with open("./hmm.json",'w',encoding='utf-8') as json_file:
       json.dump(model,json_file,ensure_ascii=False, default=set_default)
    
    print(msg)
    return retmsg
 
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
        self.title = '不愿意透露姓名的好心人王富贵提供：'
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

# 本地运行用这个
run()
