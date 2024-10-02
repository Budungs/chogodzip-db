# json 활용
import requests # 크롤링에 사용하는 패키지
from bs4 import BeautifulSoup # html 변환에 사용함
import time
import json

cur_page_num = 1 # 현재 페이지 번호
data_cnt = 0 # 가져온 데이터 개수
while(1):
    # 카테고리 데이터 가져오기
    url = f'https://api.gobang.kr/v1/houses?%7B%22HOUSE_TYPE_CDS%22%3A%5B%22HOUTP00002%22%5D%2C%22DONGLI_CDS%22%3A%5B%2211%22%5D%2C%22PAGE_NUM%22%3A{cur_page_num}%2C%22randomSeed%22%3A5596%7D'
    https://api.gobang.kr/v1/houses?%7B%22HOUSE_TYPE_CDS%22%3A%5B%22HOUTP00002%22%5D%2C%22DONGLI_CDS%22%3A%5B%2211%22%5D%2C%22PAGE_NUM%22%3A1%2C%22randomSeed%22%3A5596%7D
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
        print(house["NAME"])
        data_cnt = data_cnt + 1

    # 만약 다음 페이지가 없는 경우 (==hasMore 값이 false 인 경우) 페이지 종료
    if json_data["hasMore"] == False:
        break
    else: # 다음 페이지가 있는 경우 다음 페이지 json 데이터 보기
        cur_page_num = cur_page_num + 1


print("============작업 정상 종료!!================")
print(f"총 데이터 개수 : {data_cnt}")