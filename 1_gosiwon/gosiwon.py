# complete 최종 검증 완료
# 고방 기준 원룸텔(고시원) 크롤링 

# json 활용 크롤링
import requests # 크롤링에 사용하는 패키지
from bs4 import BeautifulSoup # html 변환에 사용함
import time
import json
import random
import MySQLdb

# DB 설정 파일 로드
with open('db_config.json') as config_file:
    config = json.load(config_file)

# DB 연결
conn = MySQLdb.connect(
    user=config['user'], # user명
    passwd=config['password'], #pw명
    host=config['host'], # AWS RDS 연결
    db=config['db'] #연결할 DB명
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
    url = f'https://api.gobang.kr/v1/houses?%7B%22HOUSE_TYPE_CDS%22%3A%5B%22HOUTP00001%22%2C%22HOUTP00003%22%5D%2C%22DONGLI_CDS%22%3A%5B%2211%22%5D%2C%22PAGE_NUM%22%3A{cur_page_num}%2C%22randomSeed%22%3A565%7D'

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

    # 현재 페이지의 요소들을 추출하는 함수
    for house in json_data["DATA"]:
        # if(data_cnt > 51):
        #     break
       
       # -------------------------- ROOM 테이블 데이터 -----------------------
        room_id = house["ID"]
        print(room_id)

        room_lat = house["LATITUDE"]
        print(room_lat)

        room_long = house["LONGITUDE"]
        print(room_long)

        thumbnail = house["TITLE_IMAGE"]
        print(thumbnail)

        room_addr = house["ADDR_FULL_ROAD"]
        print(room_addr)

        house_type_nm = house["HOUSE_TYPE_NM"]
        print(house_type_nm)

        dongli_nm = house["DONGLI_NM"]
        print(dongli_nm)

       # -------------------------- GOSIWON 테이블 데이터 -----------------------
        title = house["NAME"] # 검증
        print(title) 

        price_max = house["PRICE_MAX"] # 검증
        print(price_max)

        price_min = house["PRICE_MIN"] # 검증
        print(price_min)

        deposit_max = house["DEPOSIT_MAX"] # 검증
        print(deposit_max)

        deposit_min = house["DEPOSIT_MIN"] # 검증
        print(deposit_min)

        maintenance_fee = house["MAINTENANCE_FEE"] # 검증
        print(maintenance_fee)

        gender_type_cd = house["GENDER_TYPE_CD"] # 검증
        print(gender_type_cd)

        house_type_cd = house["HOUSE_TYPE_CD"] # 검증
        print(house_type_cd)

        enter_age_max = house["ENTER_AGE_MAX"]
        print(enter_age_max)

        enter_age_min = house["ENTER_AGE_MIN"]
        print(enter_age_min)

        

        
        # SQL 실행 부분 (공통) - ROOM 테이블에 삽입
        cursor.execute("SELECT COUNT(*) FROM ROOM WHERE ROOM_ID = %s", (room_id,))
        result = cursor.fetchone()

        if result[0] == 0:  # 데이터가 중복되지 않는 경우에만 삽입
            cursor.execute("""
            INSERT INTO ROOM
                ( ROOM_ID, ROOM_LAT, ROOM_LONG, THUMBNAIL, ADDRESS, HOUSE_TYPE_CD, HOUSE_TYPE_NM, DONGLI_NM)
                VALUES(%s, %s, %s, %s, %s, %s, %s, %s)
            """,(
                room_id,
                room_lat,
                room_long,
                thumbnail,
                room_addr,
                house_type_cd,
                house_type_nm,
                dongli_nm))


        
        # SQL 실행 부분 (고시원) - GOSIWON 테이블에 삽입
        cursor.execute("SELECT COUNT(*) FROM GOSIWON WHERE ROOM_ID = %s", (room_id,))
        result = cursor.fetchone()

        if result[0] == 0:  # 데이터가 중복되지 않는 경우에만 삽입
            cursor.execute("""
                INSERT INTO GOSIWON
                (ROOM_ID, TITLE, PRICE_MIN, PRICE_MAX, DEPOSIT_MIN, DEPOSIT_MAX, MAINTENANCE_FEE, 
                GENDER_LIMIT, TYPE, AGE_MAX, AGE_MIN) 
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                room_id,            # ROOM_ID
                title,              # TITLE
                price_min,           # PRICE_MIN
                price_max,               # PRICE_MAX
                deposit_min,       # DEPOSIT_MIN
                deposit_max,      # DEPOSIT_MAX
                maintenance_fee,                       # MAINTENANCE_FEE
                gender_type_cd,             # GENDER_LIMIT
                house_type_cd,     # TYPE
                enter_age_max,           # AGE_MAX
                enter_age_min,        # AGE_MIN
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

cursor.execute("SELECT * FROM GOSIWON")
results = cursor.fetchall() # 한 개만 가져올 때는 fetchone() 메서드 사용
for result in results:
    print(result)
