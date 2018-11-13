'''
 review:
 1.web自动化selenium环境：
        pip install selenium
        chromedriver 放置系统path路径下(python路径)
 2.元素定位方法8种
        浏览器开发者工具F12-elements。
        xpath:
            //:表示相对路径
            @：属性
            /..:上级
            /:下级
            text():文本值
 3.selenium常用操作
     find_element和find_elemens
     send_keys() click()
     refresh
     window_handles
     switch_to.handle(窗口名称)
     鼠标操作：
        导入：Actionschains,perform()方法执行 move_to_elements.....
今日：
     1.xpath中更灵活的俩种语法
     contains: 某个元素的某个属性或者文本值包含了什么，例如：//*[contains(@class,'test')]，表示该元素的class的值包含了 test
     starts-with:某个元素的某个属性或者文本值以什么开始，例如：//*[starts-with(@class,'test')]，表示该元素的class的值以test开始
    2. 切换frame：frameset跟其他普通标签没有区别，不会影响到正常的定位，跟普通元素写xpath是一样的 
       但是⽽frame与iframe里面的元素，需要切换进去才能操作到其中的元素。
       如果脚本报什么元素找不到：在你确认xpath没写错的情况下，先去观察改元素上下级有没有frame标签。或者直接//frame  //iframe搜索
       切换frame：switch_to_frame(id,name,frame的xpath)
    实例：qq邮箱登录：
    driver = webdriver.Chrome()
    driver.get("https://mail.qq.com/")
    driver.switch_to.frame("frame的id")
    driver.find_element_by_xpath("用户名输入框").send_keys()
    
    3.常用js方法：JavaScript可以获取浏览器提供的很多对象，并进行操作。window就是一个对象；表示浏览器窗口
        浏览器开发者工具F12-elements-console：
        window就是一个对象；表示浏览器窗口
                window.open(url)
                 window.innerWidth
				 window.innerHeight
				 window.outerWidth
				 window.outerHeight
				 滚动条：window.scrollTo(0,document.body.scrollHeight)
				  window.By(0,document.body.scrollHeight)
				 非页面类型的滚动条：document.getElementsById(id)[0].scrollTop=''
         document:表示当前页面对象
		         HTML在浏览器中以DOM形式表示为树形结构，
		        document对象就是整个DOM树的根节点,然后去操作子节点
		        获取当前标题：document.title
                输入文本的值：document.getElementsById(id)[0].value=''
                操作标签：   document.getElementsById(id)[0].click()
                更改属性：   document.getElementById('vip').style.visibility='visible'
        扩展：如果该元素没有id或者name，可以用querySelect方法
              document.querySelector("该元素的css").click()
 4.自动化用例动态读取excel表里面的数据，典型的数据驱动实例
   a.安装python操作excel依赖的模块：    pip install xlrd
     xlrd（读取excel） xlwt(写入excel)
     
    import xlrd,xlwt   
    excel =xlrd.open_workbook(r'C:\Users\MIME\Desktop\test.xlsx')    获取本地的excel
    sheet = excel.sheet_by_index(0)                                  取该excel的第一个sheet
    print(sheet.nrows,sheet.ncols)                                   表示获取sheet中的行，列数
    
    实例：新建excel，写入用户名和密码的测试数据，写一个测试用例(登录)，依次去读取excel表的数据，
         实现打开一次浏览器，和打开多次浏览器登录
    实现打开x(excel表中的数据多少组)次浏览器
        #定义登录方法：
        def login(username,password):
            driver = webdriver.Chrome()
            driver.get("http://127.0.0.1:5000/")
            driver.find_element_by_xpath("").click()   点击登录按钮
            driver.find_element_by_xpath("").send_keys()  输入用户名
            driver.find_element_by_xpath("").send_keys() 输入密码
            driver.find_element_by_xpath("").click()   点击signin 按钮登录
        #循环去取excel数据，循环的是excel的行数(sheet.nrows)
        for i in range(sheet.nrows):
            username = int(sheet.row_values(i)[0])
            password = int(sheet.row_values(i)[1])
            print('第{0}行，用户名{1}，密码{2}'.format(i,username,password))            获取每一行的数据：用户名和密码
            login(username,password)                                                       调用登录方法
    仅打开一次浏览器
        #定义登录方法：
        def login():
            driver = webdriver.Chrome()
            driver.get("http://127.0.0.1:5000/")
            driver.find_element_by_xpath("").click()   点击登录按钮
            #循环去取excel数据循环的是excel的行数(sheet.nrows)
            for i in range(sheet.nrows):
                username = int(sheet.row_values(i)[0])
                password = int(sheet.row_values(i)[1])
                print('第{0}行，用户名{1}，密码{2}'.format(i,username,password))            获取每一行的数据：用户名和密码
                driver.find_element_by_xpath("").send_keys  输入用户名
                driver.find_element_by_xpath("").send_keys  输入密码
                driver.find_element_by_xpath("").click()   点击signin 按钮登录
        login()     #方法记得需要调用，才会执行
    5. 练习郑州大学官网：俩个用例，灵活运用学过的xpath，鼠标操作，切换frame，切换window
    from selenium import  webdriver
    from selenium.webdriver.common.action_chains import ActionChains
    俩个用例：
    1.点击院系专业-临床医学系=
    driver = webdriver.Chrome()
    driver.get("http://www.zzu.edu.cn/")
    #切换frame
    driver.switch_to.frame("zzu_top_6")
    tag=driver.find_element_by_xpath("//*[text()='院系专业']")
    ActionChains(driver).move_to_element(tag).perform()
    driver.find_element_by_xpath("//*[text()='临床医学系']").click()
    2.再返回首页点击院系专业下的“更多按钮”
    window_list = driver.window_handles
    driver.switch_to.window(window_list[0])
    #返回首页后需要继续切换frame
    driver.switch_to.frame("zzu_top_6")
    tag=driver.find_element_by_xpath("//*[text()='院系专业']")
    ActionChains(driver).move_to_element(tag).perform()
    driver.find_element_by_xpath("//*[text()='临床医学系']/../..//*[contains(text(),"更多")]").click()
上面的切换frame和鼠标移动，因为俩个用例都用到了，可以封装成一个方法，大家自己去写一下
'''
   homework：
   背景：上节课中我们练习了从excel依次读取数据，仅打开一次浏览器，自动化脚本就可依次去输入excel表中的数据
	 但是前提是第一个用户名和密码都是错误的，如果用户名和密码正确的话，就进入了登录界面
	 这时候再去用户名输入框输入数据会报错，用户名输入框找不到
	
   练习：前提还是只打开一次浏览器
	 条件：不管excel表中的某一行的用户名和密码，是否是正确的数据，都不影响自动化脚本去读excel表下一行中的数据，实现登录，
         例如excel表中的数据可能是这样的：
	 15902127953    123456   第一行 正确的用户名和密码
	 159021         123      第二行 错误的用户名和密码
	 15902127953    123456   第三行 正确的用户名和密码
	 159021279      123      第四行 错误的用户名和密码 
	 
  有兴趣的同学可以用xlwt模块，
  用python去新建excel，写入数据，
  再用xlrd模块去读取你写入的excel数据，
  再用自动化脚本去登录
'''
