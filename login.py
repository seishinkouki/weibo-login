# coding=utf-8
import base64
import json
import random
import time
from PIL import Image
import cStringIO
import requests

seed = "()*,-./0123456789:?@ABCDEFGHIJKLMNOPQRSTUVWXYZ_abcdefghijklmnop~$^!|"


def numberTransfer(a):
    c = seed[0:len(seed) - 3]
    d = len(c)
    e = seed[-2]
    f = seed[-3]
    g = (f if a < 0 else "")
    a = abs(a)

    h = a / d
    i = [a % d]
    while h > 0:
        g += e
        i.append(h % d)
        h = h / d

    j = len(i) - 1
    while j >= 0:
        g += (c[i[j]] if j == 0 else c[i[j] - 1])
        j -= 1
    # g = f + g
    return g


def arrayTransfer(a):
    b = [a[0]]
    for c in range(0, len(a) - 1):
        d = []
        for e in range(0, len(a[c])):
            d.append(a[c + 1][e] - a[c][e])
            # print d
        b.append(d)
    return b


# 对生成的手势数据进行加密
def pathdataEncode(a):
    b = seed[-1]

    c = arrayTransfer(a)
    # print c
    d = ""
    e = ""
    f = ""

    for g in range(0, len(c)):
        # print g
        d += numberTransfer(c[g][0])
        e += numberTransfer(c[g][1])
        f += numberTransfer(c[g][2])
    return d + b + e + b + f


# 对验证码的滑动顺序(例如"1234")进行加密
def pathEncode(path, id):
    e = [0, 0]
    c = len(id) - 2
    for f in range(0, 2):
        g = id[c:][f]
        e[f] = (ord(g) - 87 if ord(g) > 57 else ord(g) - 48)
    # return e
    d = c * e[0] + e[1]
    r = int(path) + d
    k = [20, 50, 200, 500]
    l = [[], [], [], []]
    idd = list(set(id[:c]))
    idd.sort(key=id.index)
    j = 0
    for i in idd:
        l[j % 4].append(i)
        j += 1
    # return l

    t = 3
    s = ""
    while r > 0 and t >= 0:
        if r - k[t] >= 0:
            q = int(random.random() * len(l[t]))
            s += l[t][q]
            r -= k[t]
        else:
            t -= 1

    return s


# 解密base64中图片顺序信息
def base64decode(imgdata_1):
    asciilist = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="
    h = ''
    i = 0
    while True:
        b = asciilist.index(imgdata_1[i])
        i += 1
        c = asciilist.index(imgdata_1[i])
        i += 1
        h += chr((b << 2 | (48 & c) >> 4))
        if imgdata_1[i] != '=':
            d = asciilist.index(imgdata_1[i])
            i += 1
        h += chr((15 & c) << 4 | (60 & d) >> 2)

        if '=' not in imgdata_1[i]:
            e = asciilist.index(imgdata_1[i])
            i += 1
        if i > len(imgdata_1) or imgdata_1[i] == '=':
            break
        h += chr((3 & d) << 6 | e)
    h = h.split('_')
    del h[0]
    del h[0]
    return h


def recombinePattern(img_data):
    # 返回的图片base64由两部分组成, 前面是打乱的图片,后面是打乱图片正确组合的次序
    img_data0 = img_data.split(',')[1].split('|')[0]
    img_data1 = img_data.split(',')[1].split('|')[1]

    file = open('original.png', 'wb')
    file.write(base64.b64decode(img_data0))
    file.close()
    # 分割打乱的图片
    img = Image.open("original.png")
    for y in range(0, 5):
        for x in range(1, 6):
            combine = img.crop((32 * (x - 1), 32 * y, 32 * x, 32 * (y + 1)))
            combine.save(str(x + 5 * y) + ".png")
    # 重新组合图片
    outImage = Image.new('RGBA', (160, 160))
    noo = 0
    for i in base64decode(img_data1):
        no = int(i)

        # print no
        fromImge = Image.open(str(no + 1) + ".png")
        # loc = ((i % 2) * 200, (int(i/2) * 200))
        loc = (((noo % 5) * 32), (int(noo / 5)) * 32)
        # print noo
        noo += 1
        # print(loc)
        outImage.paste(fromImge, loc)

    outImage = outImage.convert('L')
    # outImage = outImage.resize((64, 64), Image.ANTIALIAS)
    outImage.save('merged.png')
    # print type(outImage)
    buffer = cStringIO.StringIO()
    outImage.save(buffer, format="png")
    img_base64 = base64.b64encode(buffer.getvalue())
    return img_base64


