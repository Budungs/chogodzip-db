# 1. driver 만들기
# User Agent Data 변경하기 (mobile 기준)

# change_UA_data.py 사용 시 적용되는 창 전환 : https://wikidocs.net/82611

# CDP Command 레퍼런스 사이트 모음
# CMD 모두 수록 / 파랑 사이트 : https://chromedevtools.github.io/devtools-protocol/tot/Emulation/
# 셀레니움 언어별 /초록 사이트 : https://www.selenium.dev/documentation/webdriver/actions_api/

from bs4 import BeautifulSoup
import pyperclip
import requests
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.chrome.options import Options
import random, time
from user_agents import parse
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

import pyautogui
import os

import time
#  ========================================== 변수 ===================================================
user_agent_txt_path = r'C:\outsourcing\_template\03_BotDetection\useragents.txt' # user-agent 15000개 데이터 txt파일이 저장된 공간
# input_save_path = pyautogui.prompt("저장될 경로명을 입력해주세요.")
# print(f"{input_save_path}에 저장합니다.")
# ========================================== 엑셀 작업 ===================================================
# import openpyxl 
# wb = openpyxl.Workbook() # 1) 엑셀 만들기
# ws = wb.active # 2) 엑셀 워크시트 활성화
# ws.append(['댓글 사용자명', '댓글 내용', '작성일자']) # 3) 엑셀 1행 만들기
#wb.save(excel_save_path)
# ===========================================================================
# ========================================== 파일 작업 ===================================================
# 만약 excel_save_path 경로에 폴더가 있는 경우 그 폴더 위치에 저장하고 excel_save_path 경로에 폴더가 없는 경우 새롭게 폴더를 만들어서 그 안에 저장하도록 한다.
# if os.path.isdir(input_save_path):  # 폴더가 이미 존재하는지 확인
#     # 폴더가 이미 존재하는 경우, 해당 경로에 파일 저장
#     excel_save_path = os.path.join(input_save_path, 'output.xlsx')  # output.xlsx 파일 경로
#     wb.save(excel_save_path)
# else:
#     # 폴더가 존재하지 않는 경우, 새로운 폴더를 생성하여 그 안에 파일 저장
#     os.makedirs(input_save_path, exist_ok=True)  # 폴더 생성 (존재하면 무시)
#     excel_save_path = os.path.join(input_save_path, 'output.xlsx')  # output.xlsx 파일 경로
#     wb.save(excel_save_path)  # 파일 저장
# ===========================================================================

# 드라이버 자동 최신 버전 업데이트
chromedriver_autoinstaller.install()

# user agent data를 바꾸는 함수
def make_user_agent(ua,is_mobile): 
    user_agent = parse(ua)
    model = user_agent.device.model
    platform = user_agent.os.family
    platform_version = user_agent.os.version_string + ".0.0"
    version = user_agent.browser.version[0]
    ua_full_version = user_agent.browser.version_string
    architecture = "x86"
    print(platform)
    if is_mobile:
        platform_info = "Linux armv8l"
        architecture= ""
    else: # Window 기준
        platform_info = "Win32"
        model = ""
    RET_USER_AGENT = {
        "appVersion" : ua.replace("Mozilla/", ""),
        "userAgent": ua,
        "platform" : f"{platform_info}",
        "acceptLanguage" : "ko-KR, kr, en-US, en",
        "userAgentMetadata":{
            "brands" : [
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"},
                {"brand":"Not A;Brand", "version":"99"},
            ],
            "fullVersionList":[
                {"brand":"Google Chrome", "version":f"{version}"},
                {"brand":"Chromium", "version":f"{version}"},
                {"brand":"Not A;Brand", "version":"99"},
            ],
            "fullVersion":f"{ua_full_version}",
            "platform" :platform,
            "platformVersion":platform_version,
            "architecture":architecture,
            "model" : model,
            "mobile":is_mobile #True, False
        }
    }
    return RET_USER_AGENT
# 랜덤한 user-agent가 담긴 useragents.txt 파일을 읽어온다.
def read_agents():
    agents = []
    f = open(user_agent_txt_path,"r",encoding="utf8")
    while True:
        line = f.readline()
        if not line:
            break
        agents.append(line.rstrip())
    return agents
# driver을 만들어주는 함수
    # 쿠키 저장장소 : C:\cookies\{cookie_account_id}
    # cookie_account_id : 쿠키 파일로 생성될 폴더 이름
