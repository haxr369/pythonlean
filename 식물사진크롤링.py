
from selenium import webdriver 
from selenium.webdriver.common.keys import Keys 
import time 
import os 
import urllib.request
import urllib.parse
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as wait
from PIL import Image

#원하는 디렉토리 만들기
def createFolder(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print ('Error: Creating directory. ' + directory)

#with open("Plant_list.txt") as f:
 #   for i in f:
#        plant_list.append(i)

def download_im(keyword, img_numb):
    options = webdriver.ChromeOptions()

    options.add_argument('--headless')


    options.add_argument('--no-sandbox')

    options.add_argument('--disable-dev-shm-usage')

    driver = webdriver.Chrome(options=options)
    
    driver.implicitly_wait(3)
    
    key_dic = os.path.join("C:/Users/용준/OneDrive - UOS/바탕 화면/학교관련자료/랩실/식물사진",keyword)

    createFolder(key_dic)

    print(keyword, '검색') 
    driver.get("https://www.google.co.kr/imghp?hl=ko&tab=wi&authuser=0&ogbl") # 구글 이미지 검색 url
    elem = driver.find_element_by_name("q") #구글 검색창 선택
    elem.send_keys(keyword)
    elem = driver.find_element_by_name("q") 
    elem.send_keys(Keys.ENTER) #검색 엔터키 입력

###### 스크롤 내리기##################################3
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
                driver.find_element_by_css_selector(".mye4qd").send_keys(Keys.ENTER)
            except:
                break
        last_height = new_height
##########################################################################################3
    imgs = driver.find_elements_by_css_selector(".rg_i.Q4LuWd")
    
    
    #path = os.path.join("/home/dir_v","images",keyword)
    #createFolder(path)
    #print(path,"로 저장")
    
    count = 1

    for img in imgs:
        try:
            img.click()
            time.sleep(2)

            imgUrl = driver.find_element_by_xpath(
                '//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[3]/div/a/img').get_attribute(
                "src")
            time.sleep(0.5)
            domain=imgUrl[:5]
            if domain == 'http:':
                imgUrl='https:'+imgUrl[5:] #continue 대신 http를 https로 바꾸어줬음

            ff= ".jpg"
            save_posi = os.path.join(key_dic, keyword+'{0:04d}'.format(count)+ff)
                
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

            print(keyword+'{0:03d}'.format(count)+ff+"를 저장했음 ", '갯수: ', count)
            count = count + 1
            
            if count >= img_numb:
                break
            else:
                continue
        except:
            print("문제 발생")
            pass
    print("저장 끝")
    driver.close()
plant_list =['딱총나무꽃', 'Sambucus nigra flower', '뜰보리수꽃', 'Elaeagnus multiflora flower']

for name in plant_list:
    download_im(name,5000)
