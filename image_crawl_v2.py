#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import os 
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests
from bs4 import BeautifulSoup
import json
from PIL import Image


# In[2]:


#https://yobbicorgi.tistory.com/29 코드 출처

"""
네이처링 대한민국 식물 데이터 제공
https://www.naturing.net/o/669048?mission_seq=2379&obs_user_seq=15446
"""

#원하는 디렉토리 만들기
def createFolder(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print ('Error: Creating directory. ' + directory)


plant_list =[]
"""
with open("자귀나무.txt") as f: #자귀나무.txt에는 필요한 키워드를 적어놓은 것입니다.
    for i in f: 

plant_list에 검색하고자 하는 키워드를 작성합니다.
    """



#https://velog.io/@jungeun-dev/Python-%EC%9B%B9-%ED%81%AC%EB%A1%A4%EB%A7%81Selenium-%EA%B5%AC%EA%B8%80-%EC%9D%B4%EB%AF%B8%EC%A7%80-%EC%88%98%EC%A7%91

"""
main_keyword : 폴더 명
sub_keyword : 검색 명
img_numb : 각 sub_keyword 마다 다운로드 받는 이미지 수
"""

def download_im(main_keyword, sub_keyword, img_numb):
    
    keywords = sub_keyword #검색키워드 만들기
    
    options = webdriver.ChromeOptions()

    options.add_argument('--headless')

    options.add_argument('--no-sandbox')

    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(executable_path="/home/dir_v/chromedriver",options=options)
    
    driver.implicitly_wait(3)
    


    print(sub_keyword, '검색') 
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl") # 구글 이미지 검색 url
    elem = driver.find_element_by_name("q") #구글 검색창 선택
    elem.send_keys(sub_keyword)
    elem = driver.find_element_by_name("q") 
    elem.send_keys(Keys.ENTER) #검색 엔터키 입력

    SCROLL_PAUSE_TIME = 1
    last_height = driver.execute_script("return document.body.scrollHeight")  # 브라우저의 높이를 자바스크립트로 찾음
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")  # 브라우저 끝까지 스크롤을 내림
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            try:
                driver.find_element_by_css_selector(".mye4qd").click() #결과더보기가 나올 경우 클릭하기
            except:
                break
        last_height = new_height

    imgs = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, ".rg_i.Q4LuWd")))
    
    path = os.path.join("/home/dir_v","images",main_keyword)
    createFolder(path)
    print(path,"로 저장")
    
    main_long = len(os.listdir(path))
    print("메인 키워드의 길이는",main_long)
    count = 1
    for img in imgs:
        try:

            img.click()
            #img.send_keys(Keys.ENTER)
            time.sleep(2)
            imgUrl = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute(
                "src")


            ff= ".jpg"
            save_posi = os.path.join(path, main_keyword+'{0:04d}'.format(count+main_long)+ff)

            urllib.request.urlretrieve(imgUrl, save_posi)

            img = Image.open(save_posi)
            if img.format != "JPEG":
                now_for = img.format

                if now_for == "PNG":
                    ff = ".PNG"
                elif now_for == "GIF":
                    ff = ".GIF"
                elif now_for == "BMP":
                    ff = ".RLE"
                else:
                    ff = ".jpg"

                now_path = os.path.join(path, main_keyword+'{0:04d}'.format(count+main_long)+ff)
                os.rename(save_posi, now_path)

            print(main_keyword+'{0:04d}'.format(count+main_long)+ff+"를 저장했음")


            count = count + 1
            if count > img_numb:
                break
        except:
            print("문제 발생")
            pass
    driver.close()


for key in plant_list:
    download_im("자귀나무",key,400)

