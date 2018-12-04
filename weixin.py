import itchat
import re
# jieba分词
import jieba
# wordcloud词云
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator
import os
import numpy as np
import PIL.Image as Image
itchat.login()
friends = itchat.get_friends(update=True)[0:]
tList = []
for i in friends:
    signature = i["Signature"].replace(" ", "").replace("span", "").replace("class", "").replace("emoji", "")
    rep = re.compile("1f\d.+")
    signature = rep.sub("", signature)
    tList.append(signature)
    # 拼接字符串
    text = "".join(tList)
strs = "".join(tList)
with open('record.txt','a',encoding='utf-8') as f:
    f.write(strs)


wordlist_jieba = jieba.cut(text, cut_all=True)
wl_space_split = " ".join(wordlist_jieba)
d= os.path.dirname(os.path.abspath( __file__ ))
alice_coloring = np.array(Image.open(os.path.join(d, r"3.jpg")))
my_wordcloud = WordCloud(background_color="white",
                         max_words=2000,
                         mask=alice_coloring,
                         max_font_size=400,
                         random_state=420,
                         font_path=r'C:\Users\ewuxyuq\Desktop\framework\simhei.ttf'
                         ).generate(wl_space_split)
my_wordcloud.to_file('wechat.jpg')
