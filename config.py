def warn(*args, **kwargs):
    pass
import warnings
warnings.warn = warn
import sys
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import linecache 
from datetime import datetime
sys.path.insert(1, f'config')
def driver_setup():
    try:
        options = webdriver.ChromeOptions()
        options.add_experimental_option("excludeSwitches",["ignore-certificate-errors",'enable-logging'])
    except:
        pass
    # options.add_argument('--disable-gpu')
    # options.add_argument('--headless')
    # options.add_argument("--window-size=1920,1080")

    # try:
    #     browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
    #     browser.maximize_window()
    #     return browser
    # except Exception as e:
    
    #     print(e)
    try:
        browser = webdriver.Chrome(executable_path=r'chromedriver.exe',options=options)
        browser.maximize_window()
        time.sleep(4)
        return browser
    except Exception as e:
        print(e)
        return False

def error_log(e, source_page = "lyrics.py"):
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    funtion_name = f.f_code.co_name
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename,lineno, f.f_globals)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    error_came_from = ''
    if source_page != "":
        error_came_from = f'\nError Came From : {source_page}.py'
    error = f"""========================================================================\nERROR AAYA HAI\nDateTime : {dt_string}{error_came_from}\nError File : {filename}\nError Fun Name : {funtion_name}\nError : {e}\nError Type : {exc_type}\nError Line No : {lineno}\nError Line Text : '{line.strip()}')\n========================================================================"""
    print(error)
    with open('errors_log.txt','a',encoding='utf-8') as file:
        file.write(error)
        file.close()