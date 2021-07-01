# 爬一哈每日大使任务 
import requests
import re
import json
from lxml import etree
import time
import os
import datetime
from numpy import array

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
d.update({'A Calling in Maldraxxus': '使命：玛卓克萨斯：在玛卓克萨斯完成3个世界任务'})
d.update({'A Calling in Revendreth': '使命：雷文德斯：在雷文德斯完成3个世界任务'})


cz = {'1': "强韧、崩裂、火山"}
cz.update({'2': '残暴、怨毒、重伤'})
cz.update({'3': '强韧、激励、风雷'})
cz.update({'4': '残暴、鼓舞、死疽'})
cz.update({'5': '强韧、血池、震荡'})
cz.update({'6': '残暴、暴怒、易爆'})
cz.update({'7': '强韧、怨毒、火山'})
cz.update({'8': '残暴、激励、死疽'})
cz.update({'9': '强韧、鼓舞、风雷'})
cz.update({'10': '残暴、崩裂、易爆'})
cz.update({'11': '强韧、血池、重伤'})
cz.update({'12': '残暴、暴怒、震荡'})

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
       zspp = (datetime.datetime.now()+ datetime.timedelta(hours=24)).isocalendar()[1] % 12 + 4 #周数取12余+4
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
        msg = data +"\n\n剧场："+strJc  +"\n\n镜子："+strJz +"\n\n执事者金色宝箱："+strJsbx +"\n\n全谱系驱魔师："+strQtx

    #企业微信推送
    msg = msg.replace('\n\n', '\n')
    push = WXPusher(pushusr,msg)
    push.send_message()

    #酷推推送
    current_time = (datetime.datetime.now() + datetime.timedelta(hours=8)).strftime('%Y-%m-%d %H:%M:%S')   
    requests.get(coolpushurl, params={"c": "机器人查询指令：大使、世界BOSS、剧场、周常、爬塔、全谱系、金色宝箱、狩猎小队、镜子、世界事件、名望、勇气、词缀\n"+data+"\n网站查看：http://baimiao.work"+"\n"+current_time})

    #POST发布文章
    conurl = "http://baimiao.work/action/import"
    conttext="大使任务：\n"+data +"\n\n\n\n世界BOSS(明日)：\n"+strBoss +"\n\n\n\n泊星剧场(明日)：\n"+strJc+"\n\n\n\n周常任务(明日)：\n"+strZc+"\n\n\n\n噬渊爬塔(明日)：\n"+ strPt+"\n\n\n\n全谱系驱魔师(明日)：\n"+strQtx+"\n\n\n\n执事者金色宝箱(明日)：\n"+strJsbx+"\n\n\n\n噬渊狩猎小队(明日)：\n"+strSlxd+"\n\n\n\n温西尔镜子(明日)：\n"+strJz+"\n\n\n\n世界事件(明日)：\n"+strSjsj+"\n\n\n\n名望上限(明日)：\n"+strMwsx+"\n\n\n\n勇气上限(明日)：\n"+strYqsx+"\n\n\n\n大秘境词缀(明日)：\n"+strCzinfo;
    contdata = {"title":"大使任务 更新时间(UTC+8):"+current_time,"text":conttext,"key":"ob7hww6fs2e4xo9lltzewcpok5","mid":array([6])}
    requests.post(url=conurl,data=contdata)
    
    #保存本地json    
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
             'DMJCZ':"大秘境词缀(明日)：\n"+strCzinfo}
    with open("./hmm.json",'w',encoding='utf-8') as json_file:
       json.dump(model,json_file,ensure_ascii=False, default=set_default)
    
    print(conttext)
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

# 本地运行用这个
run()
