import ctypes
import os.path
import re
import threading
import tkinter.messagebox
import tkinter as tk
from time import sleep
from tkinter import messagebox
from tkinter.ttk import Progressbar

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from wordcloud import WordCloud
import matplotlib.pyplot as mat
import jieba
from PIL import Image, ImageTk
import numpy as nu


# text = '我盯着他的眼睛说：我会给你第三项师姐记录还有一面奥运会金牌，不要担心'
# wc = WordCloud(font_path='simkai.ttf', background_color='white')
# wc.generate(text)
#
# mat.imshow(wc)
# mat.show()
# wc.to_image()
def serial_read():
    messagebox.showinfo('sdf', 'asdga')


def run():
    for i in range(400):
        p_bar['value'] = i + 1
        # 更新进度条值
        root.update()
        sleep(.05)


# def stop_thread(thread):
#     thread.join()
#

# myThread = threading.Thread(target=serial_read)
# myThread.start()
# with open('record/WordCloud/2021.12.7 18.42.50/Top1.txt', mode='r', encoding='utf-8') as parttop:
#     part = parttop.read()

root = tk.Tk()
root.geometry('400x80')
p_bar = Progressbar(root, length=350)
p_bar.pack(pady=10)
# 设置进度条最大值
p_bar['maximum'] = 400
# 设置进度条当前值(此处为清零/设初值为零)
p_bar['value'] = 0
tk.Button(root, text='走你', command=run).pack()
root.mainloop()

part = '强制性问候目的是为了加强上级领导力与下级服从性，名正言顺需要培养这两种能力的只有军事部队和一部分行政部门。其他的一切都是容嚒嚒强吻五阿哥——给自己加戏,'
cut = jieba.lcut(part)
for i in cut:
    if len(i) == 0:
        del i
for i in cut:
    print(i)
text = ' '.join(cut)

mask = nu.array(Image.open('img/bolt.png'))

wc = WordCloud(font_path='simkai.ttf', mask=mask, max_words=800, contour_width=1, contour_color='gray')
wc.generate(text)
mat.imshow(wc)
# myThread = ctypes.c_long()
# stop_thread(myThread)
mat.show()
