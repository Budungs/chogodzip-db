# json 활용 크롤링
import requests # 크롤링에 사용하는 패키지
from bs4 import BeautifulSoup # html 변환에 사용함
import time
import json
import random

# DB 연결
import MySQLdb

conn = MySQLdb.connect(
    user="root", # user명
    passwd="1234", #pw명
    host="localhost", 
    db="dabang_data" #연결할 DB명
    # charset="utf-8"
)
print(type(conn)) # 정상 연결 시 : <class 'MySQLdb.connections.Connection'>
cursor = conn.cursor()
print(type(cursor)) # 정상 연결 시 : <class 'MySQLdb.cursors.Cursor'>
# DB 구문 수행
# cursor.execute("CREATE TABLE IF NOT EXISTS coliving (room_no INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(70))") # 테이블 생성
conn.commit() 

cur_page_num = 1 # 현재 페이지 번호
data_cnt = 0 # 가져온 데이터 개수
while(1):
    # 카테고리 데이터 가져오기
    url = f'https://api.gobang.kr/v1/houses?%7B%22HOUSE_TYPE_CDS%22%3A%5B%22HOUTP00004%22%5D%2C%22DONGLI_CDS%22%3A%5B%2211%22%5D%2C%22PAGE_NUM%22%3A{cur_page_num}%2C%22randomSeed%22%3A8165%7D'

    # 헤더정보
    header = {
        'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Mobile Safari/537.36',
        'referer': 'https://m.gobang.kr/share'
    }

    response = requests.get(url, headers=header) # get 요청으로 접속
    if response.status_code == requests.codes.ok:
        print(f'---------{cur_page_num}페이지 접속성공---------')
    else:
        print(f'---------{cur_page_num}페이지 접속실패---------')
    
    json_data = json.loads(response.text) # json파일을 리스트로 받아옴
    #print(json_data)

    # NAME을 추출하는 코드
    for house in json_data["DATA"]:
        room_cnt = random.randint(1, 3)
        print(room_cnt)

        print(house["NAME"])
        room_name = house["NAME"]

        floor_raw = house["FLOOR"]
        floor = floor_raw
        
        if(house_type_cd == 'HOUTP00004') : # [임시] ENUM에 없어서 임시로 변경
            house_type_cd = 'HOUTP00003'
        print(house_type_cd)

        house_type_nms_raw = house["HOUSE_TYPE_NMS"]
        house_type_nms = house_type_nms_raw.split('|')[0]  # '|' 기호로 분리 후 첫 번째 값을 선택
        print(house_type_nms)
        if(house_type_nms not in ('쉐어하우스', '원룸텔', '고시원')):
            house_type_nms = "쉐어하우스" # [임시] ENUM에 없어서 임시로 변경

        gender_cd = house["GENDER_TYPE_CD"]
        print(gender_cd)

        tags = house["TAGS"]
        print(tags)

        img_id = house["TITLE_IMAGE"]
        print(img_id)

        room_addr = house["DONGLI_FULL_NM"]
        print(room_addr)

        room_addr_fl = house["ADDR_FULL_ROAD"]
        print(room_addr_fl)

        room_lat = house["LATITUDE"]
        print(room_lat)

        room_long = house["LONGITUDE"]
        print(room_long)

        deposit_max = house["DEPOSIT_MAX"]
        print(deposit_max)

        deposit_min = house["DEPOSIT_MIN"]
        print(deposit_min)

        price_max = house["PRICE_MAX"]
        print(price_max)

        price_min = house["PRICE_MIN"]
        print(price_min)

        is_sold_out = random.choice(['T', 'F'])
        print(is_sold_out)
        
        # SQL 실행 부분
        cursor.execute("""
            INSERT INTO room 
            (ROOM_CNT, ROOM_NAME, FLOOR, HOUSE_TYPE_CD, HOUSE_TYPE_NMS, GENDER_CD, TAGS, IMG_ID, ROOM_ADDR, ROOM_ADDR_FL, ROOM_LAT, ROOM_LONG, DEPOSIT_MAX, DEPOSIT_MIN, PRICE_MAX, PRICE_MIN, IS_SOLD_OUT) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            room_cnt,
            room_name,           # ROOM_NAME
            floor,               # FLOOR
            house_type_cd,       # HOUSE_TYPE_CD
            house_type_nms,      # HOUSE_TYPE_NMS
            gender_cd,           # GENDER_CD
            tags,                # TAGS
            img_id,              # IMG_ID
            room_addr,           # ROOM_ADDR
            room_addr_fl,        # ROOM_ADDR_FL
            room_lat,            # ROOM_LAT
            room_long,           # ROOM_LONG
            deposit_max,         # DEPOSIT_MAX
            deposit_min,         # DEPOSIT_MIN
            price_max,           # PRICE_MAX
            price_min,           # PRICE_MIN
            is_sold_out          # IS_SOLD_OUT
        ))

        conn.commit()

        # 밑에 이거 주석 풀기
        #cursor.execute("INSERT INTO coliving (name) VALUES (%s)", (house["NAME"],)) # SQL Injection 방지 코드 (자리 표시자(%s) 이용)
        #cursor.execute(f"INSERT INTO coliving (name) VALUES ('{house_name}')")
    data_cnt = data_cnt + 1

    # 만약 다음 페이지가 없는 경우 (==hasMore 값이 false 인 경우) 페이지 종료
    if json_data["hasMore"] == False:
        break
    else: # 다음 페이지가 있는 경우 다음 페이지 json 데이터 보기
        cur_page_num = cur_page_num + 1


print("============작업 정상 종료!!================")

print(f"총 데이터 개수 : {data_cnt}")
conn.commit()

cursor.execute("SELECT * FROM room")
results = cursor.fetchall() # 한 개만 가져올 때는 fetchone() 메서드 사용
for result in results:
    print(result)
