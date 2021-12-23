import os
import requests
import tkinter as tk
import time
import re
import matplotlib.pyplot as mat
import jieba
import numpy as nu
import tkinter.messagebox

from tkinter import scrolledtext
from faker import Faker  # 虚拟用户的请求头防止被服务器拦截
from wordcloud import WordCloud
from PIL import Image, ImageTk
from bs4 import BeautifulSoup

titlelist = []
pagehreflist = []
timetitle = ''


def printcomment():
    for i in range(len(titlelist)):
        k = titlelist[i]
        j = pagehreflist[i]
        print(k)
        print(j)
    print(len(pagehreflist))
    print(len(titlelist))


def deleteRecord(showmysearchrecordcopy):
    confirm = tk.messagebox.askokcancel('提示', '执行此步后会永久删除数据，确认要执行？')
    if confirm:
        with open('record/SearchRecord/searchrecord.txt', mode='w+', encoding='utf-8') as f:
            f.truncate()
            f.write('梦开始的地方：')
        showmysearchrecordcopy.destroy()


def showSearchRecord(startwindowcopy):
    showmysearchrecord = tk.Toplevel(startwindowcopy)
    showmysearchrecord.geometry('550x550+400+50')
    showmysearchrecord.title('我的搜索记录')
    showmysearchrecord.resizable(width=False, height=False)

    title = tk.Label(showmysearchrecord, text='看看我曾都搜索到了些啥', font=("华文行楷", 20), fg="green")
    title.pack()

    # 在text下面创建一个frame区域来放横向滚动条
    framescrollbar = tk.Frame(showmysearchrecord, height=20, width=550)

    # 横向滚动条
    s2 = tk.Scrollbar(framescrollbar, orient='horizontal')

    text = scrolledtext.ScrolledText(showmysearchrecord, width=50, relief='groove', height=20,
                                     font=("隶书", 15), wrap='none',
                                     xscrollcommand=s2.set)
    s2.config(command=text.xview)
    text.pack()
    framescrollbar.pack()
    s2.pack(ipadx=230)

    delete = tk.Button(showmysearchrecord, text='删除历史记录', command=lambda: deleteRecord(showmysearchrecord), width=20)
    delete.pack(pady=20)

    # 读取文件内容到text区域内显示
    with open('record/SearchRecord/searchrecord.txt', mode='r', encoding='utf-8') as f:
        searchrecord = f.read()
    if len(searchrecord) <= 7:
        text.insert('insert', '您还没有获取过热点新闻哦！！')
        delete.config(state='disable')
    else:
        text.insert('insert', searchrecord)
    text.config(state='disable')


def showWordCloud():
    os.system('start' + '.\\record\\WordCloud')


def getTitleAndPagehref():
    url = 'https://www.zhihu.com/hot'
    html = getHTML(url)
    soup = BeautifulSoup(html, "html.parser")
    fillList(soup)
    # printcomment()


