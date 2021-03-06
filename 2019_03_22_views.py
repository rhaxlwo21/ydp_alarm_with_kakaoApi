from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import requests, re
from bs4 import BeautifulSoup
import datetime
from urllib.request import urlopen, Request
import regex
import random
import urllib
dt1 = datetime.datetime.today()
todate = dt1.strftime("%Y.%m.%d")

t = ['월','화','수','목','금','토','일',]
r = datetime.datetime.today().weekday()


def get_diet(code, ymd, weekday):
    schMmealScCode = code #int 1조식2중식3석식
    schYmd = ymd #str 요청할 날짜 yyyy.mm.dd
    if weekday == 5 or weekday == 6: #토요일,일요일 버림
        element = " " #공백 반환
    else:
        num = weekday + 1 #int 요청할 날짜의 요일 0월1화2수3목4금5토6일 파싱한 데이터의 배열이 일요일부터 시작되므로 1을 더해줍니다.
        URL = (
                "http://stu.sen.go.kr/sts_sci_md01_001.do?"
                "schulCode=B100000497"
                "&schulCrseScCode=4"
                "&schulKndScCode=04"
                "&schMmealScCode=%d&schYmd=%s" % (schMmealScCode, schYmd)
            )
        #http://stu.AAA.go.kr/ 관할 교육청 주소 확인해주세요.
        #schulCode= 학교고유코드
        #schulCrseScCode= 1유치원2초등학교3중학교4고등학교
        #schulKndScCode= 01유치원02초등학교03중학교04고등학교

        #기존 get_html 함수부분을 옮겨왔습니다.
        html = ""
        resp = requests.get(URL)
        if resp.status_code == 200 : #사이트가 정상적으로 응답할 경우
            html = resp.text
        soup = BeautifulSoup(html, 'html.parser')
        element_data = soup.find_all("tr")
        element_data = element_data[2].find_all('td')
        try:
            element = str(element_data[num])

            #filter
            element_filter = ['[', ']', '<td class="textC last">', '<td class="textC">', '</td>', '&amp;', '(h)', '.']
            for element_string in element_filter :
                element = element.replace(element_string, '')
            #줄 바꿈 처리
            element = element.replace('<br/>', '\n')
            #모든 공백 삭제
            element = re.sub(r"\d", "", element)

        #급식이 없을 경우
        except:
            element = "급식이 먹고싶나?\n급식이 없다네 핳핳" # 공백 반환
    return element
    
meal1 = get_diet(2, todate, r) #중식, 2017년 11월 17일, 금요일
meal2 = get_diet(3, todate, r)

mealD = ""
mealM = ""
bar = "=====오늘의 급식=====\n"
error = "주말과 공휴일에는\n아무것도 나타나지 않아욥!"
mealM += todate+ t[r] + "요일\n" + bar + "중식\n"+ meal1+ bar + error
mealD += todate+ t[r] + "요일\n" + bar + "석식\n" + meal2 +bar + error
#========================================오늘의급식end
#========================================명언
ranNum = random.randint(0,9)
wsurl_base = 'https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blMy&query='
wsurl_mid = ['%EC%82%AC%EB%9E%91','%EC%9D%B8%EC%83%9D','%EA%B3%B5%EB%B6%80','%EC%84%B1%EA%B3%B5','%EC%B9%9C%EA%B5%AC','%EB%8F%85%EC%84%9C','%EC%9D%B4%EB%B3%84','%EC%8B%9C%EA%B0%84','%EB%85%B8%EB%A0%A5','%ED%9D%AC%EB%A7%9D','%EB%8F%84%EC%A0%84','%EC%9E%90%EC%8B%A0%EA%B0%90']
wsurl_tail = '%20%EB%AA%85%EC%96%B8'

url = wsurl_base + wsurl_mid[ranNum] + wsurl_tail
hdr = {'referer': wsurl_base + wsurl_mid[ranNum] + wsurl_tail, 'User-Agent':'Mozilla/5.0', 'referer' : 'http://www.naver.com'}
req = Request(url, headers=hdr)
page = urlopen(req)

wsSoup = BeautifulSoup(page,'html.parser')
wsText = wsSoup.find('p','lngkr').get_text()
wsMan = wsSoup.find('span','engnm').get_text()


var = '\n=======================\n'
wsTotal = '명언' + var + wsText + var + '          -' + wsMan + '-'
#========================================명언end
#========================================미세먼지, 초미세먼지
url_base = 'https://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query='
url_syb1 = '%EB%8F%99%EC%9E%91%EA%B5%AC+%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'
url_syb2 = '%EB%8F%99%EC%9E%91%EA%B5%AC+%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80'

PM10url = url_base + url_syb1
PM25url = url_base + url_syb2
hdr1 = {'referer': url_base + url_syb1, 'User-Agent':'Mozilla/5.0', 'referer' : 'http://www.naver.com'}
hdr2 = {'referer': url_base + url_syb2, 'User-Agent':'Mozilla/5.0', 'referer' : 'http://www.naver.com'}

