from urllib.request import urlopen, Request
from urllib.parse import quote_plus # 아스키 코드로 변환시켜준다.
from bs4 import BeautifulSoup
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import os

os.chdir('C:/Users/용준/OneDrive - UOS/바탕 화면/python workspace/img')
headers= {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; ; NCLIENT50_AAP1C9D5E957E6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.75 Safari/537.36'}


def createFolder(directory): 
    try: 
        if not os.path.exists(directory): 
            os.makedirs(directory) 
    except OSError: 
        print ('Error: Creating directory. ' + directory)

# 변수 url 에 저장될 url 형식은 아래와 같다.
# https://www.instagram.com/explore/tags/%EC%95%84%EC%9D%B4%EC%9C%A0/

with open("꽃종류re.txt") as f:
    plantList=[]
    while True:
        line = f.readline()[:-1]
        if not line: break
        plantList.append(line)


# baseUrl은 검색하기 전의 베이스가 되는 url이다.
instaUrl = 'https://www.instagram.com'
#plusUrl은 input으로 검색어를 받아서 아래에서 baseUrl에 추가되는 url이다.
print('아이디 입력: ')
id=input()
print('비밀번호: ')
pw=input()


#창 열고 로그인
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.get(instaUrl) # 드라이버를 띄운다. (크롬 웹 페이지를 연다.)
time.sleep(1)

id_box = driver.find_element_by_css_selector("#loginForm > div > div:nth-child(1) > div > label > input")   #아이디 입력창
password_box = driver.find_element_by_css_selector("#loginForm > div > div:nth-child(2) > div > label > input")     #비밀번호 입력창
login_button = driver.find_element_by_css_selector('#loginForm > div > div:nth-child(3) > button > div')     #로그인 버튼

#동작 제어
act = ActionChains(driver)      #동작 명령어 지정
act.send_keys_to_element(id_box, id).send_keys_to_element(password_box, pw).click(login_button).perform()     #아이디 입력, 비밀 번호 입력, 로그인 버튼 클릭 수행
time.sleep(10)

baseUrl = 'https://www.instagram.com/explore/tags/'

#67종 사진 인스타 샘플링
for plant in plantList:
    plusUrl = plant
    createFolder(plant)
    
    #검색창 가져오기
    #plusUrl로 받아온 검색어를 quote_plus 모듈로 아스키 코드로 변환시킨 뒤, url에 저장시킨다.
    url = baseUrl + quote_plus(plusUrl)+'/?hl=ko'
    req=Request(url, headers=headers)
    driver.get(url)
    time.sleep(10)

    SCROLL_PAUASE_TIME=3 
    #스크롤을 내려준다
    while True:
        time.sleep(SCROLL_PAUASE_TIME)
        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUASE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUASE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        else:
            last_height = new_height
            continue

    html = driver.page_source
    soup = BeautifulSoup(html,'lxml')

# select는 페이지에 있는 정보를 다 가져 온다.
# 클래스가 여러 개면 기존 클래스의 공백을 없애고 .으로 연결시켜 주어야 한다.
    insta = soup.select('._aabd._aa8k._aanf')
    n = 1
# 이미지 하나만 가져올 게 아니라 여러 개를 가져올 것이므로 반복문을 쓴다.
    for i in insta:
    # 인스타 주소에 i번 째의 a태그의 href 속성을 더하여 출력한다.
        print('https://www.instagram.com' + i.a['href'])
    # 인스타 페이지 소스에서 이미지에 해당하는 클래스의 이미지 태그의 src 속성을 imgUrl에 저장한다.
        imgUrl = i.select_one('._aagv').img['src']
        with urlopen(imgUrl) as f:
        # img라는 폴더 안에 programmer(n).jpg 파일을 저장한다.
        # 텍스트 파일이 아니기 때문에 w(write)만 쓰면 안되고 binary 모드를 추가시켜야 한다.
            with open(str(plant)+'/'+ plusUrl + str(n) + '.jpg', "wb") as h:
            # f를 읽고 img에 저장한다.
                img = f.read()
            # h에 위 내용을 쓴다.
                h.write(img)
    # 계속 programmer 1에 덮어쓰지 않도록 1을 증가시켜 준다
        n += 1 
        print(imgUrl)
    # 출력한 걸 보았을 때 구분하기 좋도록 빈 줄을 추가시킨다.
        print()
