import pymysql
import requests
import json
                        #'47.95.204.151'
con = pymysql.connect(host='localhost', port=3306, user='root', passwd='root', db='test')             #127.0.0.1

cor = con.cursor()
cor.execute("select * from interface_test")
a = cor.fetchall()
print(a)
for i in a:
    if i[0] == "post":
        response = requests.post(url=i[1], data=json.dumps(i[3]))
        try:
            success_result = response.json()["success"]
            if success_result == i[-1]:
                print("post接口测试成功")
            else:
                print(response.json())
        except:
            print("网络异常")

    if i[0] == 'get':
        response = requests.get(url=i[1], params=json.dumps(i[2]))
        try:
            success_result = str(response.json()["success"])
            if success_result == i[-1]:
                print("get接口测试成功")
            else:
                print("get接口测试失败，结果有问题:",response.json())
        except:
            print("网络异常")

con.close()
