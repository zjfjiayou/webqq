# -*- coding: utf-8 -*-
#import urllib.parse, urllib.request, http.cookiejar, hashlib, re, json
import urllib, urllib2, hashlib, re, json, cookielib

"""cookie"""
#cookie=http.cookiejar.CookieJar()
#chandle=urllib.request.HTTPCookieProcessor(cookie)

cookie = cookielib.CookieJar()
chandle = urllib2.HTTPCookieProcessor(cookie)

def get(url):
    #r = urllib.request.Request(url)
    r = urllib2.Request(url)
    #opener = urllib.request.build_opener(chandle)
    opener = urllib2.build_opener(chandle)
    u = opener.open(r)
    data = u.read()
    try:
        data = data.decode('utf-8')
    except:
        data = data.decode('gbk', 'ignore')
    return data

def post(url, data):
    #data = urllib.parse.urlencode(data)
    data = urllib.urlencode(data)
    
    #data = bytes(data,'utf-8')
    data = data.decode('utf-8')
    #r = urllib.request.Request(url,data)
    r = urllib2.Request(url, data)
    #opener = urllib.request.build_opener(chandle)
    opener = urllib2.build_opener(chandle)
    u = opener.open(r)
    data = u.read()
    try:
        data = data.decode('utf-8')
    except:
        data = data.decode('gbk', 'ignore')
    return data

def to_bytes(n, length, endianess = 'big'):
    h = '%x' % n
    s = ('0' * (len(h) % 2) + h).zfill(length * 2).decode('hex')
    return s if endianess == 'big' else s[::-1]

class QQ:
    num = ""
    pwd = ""
    login_sig = ""
    appid = 549000912
    qzreferrer = ""

    def __init__(self, num, pwd):
        self.num = num
        self.pwd = pwd
        self.check()
        self.login()

    def check(self):
        par = {
            'appid'                : self.appid,
            'daid'                : 5,
            'hide_title_bar'    : 1,
            'link_target'        : "blank",
            'low_login'            : 0,
            'no_verifyimg'        : 1,
            'proxy_url'            : "http://qzs.qq.com/qzone/v6/portal/proxy.html",
            'pt_qr_app'            : "手机QQ空间",
            'pt_qr_help_link'    : "http://z.qzone.com/download.html",
            'pt_qr_link'        : "http://z.qzone.com/download.html",
            'pt_qzone_sig'        : 1,
            'qlogin_auto_login'    : 1,
            's_url'                : "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            'self_regurl'        : "http://qzs.qq.com/qzone/v6/reg/index.html",
            'style'                : 22,
            'target'            : "self"
        }
        url = "http://xui.ptlogin2.qq.com/cgi-bin/xlogin?%s" % urllib.urlencode(par)#urllib.parse.urlencode(par)
        self.login_sig = re.findall('login_sig:"([^"]+)"', get(url))[0]
        par = {
            'appid'                : self.appid,
            'js_type'            : 1,
            'js_ver'            : 10076,
            'login_sig'            : self.login_sig,
            'r'                    : 0.8861454421075537,
            'regmaster'            : "",
            'u1'                : "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            'uin'                : self.num
        }
        url = 'http://check.ptlogin2.qq.com/check?%s' % urllib.urlencode(par)#urllib.parse.urlencode(par)
        _, self.vcode, self.uin = re.findall("'([^']+)'", get(url))


    def getPwd(self):
        str2 = hashlib.md5(self.pwd.encode())
        str2 = str2.digest()
        str2 = hashlib.md5((str2 + to_bytes(int(self.num), 8, "big")))#.to_bytes(8, "big")))
        str2 = str2.hexdigest().upper()
        str2 = hashlib.md5((str2 + self.vcode.upper()).encode())
        return str2.hexdigest().upper()


    def login(self):
        par = {
            'action'            : "5-20-1314",
            'aid'                : self.appid,
            'daid'                : 5,
            'from_ui'            : 1,
            'g'                    : 1,
            'h'                    : 1,
            'js_type'            : 1,
            'js_ver'            : 10076,
            'login_sig'            : self.login_sig,
            'p'                    : self.getPwd(),
            'pt_qzone_sig'        : 1,
            'pt_rsa'            : 0,
            'ptlang'            : 2052,
            'ptredirect'        : 0,
            't'                    : 1,
            'u'                    : self.num,
            'u1'                : "http://qzs.qq.com/qzone/v5/loginsucc.html?para=izone",
            'verifycode'        : self.vcode
        }

        url = "http://ptlogin2.qq.com/login?%s" % urllib.urlencode(par)#urllib.parse.urlencode(par)
        # get(url)
        li = re.findall("'([^']+)'", get(url))

        if not int(li[0]):
            self.qzreferrer = li[2]
            print(u"你好，%s" % li[len(li) - 1])
            return True
        else:
            return False


    def gtk(self):
        for x in cookie:
            if x.name == "skey":
                hash = 5381;
                for c in x.value:
                    hash += (hash << 5) + ord(c)
                return hash & 0x7fffffff;


    def feed(self, txt, pic = False):
        url = "http://taotao.qq.com/cgi-bin/emotion_cgi_publish_v6?g_tk=%d" % self.gtk()
        par = {
            'code_version'        : 1,
            'con'                : txt,
            'feedversion'        : 1,
            'format'            : "fs",
            'hostuin'            : self.num,
            'paramstr'            : 1,
            'pic_template'        : "",
            'qzreferrer'        : self.qzreferrer,
            'richtype'            : "",
            'richval'            : "",
            'special_url'        : "",
            'subrichtype'        : "",
            'syn_tweet_verson'    : 1,
            'to_sign'            : 0,
            'to_tweet'            : 0,
            'ugc_right'            : 1,
            'ver'                : 1,
            'who'                : 1
        }
        if not int(re.findall('"subcode":([\d\-]+)', post(url, par))[0]):
            return True
        else:
            return False

qq = QQ("****", "****")
qq.feed("I'm Spider-Man测试")