def getHTML(url):
    try:
        headers = {'cookie': '_zap=523489b0-e941-417f-8f6a-78ffd0cdd7d1; _xsrf=0P2AOAR4txN6F3TIkAy26GaKTQPjy4i6; '
                             'd_c0="AGAQOuyZHhSPToUr4_USumtX0404ViCt8Z8=|1638430999"; '
                             'Hm_lvt_98beee57fd2ef70ccdd5ca52b9740c49=1636615609,1636629537,1636900725,1638431000; '
                             '__snaker__id=vMEFNSzF9wJXFnEZ; SESSIONID=rkeP596J0F0ghc3bDGodgVJjr1gtYVM8rSftfFwL8s6; '
                             'JOID=UlAWAELLakpdj4MRU8i7kvAtP9dCsQovB7OyLBnyJHE67ekqOtAY6D'
                             '-OgBpZ_EqKtYGNAz1QOBpJufXd5Klmx6M=; '
                             'osd'
                             '=U1sWBUnKYUpYhIIaU82wk_stOtxDugoqDLK5LBz5JXo66OIrMdAd4z6FgB9S_UG'
                             'KsIqMCD1VMxtCufDW5aJmwqg=; _9755xjdesxxd_=32; YD00517437729195%3'
                             'AWM_NI=Q017jhT79Qc4kjsYuxxYO%2F6wveMTGLzfAAMdxeZMH5SNit7v6VoboVme'
                             'K3w2kSEWd2K95YPgeG%2FK%2FaJ%2BHczAGItbGURoCQstXLL8AVrPmQUJaRyHqz9'
                             'fpl5Kpi3dmEYPZ1E%3D; YD00517437729195%3AWM_NIKE=9ca17ae2e6ffcda17'
                             '0e2e6eea2b56ba7ad8a99cf4fa7868bb3c85f869f9a85b680aae997b3bc4283a9'
                             'bcbbc72af0fea7c3b92a93f0ffd8e96498e9f7b2e240a9b6bdbaf874bc8781d0b'
                             '57db6bb83b5c648baba8fa2d070bcbb96aecb3f9192a795b67ef68aa183ee5eaf'
                             'bb85d4f63aa98d8bb8e73a89e7fbbad36da799e1acae6b8af58884f94b8597bc8'
                             '3c65f92b18db2f2809c9484d9c45eb290a3b2d842a38eb7a9f472fbbac08db841'
                             'b4b7fd85f04f9b9096d2c837e2a3; YD00517437729195%3AWM_TID=o5t%2BGN8'
                             'VdLpFAQUQUFdqjFsLg5%2Futzu9; gdxidpyhxdE=D06wdzNbYsDg6knO%2FfKX4a'
                             'ZhowPpfSh2ogPq3eZQTmkSB8OxWS2mXROulTjV6LiUq3iGw%5CLkWmMR%5CKa%2Bn'
                             'r8r3m2gVnbjNkY911zepHOnPm4dSV%2BWnG%2BCOAsh%2Bq%2F6kegl2Ofk%5CHnD'
                             'YGnzyPe7B24giL2bO2wrGguXbWA5A%2B6hNwWtkoqZ%3A1638435381588; captc'
                             'ha_session_v2="2|1:0|10:1638434506|18:captcha_session_v2|88:MDRSY'
                             'kJRQ2Vwa2dGMGxwU0RqRjJZeWN1T2FFbXJYT3FMb3hhaUNGWklqMFFMSllwc3FBMW'
                             't4OU5yZHIzRzBlUg==|a230b51ea6b3a6e0d5f28dc05463920930556cb5a0f8e4'
                             '842591359e7829f1be"; z_c0="2|1:0|10:1638434545|4:z_c0|92:Mi4xWmFf'
                             'NUtnQUFBQUFBWUJBNjdKa2VGQ2NBQUFDRUFsVk44UlBRWVFBTUZ5SjR6LW5FRDU0O'
                             'G9KbFkwc081UjBfdjNB|8e387e3181d852daae9ddf961508be175b1e7691a0f1a'
                             '87a0a7cb2c1bc9af342"; tst=h; NOT_UNREGISTER_WAITING=1; Hm_lpvt_98'
                             'beee57fd2ef70ccdd5ca52b9740c49=1638436210; KLBRSID=975d56862ba86e'
                             'b589d21e89c8d1e74e|1638436211|1638430998',
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/91.0.4472.106 Safari/537.36'}
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        return r.text
    except:
        print("error")


def fillList(soup):
    titleandhref = soup.find_all('a', {'class': 'HotItem-img'})
    titlelist.clear()
    pagehreflist.clear()
    for news in titleandhref:
        if len(news) == 0:
            break
        title = news.get('title')
        href = news.get('href')
        titlelist.append(title)
        pagehreflist.append(href)


def getPage(url):
    try:
        pagetext = ''

        headers = {
            'User-Agent': Faker().user_agent()
        }
        r = requests.get(url, headers=headers)
        r.encoding = 'utf-8'
        soup = BeautifulSoup(r.text, "html.parser")
        pagelisttotal = soup.find_all('p', {'data-pid': re.compile('.*')})
        for page in pagelisttotal:
            pagetext += page.string + '\n'
        return pagetext
    except:
        return ''


def saveCiyun(timetititlecopy, wccopy):
    title = timetititlecopy.replace(':', '.')
    path = 'record\\WordCloud\\'
    file_name = path + title
    if file_name not in os.listdir(path):  # 文件夹名称不存在才创建
        try:
            os.mkdir(file_name)
            with open('record\\WordCloud\\{filename}\\Top{number}.txt'.format(filename=title, number=number),
                      'w') as f:
                f.write('标题：' + titlelist[number - 1] + '\n\n' + '正文：' + '\n' + pagelist)
            wccopy.to_file(os.path.join('record/WordCloud/{}'.format(title), '本次获取的词云.jpg'))
            tk.messagebox.showinfo('成功', '保存成功')
        except:
            tk.messagebox.showerror('错误', '您已经保存了当前的文章和词云，刷新一下试试')


def GO(startwindowcopy, enternumber):
    text = ''
    n = enternumber - 1
    # 当用户第一次点击生成词云生成词云和记录并保存，当用户第二次点击时就不再生成词云而直接保存
    global pagelist
    # 把50篇文章进行题词
    pagetext = getPage(pagehreflist[n])
    if len(pagetext) < 20:
        pagelist = '不好意思，这篇文章可能是因为网络问题，暂时没有找到。。。'
    else:
        pagelist = pagetext
    cut = jieba.lcut(pagelist)

    # 一共三次删除cut表里面的长度为1的汉字
    for j in cut:
        j.split(' ')
        j.strip(' ')
        if len(j) <= 1:
            cut.remove(j)
    for j in cut:
        j.split(' ')
        j.strip(' ')
        if len(j) <= 1:
            cut.remove(j)
    for j in cut:
        j.split(' ')
        j.strip(' ')
        if len(j) <= 1:
            cut.remove(j)

    text += ' '.join(cut)
    # print(text)

    # 生成词云
    mask = nu.array(Image.open('img/bolt.png'))
    global wc
    wc = WordCloud(font_path='simkai.ttf', mask=mask, max_words=800, contour_width=1, contour_color='blue',
                   background_color='white', scale=6)
    wc.generate(text)
    mat.imshow(wc)
    # mat.show()

    wc.to_file(os.path.join('cache', 'ciyun.jpg'))  # 将生成的词云暂时保存在cache路径下

    showciyu = tk.Toplevel(startwindowcopy)
    showciyu.geometry('450x550+400+50')
    showciyu.title('目前的热点词云')
    showciyu.resizable(width=False, height=False)

    btusaveciyun = tk.Button(showciyu, text='保存Top50文章和词云', command=lambda: saveCiyun(timetitle, wc), width=20)

    # 想要在窗口显示图片就必须全局这两个变量，我也不知道为什么
    global img
    global photo
    # 2.读取图片并在窗口显示
    img = Image.open('cache/ciyun.jpg')  # 打开图片
    showimg = img.resize((400, 405), Image.BILINEAR)  # 保存的图片太大，改变在窗口显示的大小
    photo = ImageTk.PhotoImage(showimg)  # 用PIL模块的PhotoImage打开
    imglabel = tk.Label(showciyu, image=photo, width=400, height=500)
    imglabel.pack(side='top')
    btusaveciyun.pack()


def getPageAndCiyun(startwindowcopy, enternumber, choosecopy):
    choosecopy.destroy()
    try:
        enternumber = int(enternumber)
    except:
        tk.messagebox.showerror('错误', '您输入的数字不合法！')

    if enternumber > len(titlelist):
        tk.messagebox.showerror('错误', '您输入的数字不合法！')
    else:
        global number
        number = enternumber
        GO(startwindowcopy, number)


def getciyun(startwindowcopy):
    # text = ''
    if pagelist == '':
        choose = tk.Toplevel(startwindowcopy)
        choose.geometry('200x150+450+250')
        choose.title('目前的热点词云')
        choose.resizable(width=False, height=False)

        topnumber = tk.Label(choose, text='共爬取了{}篇文章'.format(len(titlelist)), font=("华文行楷", 15), fg="green")
        topnumber.pack(pady=10)

        enter = tk.Entry(choose)
        enter.pack(pady=10)
        # enter.insert(0, '您想获取Top几？')

        butGO = tk.Button(choose, text='GO!',
                          command=lambda: getPageAndCiyun(startwindowcopy, enter.get(), choose),
                          width=15, state='normal')
        butGO.pack(pady=10)
    else:
        showciyu = tk.Toplevel(startwindowcopy)
        showciyu.geometry('450x550+400+50')
        showciyu.title('目前的热点词云')
        showciyu.resizable(width=False, height=False)

        btusaveciyun = tk.Button(showciyu, text='保存Top50文章和词云', command=lambda: saveCiyun(timetitle, wc), width=20)

        # 想要在窗口显示图片就必须全局这两个变量，我也不知道为什么
        global img
        global photo
        # 2.读取图片并在窗口显示
        img = Image.open('cache/ciyun.jpg')  # 打开图片
        showimg = img.resize((400, 405), Image.BILINEAR)  # 保存的图片太大，改变在窗口显示的大小
        photo = ImageTk.PhotoImage(showimg)  # 用PIL模块的PhotoImage打开
        imglabel = tk.Label(showciyu, image=photo, width=400, height=500)
        imglabel.pack(side='top')
        btusaveciyun.pack()


# 往text区域添加链接样式的文字
def insertLink(textcopy, link, row):
    row = str(row)
    lenght = len(link) + 5
    lenght = str(lenght)
    textcopy.insert('insert', '     ' + link + '\n\n')
    textcopy.tag_add("link", '{}.5'.format(row), '{}.{}'.format(row, lenght))
    textcopy.tag_config('link', foreground='blue', underline=True)


def getinformation(btuinformationcopy, textcopy, butciyuncopy):
    btuinformationcopy.config(text='刷新')
    global pagelist
    pagelist = ''  # 每次点击获取Top50按钮时都清空pagelist重新生成词云
    text = textcopy
    butciyun = butciyuncopy

    text.config(state='normal')
    text.delete('1.0', 'end')

    getTitleAndPagehref()

    for i in range(len(titlelist)):
        text.insert('insert', 'Top{}:'.format(i + 1) + titlelist[i] + '\n')
        # text.insert('insert', '     ' + pagehreflist[i] + '\n\n')
        insertLink(text, pagehreflist[i], i * 3 + 2)
    text.config(state='disable')

    # 点击获取Top50按钮后获取词云的按钮可以点击
    if text.get('1.0', 'end'):
        butciyun.config(state='normal')

    # 开始存入搜索记录
    t = time.localtime()
    global timetitle

    # 用户点击获取Top50按钮后就生成一个时间的名字来记录和作为保存文件的名字
    timetitle = str(t.tm_year) + '.' + str(t.tm_mon) + '.' + str(t.tm_mday) + ' ' + \
                str(t.tm_hour) + ':' + str(t.tm_min) + ':' + str(t.tm_sec)

    # 往txt文件里面写入搜索记录
    with open('record/SearchRecord/searchrecord.txt', 'a', encoding='utf-8') as f:
        f.write('\n' + timetitle + '\n')
        for i in range(len(titlelist)):
            f.write('       ' + 'Top{}: '.format(i + 1) + str(titlelist[i]) + '\n')


def getStartWindow():
    startwindow = tk.Tk()
    startwindow.title('知乎Top50，看看网友都在关注什么吧！')
    startwindow.geometry('500x620+400+30')
    startwindow.resizable(width=False, height=False)

    menubar = tk.Menu(startwindow)

    myoperate = tk.Menu(menubar, tearoff=False)
    myoperate.add_command(label="我的搜索记录", command=lambda: showSearchRecord(startwindow))
    myoperate.add_command(label="我的保存记录", command=lambda: showWordCloud())

    menubar.add_cascade(label="我的", menu=myoperate)
    startwindow.config(menu=menubar)

    # 声明窗口顶部的主frame和里面的两个子frame,frametoprleft放一个惊讶的图片frametopright放一个top50的图片
    frametop = tk.Frame(startwindow, height=200, width=500)
    frametopright = tk.Frame(frametop, height=200, width=300)
    frametoprleft = tk.Frame(frametop, height=200, width=200)

    # 创建top50的画布，放一个top50的图片，再把这个画布放在frametopright里面
    toprightimg = tk.Canvas(frametopright, height=200, width=300)
    imgfileright = tk.PhotoImage(file='./img/top50.png')
    toprightimg.create_image(0, 0, anchor='nw', image=imgfileright)

    # 创建惊讶图片的画布，放一个惊讶的图片，再把这个画布放在frametoprleft里面
    topleftimg = tk.Canvas(frametoprleft, height=200, width=200)
    imgfileleft = tk.PhotoImage(file='./img/jy.png')
    topleftimg.create_image(0, 0, anchor='nw', image=imgfileleft)
    toprightimg.pack()
    topleftimg.pack()

    # frametoprleft在主frame的左边，frametopright在主frame右边的
    frametoprleft.pack(side='left')
    frametopright.pack(side='right')
    # frame放在窗口的顶部
    frametop.pack(side='top')

    tip = tk.Label(startwindow, text='辉煌时刻谁都有，别把一刻当永久', font=("华文行楷", 20), fg="green")
    tip.pack()

    # 在text下面创建一个frame区域来放横向滚动条
    framescrollbar = tk.Frame(startwindow, height=20, width=450)

    # 横向滚动条
    s2 = tk.Scrollbar(framescrollbar, orient='horizontal')

    # 自带纵向滚动条的text
    text = scrolledtext.ScrolledText(startwindow, width=40, relief='groove', height=14,
                                     font=("隶书", 15), wrap='none',
                                     xscrollcommand=s2.set)
    text.insert('insert', '还没有内容\n点击下方的“获取Top50” 按钮试试')
    text.config(state='disable')
    s2.config(command=text.xview)
    text.pack()
    framescrollbar.pack()
    s2.pack(ipadx=185)

    framebutton = tk.Frame(startwindow, height=60, width=500)  # 在滚动条下面创建一个frame区域来放功能按钮

    butinformation = tk.Button(framebutton, text='获取Top50',
                               command=lambda: getinformation(butinformation, text, butciyun), width=15)
    butinformation.place(x=39, y=20)

    butciyun = tk.Button(framebutton, text='生成词云', command=lambda: getciyun(startwindow), width=15, state='disable')
    butciyun.place(x=326, y=20)

    framebutton.pack()

    startwindow.mainloop()


getStartWindow()