# 通过截取特定的小区域与预先处理的24种情形对比来识别验证码
def patterntohash():
    abc = {1: [27, 78, 32, 83],
           2: [78, 127, 83, 132],
           3: [127, 78, 132, 83],
           4: [78, 27, 83, 32]}
    p_pattern = []
    for i in range(1, 5):
        L = Image.open('merged.png')
        L = L.crop((abc[i][0], abc[i][1], abc[i][2], abc[i][3])).convert('L')
        pix = L.load()
        for ii in range(0, 5):
            for jj in range(0, 5):
                g_pix = pix[jj, ii]
                p_pattern.append(g_pix)
    # print aaa
    # print xxx
    with open('p_pattern.txt', 'r') as fp:
        data = fp.read()
        data = eval(data)
        fp.close()
    for key in data:
        sum = 0
        for arr in range(0, 100):
            sum += abs(data[key][arr] - p_pattern[arr])
        if sum < 100:
            return key


# 生成随机的滑动路径数据
def path_generate(a):
    pos = {'1': [32, 32],
           '2': [128, 32],
           '3': [32, 128],
           '4': [128, 128]}
    path = []
    t0 = (int(round(time.time() * 1000)))
    t00 = 0
    for j in range(0, 3):
        for i in range(0, 7):
            x = pos[a[j]][0] + i * (pos[a[j + 1]][0] - pos[a[j]][0]) / 6 + int(random.uniform(1, 3))

            y = pos[a[j]][1] + i * (pos[a[j + 1]][1] - pos[a[j]][1]) / 6 + int(random.uniform(2, 3))

            t = 30 * int(random.uniform(1, 2))
            t00 += t

            path0 = [x, y, t00]
            path.append(path0)
    path[0][2] = t0
    # print path
    return path


headers2 = {'Accept': '*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Connection': 'keep-alive',
            'Content-Length': '152',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': '',
            'Host': 'passport.weibo.cnn',
            'Referer': 'https://passport.weibo.cn/signin/login?display=0&retcode=6102',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.104 Safari/537.36 Core/1.53.3427.400 QQBrowser/9.6.12513.400'}

headers3 = {
    'Host': 'passport.weibo.cn',
    'Connection': 'keep-alive',
    'Content-Length': '206',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Origin': 'https://passport.weibo.cn',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': '*/*',
    'Referer': 'https://passport.weibo.cn/signin/login',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,zh-TW;q=0.7',
    'Cookie': ''}


def getcookies(user, passwd):
    # 获取验证码
    sign = random.random()
    url = "https://captcha.weibo.com/api/pattern/get?ver=daf139fb2696a4540b298756bd06266a&source=ssologin&usrname=" + user + "&line=160&side=100&radius=30&_rnd=" + str(
        sign) + "&callback=pl_cb"
    r = requests.get(url)
    imgdata = json.loads(r.text.replace("pl_cb(", '').replace(")", ''))['path_enc']
    id = json.loads(r.text.replace("pl_cb(", '').replace(")", ''))['id']
    recombinePattern(imgdata)
    data_enc = pathdataEncode(path_generate(patterntohash()))
    path_enc = pathEncode(patterntohash(), id)

    url2 = "https://captcha.weibo.com/api/pattern/verify?ver=daf139fb2696a4540b298756bd06266a&id=" + id + "&usrname=" + user + "&source=ssologin&path_enc=" + path_enc + "&data_enc=" + data_enc + "&callback=pl_cb"
    url3 = 'https://passport.weibo.cn/sso/login'
    # 必要的等待时间
    time.sleep(1)
    # 验证验证码
    session = requests.Session()
    r2 = session.get(url2)
    # print r2.headers
    print json.loads(r2.text.replace("pl_cb(", '').replace(")", ''))['msg']
    # print id

    formdata = {'username': user,
                'password': passwd,
                'savestate': '1',
                'ec': '0',
                'entry': 'mweibo',
                'mainpageflag': '1',
                'vid': id,
                'wentry': '',
                'loginfrom': '',
                'client_id': '',
                'code:qq': '',
                'r': '',
                'pagerefer': '',
                'hff': '',
                'hfp': ''}

    # print formdata['vid']
    # 登录
    r3 = session.post(url3, data=formdata, headers=headers3)
    cookies_url = r3.headers['Set-Cookie']
    print json.loads(r3.content)['msg']
    return {k.split('=')[0]: k.split('=')[1] for k in cookies_url.split(';')}

    # r4 = requests.get('https://m.weibo.cn/')
    # print r4.headers['Set-Cookie']


user = ''
passwd = ''
print getcookies(user, passwd)
