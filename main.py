import requests  # HTTP 요청을 보내는 모듈
import json  # json 파일 파싱하여 데이터 읽는 모듈
import datetime  # 날짜시간 모듈
from datetime import date, datetime, timedelta  # 현재 날짜 외의 날짜 구하기 위한 모듈
import sys # 출력결과 파일에 저장 (업데이트 형식으로 저장)
import math

# 날씨
# 기상청_동네 예보 조회 서비스 api 데이터 url 주소
vilage_weather_url ="http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getVilageFcst?"

# 발급 받은 인증키 (Encoding Key) - secret.json 파일에 저장한 key값 읽음
with open('secret.json') as json_file:
    json_data = json.load(json_file)
    json_string1 = json_data["tmp_key"]
    json_string2 = json_data["air_key"]
# print(json_data)
weather_key = json_string1
dust_key = json_string2
# print(service_key)

##############################################

with open('secret.json') as json_file:
    json_data = json.load(json_file)
    json_string3 = json_data["kakao_rest_key"]
client_id = json_string3

def mapToGrid(lat, lon, code=0):
    NX = 149  ## X축 격자점 수
    NY = 253  ## Y축 격자점 수
    Re = 6371.00877  ##  지도반경
    grid = 5.0  ##  격자간격 (km)
    slat1 = 30.0  ##  표준위도 1
    slat2 = 60.0  ##  표준위도 2
    olon = 126.0  ##  기준점 경도
    olat = 38.0  ##  기준점 위도
    xo = 210 / grid  ##  기준점 X좌표
    yo = 675 / grid  ##  기준점 Y좌표
    first = 0

    if first == 0:
        PI = math.asin(1.0) * 2.0
        DEGRAD = PI / 180.0
        RADDEG = 180.0 / PI

        re = Re / grid
        slat1 = slat1 * DEGRAD
        slat2 = slat2 * DEGRAD
        olon = olon * DEGRAD
        olat = olat * DEGRAD

        sn = math.tan(PI * 0.25 + slat2 * 0.5) / math.tan(PI * 0.25 + slat1 * 0.5)
        sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
        sf = math.tan(PI * 0.25 + slat1 * 0.5)
        sf = math.pow(sf, sn) * math.cos(slat1) / sn
        ro = math.tan(PI * 0.25 + olat * 0.5)
        ro = re * sf / math.pow(ro, sn)
        first = 1

    ra = math.tan(PI * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > PI:
        theta -= 2.0 * PI
    if theta < -PI:
        theta += 2.0 * PI
    theta *= sn
    x = (ra * math.sin(theta)) + xo
    y = (ro - ra * math.cos(theta)) + yo
    x = int(x + 1.5)
    y = int(y + 1.5)
    return x, y

def get_coordinates(address):
    # API_KEY_1 (카카오톡 developers)
    api_key_1 = client_id
    url = f"https://dapi.kakao.com/v2/local/search/address.json?query={address}"
    headers = {"Authorization": f"KakaoAK {api_key_1}"}
    response = requests.get(url, headers=headers)
    response_json = response.json()

    if "documents" in response_json:
        documents = response_json["documents"]
        if documents:
            first_result = documents[0]
            x = first_result["x"]
            y = first_result["y"]
            return x, y
    return None
##############################################
now = datetime.now()
print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")

# print("주소와 위도 경도를 입력하시오.")
print("주소를 입력하시오.")
# print("ex. 충북 청주시 가경동")
print("ex. 충청북도 청주시 가경동")
# print("ex. 충북대 (68 106)")
print("(입력) : ", end="")
address = input()
sidoName1, sidoName2, dongName= address.split()
# do = sidoName1, si = sidoName2.replace('시', '')

print("(1) 오늘의 날씨/미세먼지 정보")
print("(2) 날씨에 따른 옷 추천")
print("(선택) : ")
UserChoice =  int(input())

coordinates = get_coordinates(address)

if coordinates:
    longitude, latitude = map(float, coordinates)
    # print(latitude,longitude)
	#map(float, coordinates)는 coordinates 리스트의 각 요소를 float로 변환하는 함수
    #grid_value_x, grid_value_y = mapToGrid(latitude, longitude) #순서에 맞게 경도 위도 변경
    grid_value_x, grid_value_y = mapToGrid(latitude, longitude)
    nx = int(grid_value_x)
    ny = int(grid_value_y)
    nx = str(nx)
    ny = str(ny)

# 오늘
today = datetime.today()  # 현재 지역 날짜 반환
today_date = today.strftime("%Y%m%d")  # 오늘의 날짜 (연도/월/일 반환)
print('오늘의 날짜는', today_date)

# 어제
yesterday = date.today() - timedelta(days=1)
yesterday_date = yesterday.strftime('%Y%m%d')
print('어제의 날짜는', yesterday_date)

# 1일 총 8번 데이터가 업데이트 (0200, 0500, 0800, 1100, 1400, 1700, 2000, 2300)
# 현재 api를 가져오려는 시점의 이전 시각에 업데이트된 데이터를 base_time, base_date로 설정
if now.hour<2 or (now.hour==2 and now.minute<=10): # 0시~2시 10분 사이
    base_date=yesterday_date # 구하고자 하는 날짜가 어제의 날짜
    base_time="2300"
elif now.hour<5 or (now.hour==5 and now.minute<=10): # 2시 11분~5시 10분 사이
    base_date=today_date
    base_time="0200"
elif now.hour<8 or (now.hour==8 and now.minute<=10): # 5시 11분~8시 10분 사이
    base_date=today_date
    base_time="0500"
elif now.hour<=11 or now.minute<=10: # 8시 11분~11시 10분 사이
    base_date=today_date
    base_time="0800"
elif now.hour<14 or (now.hour==14 and now.minute<=10): # 11시 11분~14시 10분 사이
    base_date=today_date
    base_time="1100"
elif now.hour<17 or (now.hour==17 and now.minute<=10): # 14시 11분~17시 10분 사이
    base_date=today_date
    base_time="1400"
elif now.hour<20 or (now.hour==20 and now.minute<=10): # 17시 11분~20시 10분 사이
    base_date=today_date
    base_time="1700"
elif now.hour<23 or (now.hour==23 and now.minute<=10): # 20시 11분~23시 10분 사이
    base_date=today_date
    base_time="2000"
else: # 23시 11분~23시 59분
    base_date=today_date
    base_time="2300"

base_date = str(base_date)
base_time = str(base_time)
weather_key = str(weather_key)
payload = "dataType=JSON" + "&" + "serviceKey=" + weather_key + "&" + "base_date=" + base_date + "&" + "base_time=" + base_time + "&" + "nx=" + nx + "&" + "ny=" + ny
# print(vilage_weather_url + payload)

# 값 요청 (웹 브라우저 서버에서 요청 - url주소와 + 필요한 데이터값 )
response = requests.get(vilage_weather_url + payload)

items = response.json().get('response').get('body').get('items')

data = dict()
data['date'] = base_date

weather_data = dict()
for item in items['item']:
    # 기온
    if item['category'] == 'TMP':
        weather_data['tmp'] = item['fcstValue']

    # 기상상태
    if item['category'] == 'PTY':

        weather_code = item['fcstValue']

        if weather_code == '1':
            weather_state = '비'
        elif weather_code == '2':
            weather_state = '비/눈'
        elif weather_code == '3':
            weather_state = '눈'
        elif weather_code == '4':
            weather_state = '소나기'
        else:
            weather_state = '없음'

        weather_data['code'] = weather_code
        weather_data['state'] = weather_state

data['weather'] = weather_data

print()
# for i in data:
#    print(data[i])
# ex) {'code': '0', 'state': '없음', 'tmp': '17'} # 17도 / 기상 이상 없음

state = data['weather']['state']

# 위는 날씨 관련
# 아래는 미세먼지 관련
dust_url = "http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty?"

# 응답메시지 시도명 -> API에 맞는 값으로 변경
# 가능한 시도 이름 (서울, 부산, 대구, 인천, 광주, 대전, 울산, 경기, 강원, 충북, 충남, 전북, 전남, 경북, 경남, 제주, 세종)
if (sidoName1 == '서울시'): sido = '서울'
elif (sidoName1 == '서울') :sido = '서울'
elif (sidoName1 == '서울특별시') :sido = '서울'
elif (sidoName1 == '부산시') :sido = '부산'
elif (sidoName1 == '부산광역시') :sido = '부산'
elif (sidoName1 == '부산') :sido = '부산'
elif (sidoName1 == '대구시'): sido = '대구'
elif (sidoName1 == '대구광역시'): sido = '대구'
elif (sidoName1 == '대구'): sido = '대구'
elif (sidoName1 == '인천시'): sido = '인천'
elif (sidoName1 == '인천광역시'): sido = '인천'
elif (sidoName1 == '인천'): sido = '인천'
elif (sidoName1 == '광주시'): sido = '광주'
elif (sidoName1 == '광주광역시'): sido = '광주'
elif (sidoName1 == '광주'): sido = '광주'
elif (sidoName1 == '대전시'): sido = '대전'
elif (sidoName1 == '대전광역시'): sido = '대전'
elif (sidoName1 == '대전'): sido = '대전'
elif (sidoName1 == '울산시'): sido = '울산'
elif (sidoName1 == '울산광역시'): sido = '울산'
elif (sidoName1 == '울산'): sido = '울산'
elif (sidoName1 == '제주시'): sido = '제주'
elif (sidoName1 == '제주특별시'): sido = '제주'
elif (sidoName1 == '제주'): sido = '제주'
elif (sidoName1 == '세종시'): sido = '세종'
elif (sidoName1 == '세종특별시'): sido = '세종'
elif (sidoName1 == '세종'): sido = '세종'
elif (sidoName1 == '경기도'): sido = '경기'
elif (sidoName1 == '경기'): sido = '경기'
elif (sidoName1 == '강원도'): sido = '강원'
elif (sidoName1 == '강원'): sido = '강원'
elif (sidoName1 == '충청북도'): sido = '충북'
elif (sidoName1 == '충북'): sido = '충북'
elif (sidoName1 == '충청남도'): sido = '충남'
elif (sidoName1 == '충남'): sido = '충남'
elif (sidoName1 == '전라북도'): sido = '전북'
elif (sidoName1 == '전북'): sido = '전북'
elif (sidoName1 == '전라남도'): sido = '전남'
elif (sidoName1 == '전남'): sido = '전남'
elif (sidoName1 == '경상북도'): sido = '경북'
elif (sidoName1 == '경북'): sido = '경북'
elif (sidoName1 == '경상남도'): sido = '경남'
elif (sidoName1 == '경남'): sido = '경남'

# print("지금은", now.year, "년", now.month, "월", now.day, "일", now.hour, "시", now.minute, "분", now.second, "초입니다.")
now = datetime.now()
today_datetime = now.strftime('%Y-%m-%d')  # 오늘의 날짜 (연도/월/일 시:분 반환)

if now.hour<6 or (now.hour==6 and now.minute<=10): # 0시~6시 10분 사이
    today_datetime = today_datetime + ' 00:00'
elif now.hour<12 or (now.hour==12 and now.minute<=10): # 6시 11분~12시 10분 사이
    today_datetime = today_datetime + ' 06:00'
elif now.hour<18 or (now.hour==18 and now.minute<=10): # 12시 11분~18시 10분 사이
    today_datetime = today_datetime + ' 12:00'
else: # 18시 11분~23시 59분
    today_datetime = today_datetime + ' 18:00'

payload = "serviceKey=" + dust_key + "&" +\
    "returnType=json" + "&" +\
    "dataTime=" + today_datetime + "&" +\
    "sidoName=" + sido + "&" +\
    "ver=1.0" + "&" +\
    "informCode="

# pm10 수치 가져오기
pm10_res = requests.get(dust_url + payload + 'pm10Value')
items = pm10_res.json().get('response').get('body').get('totalCount')
dust_data = items

# PM10 미세먼지 30 80 150
pm10_value = dust_data
if pm10_value <= 30:
    pm10_state = "좋음"
elif pm10_value <= 80:
    pm10_state = "보통"
elif pm10_value <= 150:
    pm10_state = "나쁨"
else:
    pm10_state = "매우나쁨"

# 출력결과 파일에 저장
sys.stdout = open('stdout.txt', 'w', encoding="UTF-8") # 파일 열기, 인코딩 utf-8로 설정
# 아래는 날씨 관련 출력문
print(data['date'][0:4], '년', data['date'][4:6], '월', data['date'][6:8], '일', base_time, '시의 날씨 데이터입니다.')
print("위치 :", sidoName1, sidoName2, dongName)
print("기온 :", data['weather']['tmp'], "도")

if state == '비':
    print('비가 옵니다. 우산을 꼭 챙겨주세요.')
elif state == '비/눈':
    print('비 또는 눈이 옵니다. 우산을 챙겨주세요.')
elif state == '눈':
    print('눈이 옵니다. 빙판 길 조심하십시오.')
elif state == '소나기':
    print('소나기 주의. 우산을 꼭 챙겨주세요.')
else:
    print('날씨가 화창합니다.')

# 아래는 미세먼지 관련 출력문
print("미세먼지는", dust_data, pm10_state, "입니다.")
sys.stdout.close() # 파일 닫기

#################################################################
# 카카오톡 연결
import requests
import json

def kakao1():
    # 발행한 토큰 불러오기
    with open("token.json", "r") as kakao:
        tokens = json.load(kakao)

    # 카카오톡 URL 주소
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    # 날씨 상세 정보 URL
    weather_url = "https://www.weather.go.kr/"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " + tokens["access_token"]
    }

    # 날씨, 미세먼지 값 읽기
    file = open('stdout.txt', 'r', encoding="utf-8")
    printText = file.read()
    file.close()

    template = {
        "template_object": json.dumps({
            "object_type": "text",
            "text": printText,
            "link": {
                "web_url": weather_url,
                "mobile_web_url": weather_url
            },
            "button_title": "확인"
        })
    }

    """
    # JSON 형식 -> 문자열 변환
    payload = {
        "template_object" : json.dumps(template)
    }
    """

    # 카카오톡 보내기
    # data = {'template_object': json.dumps(template)}
    response = requests.post(url, headers=headers, data=template)
    response.status_code

    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

