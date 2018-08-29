import sys
from selenium import webdriver
from time import sleep

option = None
driver = None
file_name = None
blog_content = ''


def load_blog():
    argv_len = len(sys.argv)
    if argv_len != 2:
        print('Usage: upload.py xxx.md')
        sys.exit()
    global file_name
    file_name = sys.argv[1]
    global blog_content
    with open(file_name, 'r') as f:
        for line in f:
            blog_content = blog_content + line


def init_driver():
    global option, driver
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')

    driver = webdriver.Chrome(chrome_options=option)
    driver.maximize_window()


def login_cnblogs():

    """Login Cnblogs"""
    driver.implicitly_wait(30)
    login_url = 'https://passport.cnblogs.com/user/signin?ReturnUrl=http:' \
                '//i.cnblogs.com/EditPosts.aspx?opt=1&AspxAutoDetectCookieSupport=1'
    driver.get(login_url)

    driver.find_element_by_id('input1').clear()
    driver.find_element_by_id('input1').send_keys('RogerDTZ')
    driver.find_element_by_id('input2').clear()
    driver.find_element_by_id('input2').send_keys('dfdlxx858*')
    driver.find_element_by_id('signin').click();

    while True:
        # print(driver.current_url)
        if driver.current_url[30] != 'X':
            break
        sleep(0.1)
    # Done


def fill_blog():
    global file_name
    global blog_content

    strlen = len(file_name)

    # set title
    driver.find_element_by_name('Editor$Edit$txbTitle').clear();
    driver.find_element_by_name('Editor$Edit$txbTitle').send_keys(file_name[0:strlen-3])

    # set content
    # textarea = driver.find_element_by_name('Editor$Edit$EditorBody')
    # driver.execute_script("arguments[0].focus();", textarea)
    # sleep(0.1)
    # test = "test \n great"
    # command = "arguments[0].value='{}'".format(test)
    # print(command)
    # driver.execute_script(command, textarea)

    driver.find_element_by_name('Editor$Edit$EditorBody').send_keys(blog_content)


load_blog()
init_driver()
login_cnblogs()
fill_blog()