req1 = Request(PM10url, headers=hdr1)
page1 = urlopen(req1)
req2 = Request(PM25url, headers=hdr2)
page2 = urlopen(req2)

soup1 = BeautifulSoup(page1,'html.parser')
soup2 = BeautifulSoup(page2,'html.parser')

pm10 = soup1.find('em','main_figure').get_text()
pm25 = soup2.find('em','main_figure').get_text()

if(int(pm25)<=15):
    warning1 = '\n상태 : 좋음\n\n일반인 : 굳'
elif(16<=int(pm25) and int(pm25)<=35):
    warning1 = '\n상태 : 보통\n\n민감군 : 실외활동 시 특별히 행동에 제약은 없으나 몸 상태에 따라 유의하여 활동'
elif(36<=int(pm25) and int(pm25)<=75):
   warning1 = '\n상태 : 나쁨\n\n일반인 : 장시간 또는 무리한 실외활동 제한, 특히 눈이 아프거나, 기침, 목의 통증으로 불편한 사람은 실외활동을 피해야 함\n\n민감군 : 장시간 또는 무리한 실외활동 제한, 특히 천식환자는 실외활동 시 흡입기를 더 자주 사용할 필요가 있음'
elif(76<=int(pm25)):
    warning1 = '\n상태 : 매우나쁨\n\n일반인 : 장시간 또는 무리한 실외 활동제한, 기침이나 목의 통증 등이 있는 사람은 실외활동을 피해야 함\n\n민감군 : 가급적 실내 활동만 하고 실외 활동시 의사와 상의'

if(int(pm10)<=30):
    warning2 = '\n상태 : 좋음\n\n일반인 : 굳'
elif(31<=int(pm10) and int(pm10)<=80):
    warning2 = '\n상태 : 보통\n\n민감군 : 실외활동 시 특별히 행동에 제약은 없으나 몸 상태에 따라 유의하여 활동'
elif(81<=int(pm10) and int(pm10)<=150):
   warning2 = '\n상태 : 나쁨\n\n일반인 : 장시간 또는 무리한 실외활동 제한, 특히 눈이 아프거나, 기침, 목의 통증으로 불편한 사람은 실외활동을 피해야 함\n\n민감군 : 장시간 또는 무리한 실외활동 제한, 특히 천식환자는 실외활동 시 흡입기를 더 자주 사용할 필요가 있음'
elif(151<=int(pm10)):
    warning2 = '\n상태 : 매우나쁨\n\n일반인 : 장시간 또는 무리한 실외 활동제한, 기침이나 목의 통증 등이 있는 사람은 실외활동을 피해야 함\n\n민감군 : 가급적 실내 활동만 하고 실외 활동시 의사와 상의'

resultpm25 = '동작구 초미세먼지: ' + pm25 + warning1 + '\n\nhttps://search.naver.com/search.naver?sm=top_hty&fbm=1&ie=utf8&query=%EB%8F%99%EC%9E%91%EA%B5%AC+%EC%B4%88%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80 에서 수집된 정보이고, 사이트별로 오차가 있을수 있습니다.'
resultpm10 = '동작구 미세먼지: ' + pm10 + warning2 + '\n\nhttps://search.naver.com/search.naver?sm=top_hty&fbm=0&ie=utf8&query=%EB%8F%99%EC%9E%91%EA%B5%AC+%EB%AF%B8%EC%84%B8%EB%A8%BC%EC%A7%80 에서 수집된 정보이고, 사이트별로 오차가 있을수 있습니다.'
#========================================미세먼지, 초미세먼지end
#========================================시간표
sub = t[r] + "요일 시간표\n"
bar = "==========\n"
danger = "시간표가변경될수있습니다.\n오타제보 1대1 상담으로 부탁드립니다."
#========================================class기틀end
#=================================class33
if t[r] == "월":
    classTime33 = "1교시: 영A\n2교시: 논술\n3교시: 사문\n4교시: 확통\n5교시: 작B\n6교시: 역사\n7교시: 체육\n"
elif t[r] == "화":
    classTime33 = "1교시: 진로\n2교시: 작A\n3교시: 한문\n4교시: 확통\n5교시: 사문\n6교시: 생윤\n7교시: 영A\n"
elif t[r] == "수":
    classTime33 = "1교시: 체육\n2교시: 생윤\n3교시: 한지\n4교시: 영A\n5교시: 사문\n6교시: 작B\n"
elif t[r] == "목":
    classTime33 = "1교시: 영B\n2교시: 역사\n3교시: 한지\n4교시: 작B\n5교시: 지학\n6교시: 확통\n7교시: 작A\n"
elif t[r] == "금":
    classTime33 = "1교시: 역사\n2교시: 한지\n3교시: 영B\n4교시: 생윤\n5교시: 창체\n6교시: 창체\n"