######## 무신사 실시간 랭킹 크롤링 과정

from urllib.request import urlopen
from bs4 import BeautifulSoup

def scrapping(category_num):
    # category_num=input("Category 번호를 입력하세요: ")
    url = f"https://www.musinsa.com/ranking/best?period=now&age=ALL&mainCategory="
    urladd = category_num
    #해당 url을 오픈합니다.
    html = urlopen(url + urladd)
    bsObject = BeautifulSoup(html, "html.parser")

    #상품들의 정보가 담긴 li_box를 모두 가져옵니다.
    item_list = bsObject.findAll('li',{'class':'li_box'})

    # 빈리스트를 만들어 줍니다.
    brand = []
    name = []
    link = []
    number = []
    number_box = 0  # 이걸로 순위를 카운트합니다.

    for item in item_list:
        # 브랜드 담기
        brand_box = item.findAll('p', {'class': 'item_title'})
        if len(brand_box) == 1:
            brand.append(brand_box[0].get_text())
        elif len(brand_box) == 2:
            brand.append(brand_box[1].get_text())
        # 상품명 담기
        name_box = item.findAll('p', {'class': 'list_info'})
        name.append(name_box)
        # 링크 담기
        link_box = item.find('a', {'class':'img-block'}).get('href')
        link.append(link_box)
        # 순위 담기
        number_box += 1
        number.append(str(number_box))

    ## 데이터 정제
    import pandas as pd

    data = {'순위': number, '브랜드': brand, '상품명': name, '링크': link}
    df = pd.DataFrame(data)
    final_df = df.loc[0:4]
    # final_df = final_df.set_index("순위") # 순위를 index로 보냄으로써 csv 파일 내에 순위 숫자 정보는 삭제
    if (category_num == '058007001' or category_num == '011011' or category_num == '009001' or category_num == '002013' or category_num == '007'):
        c_num = '000'
    else:
        c_num = category_num[0] + category_num[1] + category_num[2]
    file_name = f"musinsa_ranking_category{c_num}.csv"
    final_df.to_csv(file_name, index=False, encoding='utf-8')
    pd.read_csv(file_name)

