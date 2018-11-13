import pandas as pd
from selenium import webdriver
import urllib
from PIL import Image
import pytesseract
import numpy as np
import time
from matplotlib import pyplot as plt
# import wordcloud
# import jieba
import jieba
import jieba.analyse

from wordcloud import WordCloud

def gethtml(url):
    loginurl='https://www.douban.com/'    # 登录页面

    browser = webdriver.Chrome()    
    browser.get(loginurl)    # 请求登录页面
    browser.find_element_by_name('form_email').clear()  # 获取用户名输入框，并先清空
    browser.find_element_by_name('form_email').send_keys(u'2533450204@qq.com') # 输入用户名
    browser.find_element_by_name('form_password').clear()  # 获取密码框，并清空
    browser.find_element_by_name('form_password').send_keys(u'wuyuqing666') # 输入密码

    # 验证码手动处理,输入后，需要将图片关闭才能继续执行下一步
    captcha_link = browser.find_element_by_id('captcha_image').get_attribute('src')
    urllib.request.urlretrieve(captcha_link,'captcha.jpg')
    Image.open('captcha.jpg').show()
    captcha_code = input('Pls input captcha code:')
    # pic_content=pytesseract.image_to_string(Image.open('captcha.jpg'))
    # print(pic_content)
    # captcha_code = pic_content
    browser.find_element_by_id('captcha_field').send_keys(captcha_code)   
    browser.find_element_by_css_selector('input[class="bn-submit"]').click()
    browser.get(url)
    browser.implicitly_wait(10)
    return(browser)

def getComment(url):
    i = 1
    AllArticle = pd.DataFrame()
    browser = gethtml(url)
    while True:
        s = browser.find_elements_by_class_name('comment-item')
        articles = pd.DataFrame(s,columns = ['web'])
        articles['uesr'] = articles.web.apply(lambda x:x.find_element_by_tag_name('a').get_attribute('title'))
        articles['comment'] = articles.web.apply(lambda x:x.find_element_by_class_name('short').text)
        articles['star'] = articles.web.apply(lambda x:x.find_element_by_xpath("//*[@id='comments']/div[1]/div[2]/h3/span[2]/span[2]").get_attribute('title'))
        articles['date'] = articles.web.apply(lambda x:x.find_element_by_class_name('comment-time').get_attribute('title'))
        articles['vote'] = articles.web.apply(lambda x:np.int(x.find_element_by_class_name('votes').text))
        del articles['web']
        AllArticle = pd.concat([AllArticle,articles],axis = 0)
        print ('The ' + str(i) + ' page finished!')

        try:
            if i==1:
                browser.find_element_by_xpath("//*[@id='paginator']/a").click()  
            else:
                browser.find_element_by_xpath("//*[@id='paginator']/a[3]").click()
            browser.implicitly_wait(10)
            time.sleep(1) # 暂停3秒
            i = i + 1
        except:
            AllArticle = AllArticle.reset_index(drop = True)
            return AllArticle
    AllArticle = AllArticle.reset_index(drop = True)
    
    return AllArticle
	
url = 'https://movie.douban.com/subject/27605698/comments?status=P'
result = getComment(url)
# print(result.to_string())
result.to_csv('C:\\Users\\yuqing.wu\\Downloads\\yuqing.csv',index=False,header=False)




texts = ';'.join(result.comment.tolist())
cut_text = " ".join(jieba.cut(texts))
keywords = jieba.analyse.extract_tags(cut_text, topK=500, withWeight=True, allowPOS=('a','e','n','nr','ns'))


ss = pd.DataFrame(keywords,columns = ['word','important'])

fig = plt.axes()
plt.barh(range(len(ss.important[:20][::-1])),ss.important[:20][::-1],color = 'darkred')
fig.set_yticks(np.arange(len(ss.important[:20][::-1])))
fig.set_yticklabels(ss.word[:20][::-1],fontproperties="font")
fig.set_xlabel('Importance')

alice_mask = np.array(Image.open( "C:\\Users\\yuqing.wu\\Downloads\\yiren.png"))
text_cloud = dict(keywords)
cloud = WordCloud(
        width = 600,height =400,
        font_path="STSONG.TTF",
       # 设置背景色
        background_color='white',

        mask=alice_mask,
        #允许最大词汇
        max_words=500,
        #最大号字体
        max_font_size=150,
        #random_state=777,
        #colormap = 'Accent_r'
    )



plt.figure(figsize=(12,12))
word_cloud = cloud.generate_from_frequencies(text_cloud)
plt.imshow(word_cloud)
plt.axis('off')
plt.show()


# import jieba
# import jieba.analyse
# print("***案例1***"*3)
# txt='那些你很冒险的梦，我陪你去疯，折纸飞机碰到雨天终究会坠落，伤人的话我直说，因为你会懂，冒险不冒险你不清楚，折纸飞机也不会回来，做梦的人睡不醒！'
# Key=jieba.analyse.extract_tags(txt,topK=3)
# print(Key)
