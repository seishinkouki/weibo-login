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
    b = seed
    c = b[0:len(b) - 3]
    d = len(c)
    e = b[-2]
    f = b[-3]
    g = (f if a < 0 else "")
    a = abs(a)

    h = int(a / d)
    i = [a % d]
    while h > 0:
        g += e
        i.append(h % d)
        h = int(h / d)

    j = len(i) - 1
    while j >= 0:
        # g += 0 == j ? c.charAt(i[j]) : c.charAt(i[j] - 1)
        # g += c[i[j]]
        # g += c[i[j]-1]
        g += (c[i[j]] if j == 0 else c[i[j] - 1])
        j -= 1
    # g = f + g
    return g


# print numberTransfer(1538840053066)


def arrayTransfer(a):
    b = [a[0]]
    for c in range(0, len(a) - 1):
        d = []
        for e in range(0, len(a[c])):
            d.append(a[c + 1][e] - a[c][e])
            # print d
        b.append(d)
    return b


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


# test = [[30, 30, 1538844400022], [30, 30, 60], [30, 30, 153253]]
# print arrayTransfer(test)
# print pathEncode(test)
# K((|K((|!!!!!!@F8aiU0^!!!!!!@F8aiT5!!P8g
# K((|K((|!!!!!!@F8aiU0^!!!!!!@F8aiT5!!P8g
# file = open('1.gif', 'wb')
# file.write(imgdata)
# file.close()

# a = 255
# b = ord("V")
# print a&b
# b = 12
# c = 19
# print 16 >> 4
# print chr((b << 2 | (48 & c) >> 4))
# d = 60
# print chr(((15 & c) << 4 | (60 & d) >> 2))


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
    l = []
    m = {}
    n = 0

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


# print pathEncode('24', '3434cf7d036cc21db95c97da5378dabc46a5378dabc4')

s = [["7", "e", "5", "6"],
     ["8", "c", "d", "a"],
     ["0", "3", "9", "4"],
     ["1", "2", "b", "f"]]


def base64decode(imgdata_1):
    asciilist = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T',
                 'U', 'V',
                 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p',
                 'q', 'r',
                 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/',
                 '=']
    h = ''
    i = 0
    while True:
        b = asciilist.index(imgdata_1[i])
        i += 1
        c = asciilist.index(imgdata_1[i])
        i += 1
        h += chr((b << 2 | (48 & c) >> 4))
        # print 1, (b << 2 | (48 & c) >> 4), chr((b << 2 | (48 & c) >> 4))
        if imgdata_1[i] != '=':
            d = asciilist.index(imgdata_1[i])
            i += 1
        h += chr((15 & c) << 4 | (60 & d) >> 2)
        # print 2, ((15 & c) << 4 | (60 & ifequal) >> 2), chr((15 & c) << 4 | (60 & ifequal) >> 2)

        if '=' not in imgdata_1[i]:
            e = asciilist.index(imgdata_1[i])
            i += 1
        # print 3, ((3 & ifequal) << 6 | ifunderline), chr((3 & ifequal) << 6 | ifunderline)

        if i > len(imgdata_1) or imgdata_1[i] == '=':
            break
        h += chr((3 & d) << 6 | e)
    h = h.split('_')
    del h[0]
    del h[0]
    return h


def recombinePattern(img_data):
    img_data0 = img_data.split(',')[1].split('|')[0]
    img_data1 = img_data.split(',')[1].split('|')[1]

    file = open('original.png', 'wb')
    file.write(base64.b64decode(img_data0))
    file.close()

    img = Image.open("original.png")
    for y in range(0, 5):
        for x in range(1, 6):
            # print (32 * (x - 1), 32 * y, 32 * x, 32 * (y + 1))
            combine = img.crop((32 * (x - 1), 32 * y, 32 * x, 32 * (y + 1)))
            combine.save(str(x + 5 * y) + ".png")
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
    url = "https://captcha.weibo.com/api/pattern/get?ver=daf139fb2696a4540b298756bd06266a&source=ssologin&usrname=949164753@qq.com&line=160&side=100&radius=30&_rnd=" + str(
        sign) + "&callback=pl_cb"
    r = requests.get(url)
    imgdata = json.loads(r.text.replace("pl_cb(", '').replace(")", ''))['path_enc']
    id = json.loads(r.text.replace("pl_cb(", '').replace(")", ''))['id']
    recombinePattern(imgdata)
    data_enc = pathdataEncode(path_generate(patterntohash()))
    path_enc = pathEncode(patterntohash(), id)

    url2 = "https://captcha.weibo.com/api/pattern/verify?ver=daf139fb2696a4540b298756bd06266a&id=" + id + "&usrname=949164753@qq.com&source=ssologin&path_enc=" + path_enc + "&data_enc=" + data_enc + "&callback=pl_cb"
    url3 = 'https://passport.weibo.cn/sso/login'
    session = requests.Session()
    # 验证验证码
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