scrapping('001') # 상의 top 5 추출
scrapping('003') # 하의 top 5 추출
scrapping('005') # 신발 top 5 추출

if ((((weather_state == '비') or (weather_state == '비/눈')) or (weather_state == '소나기')) and (int(data['weather']['tmp']) >= 25)):
    scrapping('058007001')  # 우산 추천
elif (((weather_state == '비/눈') or (weather_state == '눈')) or (int(data['weather']['tmp']) <= 5)):
    scrapping('011011')  # 장갑 추천
elif ((weather_state != '비') and (weather_state != '눈') and (weather_state != '소나기') and (int(data['weather']['tmp']) >= 25)):
    scrapping('009001')  # 썬글라스 추천
elif (int(data['weather']['tmp']) < 0):
    scrapping('002013')  # 패딩 추천
else:
    scrapping('007')  # 모자 추천

########## 옷 추천 카톡 전송

###### csv 파일 불러오기
import csv
import random

def top_recommend():
    with open('musinsa_ranking_category001.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        random_data = random.choice(data)
        link = random_data['링크']
        return link

def pants_recommend():
    with open('musinsa_ranking_category003.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        random_data = random.choice(data)
        link = random_data['링크']
        return link

def shoes_recommend():
    with open('musinsa_ranking_category005.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        random_data = random.choice(data)
        link = random_data['링크']
        return link

def extra_recommend():
    with open('musinsa_ranking_category000.csv', 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        data = list(reader)
        random_data = random.choice(data)
        link = random_data['링크']
        return link

################## 카톡
import requests
import json

def kakao2():
    # 발행한 토큰 불러오기
    with open("token.json", "r") as kakao:
        tokens = json.load(kakao)

    # 카카오톡 URL 주소
    url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    # 날씨 상세 정보 URL
    weather_url = "https://www.weather.go.kr/"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Bearer " + tokens["access_token"]
    }

    # 리스트 템플릿 형식 만들기
    contents = []
    template = {
        "object_type" : "list",
        "header_title" : "현재 날씨에 따른 옷차림 추천",
        "header_link" : {
            "web_url": weather_url,
            "mobile_web_url" : weather_url
        },
        "contents" : contents,
        "buttons" : [
            {
                "title" : "날씨 정보 상세보기",
                "link" : {
                    "web_url": weather_url,
                    "mobile_web_url" : weather_url
                }
            }
        ]
    }

    # contents 만들기
    recommends = []
    top = top_recommend()
    pants = pants_recommend()
    shoes = shoes_recommend()
    extra = extra_recommend()
    recommends.append('상의 추천')
    recommends.append(top)
    recommends.append('https://kuku-keke.com/wp-content/uploads/2020/04/2486_4-550x550.png')
    recommends.append('하의 추천')
    recommends.append(pants)
    recommends.append('https://kuku-keke.com/wp-content/uploads/2020/04/2492_6-768x998.png')
    #recommends.append('신발 추천')
    #recommends.append(shoes)
    #recommends.append('https://kuku-keke.com/wp-content/uploads/2020/04/2514_5-768x632.png')
    recommends.append('오늘의 추천 아이템')
    recommends.append(extra)
    recommends.append('https://littledeep.com/wp-content/uploads/2021/06/weather-illustration-main.png')

    from PIL import Image

    for i in range(0, 8, 3):
        title = recommends[i]
        link = recommends[i+1]
        image_URL = recommends[i+2]
        content = {
            "title": title,
            "image_url": image_URL,
            "image_width": 50, "image_height": 50,
            "link": {
                "web_url": link,
                "mobile_web_url": link
            }
        }
        contents.append(content)
    # contents 추가
    template["contents"] = contents

    # JSON 형식 -> 문자열 변환
    payload = {
        "template_object": json.dumps(template)
    }

    # 카카오톡 보내기
    response = requests.post(url, headers=headers, data=payload)

    if response.json().get('result_code') == 0:
        print('메시지를 성공적으로 보냈습니다.')
    else:
        print('메시지를 성공적으로 보내지 못했습니다. 오류메시지 : ' + str(response.json()))

if(UserChoice == 1):
    kakao1()
elif(UserChoice == 2):
    kakao2()
else:
    kakao1()