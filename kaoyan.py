import requests
from bs4 import BeautifulSoup
from pandas.core.frame import DataFrame
import re
import time


class Graduate:
    def __init__(self, province, category):
        self.head = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKi"
                          "t/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
        }
        self.data = []
        self.province = province
        self.category = category

    def get_list_fun(self, url, name):
        """获取提交表单代码"""
        response = requests.get(url, headers=self.head)
        province = response.json()
        with open("{}.txt".format(name), "w") as f:
            for x in province:
                f.write(str(x))
                f.write("\n")

    def get_list(self):
        """
        分别获取省，学科门类，专业编号数据
        写入txt文件
        """
        self.get_list_fun("http://yz.chsi.com.cn/zsml/pages/getSs.jsp", "province")
        self.get_list_fun('http://yz.chsi.com.cn/zsml/pages/getMl.jsp', "category")
        self.get_list_fun('http://yz.chsi.com.cn/zsml/pages/getZy.jsp', 'major')

    def get_school_url(self):
        """
        输入省份，
        发送post请求，获取数据
        提取数据
        必填省份，学科门类，专业可选填
        返回学校网址
        """
        url = "http://yz.chsi.com.cn/zsml/queryAction.do"
        data = {
            "ssdm": self.province,
            "yjxkdm": self.category,
        }
        response = requests.post(url, data=data, headers=self.head)
        html = response.text
        reg = re.compile(r'(<tr>.*? </tr>)', re.S)
        content = re.findall(reg, html)
        schools_url = re.findall('<a href="(.*?)" target="_blank">.*?</a>', str(content))
        return schools_url

    def get_college_data(self, url):
        """返回一个学校所有学院数据"""
        response = requests.get(url, headers=self.head)
        html = response.text
        colleges_url = re.findall('<td class="ch-table-center"><a href="(.*?)" '
                                  'target="_blank">查看</a>', html)
        return colleges_url

    def get_final_data(self, url):
        """输出一个学校一个学院一个专业的数据"""
        temp = []
        response = requests.get(url, headers=self.head)
        html = response.text
        soup = BeautifulSoup(html, features='lxml')
        summary = soup.find_all('td', {"class": "zsml-summary"})
        for x in summary:
            temp.append(x.get_text())
        self.data.append(temp)

    def get_schools_data(self):
        """获取所有学校的数据"""
        url = "http://yz.chsi.com.cn"
        schools_url = self.get_school_url()
        amount = len(schools_url)
        i = 0
        for school_url in schools_url:
            i += 1
            url_ = url + school_url
            # 找到一个学校对应所有满足学院网址
            colleges_url = self.get_college_data(url_)
            print("已完成第" + str(i) + "/" + str(amount) + "学院爬取")
            time.sleep(1)
            for college_url in colleges_url:
                _url = url + college_url
                self.get_final_data(_url)

    def get_data_frame(self):
        """将列表形数据转化为数据框格式"""
        data = DataFrame(self.data)
        data.to_csv("查询招生信息.csv", encoding="utf_8_sig")


if __name__ == '__main__':
    # province = input("请输入查询学校省份编号:")
    # category = input("请输入查询专业代码:")
    province = "11"
    category = "0812"
    spyder = Graduate(province, category)
    spyder.get_schools_data()
    spyder.get_data_frame()