elif t[r] == "토" or "일":
    classTime33 = "토,일요일은 수업이 없습니다\n"

class33 = sub + bar + classTime33 + bar + danger
#===============================class33end
#=================================class35
if t[r] == "월":
    classTime35 = "1교시: 법정\n2교시: 기벡\n3교시: 작B\n4교시: 역사\n5교시: 작A\n6교시: 영A\n7교시: 한문\n"
elif t[r] == "화":
    classTime35 = "1교시: 지학\n2교시: 기벡\n3교시: 영A\n4교시: 환경\n5교시: 작A\n6교시: 역사\n7교시: 작B\n"
elif t[r] == "수":
    classTime35 = "1교시: 역사\n2교시: 법정\n3교시: 생물\n4교시: 영B\n5교시: 확통\n6교시: 체육\n"
elif t[r] == "목":
    classTime35 = "1교시: 생물\n2교시: 영B\n3교시: 기벡\n4교시: 작B\n5교시: 영A\n6교시: 법정\n7교시: 지학\n"
elif t[r] == "금":
    classTime35 = "1교시: 진로\n2교시: 생물\n3교시: 체육\n4교시: 확통\n5교시: 창체\n6교시: 창체\n"
elif t[r] == "토" or "일":
    classTime35 = "토,일요일은 수업이 없습니다\n"
    
class35 = sub + bar + classTime35 + bar + danger
#===============================class35end

def keyboard(request):

    return JsonResponse({
        'type':'buttons',
        'buttons':['급식','오늘의 명언','미세먼지-초미세먼지','시간표','영등포고등학교 홈페이지','변경사항','개발정보']
    })

@csrf_exempt
def message(request):

    json_str = ((request.body).decode('utf-8'))
    received_json_data = json.loads(json_str)
    datacontent = received_json_data['content']

    if datacontent == '급식':

        return JsonResponse({
                'message': {
                    'text': '아래 중식, 석식중 선택하세요'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['중식','석식']
                }
            })

    elif datacontent == '처음으로':

        return JsonResponse({
                'message': {
                    'text': '메인페이지'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['급식','오늘의 명언','미세먼지-초미세먼지','시간표','영등포고등학교 홈페이지','변경사항','개발정보']
                }
            })

    elif datacontent == '오늘의 명언':

        return JsonResponse({
                'message': {
                    'text': wsTotal
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '시간표':

        return JsonResponse({
                'message': {
                    'text': '반을 선택하세요.'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['3학년3반','3학년5반','다른반은?']
                }
            })

    elif datacontent == '개발정보':

        return JsonResponse({
                'message': {
                    'text': '개발자 : 20612서정현,20521장환곤\n인성스포츠 리그 권한 문제 해결 : 갓현석 선배\n오타300줄 : 김도유\n항상 조언해주시는 갓주현 선생님, 갓효진 선배,스포츠대회 일정 이미지 권한 문제 해결 유현석 선배님\n>모두 감사드립니다.\n\n명언 : NAVER에서 정보를 받아옴.\n급식: 나이스에서 받아옴\n시간표: 수제작\n\n자세한정보 : https://github.com/rhaxlwo21/ydp_alarm_with_kakaoApi/tree/master'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '영등포고등학교 홈페이지':

        return JsonResponse({
                'message': {
                    'text': '더 자세한 사항은 영등포고등학교 홈페이지를 참고하세요. \n홈페이지 주소 : http://www.ydp.hs.kr/index.do'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '중식':

        return JsonResponse({
                'message': {
                    'text': mealM
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '석식':

        return JsonResponse({
                'message': {
                    'text': mealD
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '변경사항':

        return JsonResponse({
                'message': {
                    'text': '선생님위치기능, 인성스포츠대회 일정(기상이변), 등 기능 삭제.\n초기 기획인 명언이 크롤링 오류 해결로 추가됨.\n\n2019년 5월말 혹은 6월초 금전적인 이유로 서비스 종료될 예정입니다 헣헣'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '미세먼지-초미세먼지':

        return JsonResponse({
                'message': {
                    'text': '선택하세요'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['미세먼지','초미세먼지']
                }
            })

    elif datacontent == '미세먼지':

        return JsonResponse({
                'message': {
                    'text': resultpm10
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '초미세먼지':

        return JsonResponse({
                'message': {
                    'text': resultpm25
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '3학년3반':

        return JsonResponse({
                'message': {
                    'text': class33
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '3학년5반':

        return JsonResponse({
                'message': {
                    'text': class35
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })

    elif datacontent == '다른반은?':

        return JsonResponse({
                'message': {
                    'text': '다른 반의 시간표가 필요하다면 1대1 상담으로 반의 시간표를 보내주세요.'
                },
                'keyboard': {
                    'type':'buttons',
                    'buttons':['처음으로']
                }
            })