def make_driver():
    try:
        # 해상도 설정
        pc_device = ["1920,1440","1920,1200","1920,1080","1600,1200","1600,900",
                        "1536,864", "1440,1080","1440,900","1360,768"
                ]

        mo_device = [
                    "360,640", "360,740", "375,667", "375,812", "412,732", "412,846",
                    "412,869", "412,892", "412,915"
                ]

        width,height = random.choice(mo_device).split(",")
        
        UA_list = read_agents()
        #UA = "Mozilla/5.0 (Linux; Android 9; Mi A2 Lite Build/PKQ1.180917.001; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/80.0.3987.132 Mobile Safari/537.36" # user agent 조작
        UA = random.choice(UA_list)  #seed = time.time()
        
        options = uc.ChromeOptions()
        
        # User Agent 속이기
        options.add_argument(f'--user-agent={UA}') # User Agent 변경
        options.add_argument(f"--window-size={width},{height}")
        options.add_argument("--no-first-run --no-service-autorun --password-store=basic")
        options.add_argument('--disable-logging')
        options.add_argument('--disable-popup-blocking') # uc에서 새 탭 열기 허용

        driver = uc.Chrome(options=options, version_main=128) # 일시적인 버전 오류가 있는 경우 version_main=120~122

        UA_Data = make_user_agent(UA, True) # user agent data를 바꾸는 함수 호출 

        driver.execute_cdp_cmd("Network.setUserAgentOverride", UA_Data) # user agent data를 바꾸기 위해 필요한 코드 

        # Max Touch Point 변경
        # 모바일은 보통 1,5 / PC는 보통 0,2
        Mobile = {"enabled":True, "maxTouchPoints" : random.choice([1,5])}
        driver.execute_cdp_cmd("Emulation.setTouchEmulationEnabled", Mobile)
        driver.execute_cdp_cmd("Emulation.setNavigatorOverrides",{"platform":"Linux armv8l"})
        # DeviceMetrics 변경(Emulation 쪽에서 setDeviceMetricsOverride 적용)
        driver.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width":int(width),
            "height":int(height),
            "deviceScaleFactor":1,
            "mobile":True,
        })

        # 위치 정보 변경 (Geo Location 변경) 
        # 서울쪽에 원하는 위치를 잡기 위해서는 구글에 "위도 경도 지도" 검색 후 좌상단, 우하단 위도/경도값을 가져오면 된다.
        # 찾는 사이트 : http://map.esran.com/
        def generate_random_geolcation():
            ltop_lat = 37.61725745260699 # 좌 위도
            ltop_long = 126.92437164480178 # 좌 경도
            rbottom_lat = 37.56825361755575 # 우 위도
            rbottom_long = 127.05771697149082 # 우 경도

            targetLat = random.uniform(rbottom_lat, ltop_lat)
            targetLong = random.uniform(ltop_long, rbottom_long)
            return {"latitude" : targetLat, "longitude" : targetLong, "accuracy":100}
        GEO_DATA = generate_random_geolcation()
        driver.execute_cdp_cmd("Emulation.setGeolocationOverride", GEO_DATA)

        # User Agent 적용
        driver.execute_cdp_cmd("Emulation.setUserAgentOverride",UA_Data)
        print(width,height)
        driver.set_window_size(int(width),int(height))

        return driver
    
    except Exception as e:
        print(e)
        driver = None
        return driver

# 창 띄우기
driver = make_driver()
driver.get('https://m.gobang.kr/home')
driver.implicitly_wait(10)
# 쉐어하우스 버튼 클릭
sharehouse_btn = driver.find_element(By.XPATH, '//*[@id="wrap"]/div[1]/main/div[3]/div[1]/a[2]/span[1]')
sharehouse_btn.click()
driver.implicitly_wait(10)
# 무한 스크롤 구현 
before_height = driver.execute_script("return window.scrollY") # 스크롤 전 높이

scroll_cnt = 0 # 현재 스크롤한 횟수
target_scroll_cnt = 5 # 목표한 스크롤 횟수 (임의로 설정)
while True:
    # 맨 아래로 스크롤을 내린다. (END 키를 눌러 스크롤을 내린다.)
    driver.find_element(By.CSS_SELECTOR, "body").send_keys(Keys.END)
    # 스크롤 되는 동안 로딩 시간을 준다.
    time.sleep(1.5)
    # 스크롤 후 높이 체크
    after_height = driver.execute_script("return window.scrollY")
    scroll_cnt = scroll_cnt + 1
    
    if after_height == before_height: # 끝까지 내린 경우 내린 window.ScrollY 위치가 이전 위치와 같다.
        break # 이 경우에는 탈출한다.
    if scroll_cnt == target_scroll_cnt: # 목표한 횟수까지 스크롤한 경우
        break # 탈출

    before_height = after_height

# 각 요소들을 방문하면서 크롤링
sharehouse_elements = driver.find_elements(By.XPATH, '//*[@id="wrap"]/main/article/section[3]/div[2]/ul/li[*]/section/div')
for sharehouse_element in sharehouse_elements:
    print()

input()
quit()