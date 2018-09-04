# ydp_alarm_with_kakaoApi입니다.

이 폴더는 카카오톡 플러스 친구를 이용한 영등포고등학교 알람서비스인 ydpalarm에 사용된 것들입니다.
업데이트 정보를 확인하려면 patchNote를 확인하세요.

◎ 제공중인 서비스
1. 오늘의 급식
	- 중식
	- 석식
: 오늘의 급식을 '나이스'로부터 정보를 받아와 출력합니다
- url : http://stu.sen.go.kr/sts_sci_md01_001.do?

파서 출처 : M4ndU님 블로그, github
- github_url : https://github.com/M4ndU/school_meal_parser_python
- M4ndU'blog : http://mandu-mandu.tistory.com/category/Project/Programming

2. 스포츠 리그 일정표
: 스포츠 리그의 일정표 이미지로 출력합니다. ( 카카오톡 링크로, 사진 확대가 불가능합니다. 개선할 계획입니다.)

3. 시간표
: 오늘의 시간표를 출력합니다.
	- : 현재 시간표는 2학년만 출력 가능합니다. 오타지적 감사히 받겠습니다.

4. 개발정보
: 개발하기까지 참고한 사이트, 블로그 , 분들께 감사를 표하는 기능입니다.

5. 선생님 교무실 위치
: 선생님의 교무실 위치를 라벨별 출력합니다(이스터에그 존재).

6. 공지사항 버튼 추가
: 학교에서 중요한 내용을 받아, 받은 날 자정 업데이트 됩니다. 

◎ 추가 예정인 기능
1. 오늘의 경기
: 오늘의 스포츠리그 경기를 추가하여 알려줍니다.

◎ 삭제된 기능
1. 오늘의 명언 (다음 업데이트에 오류수정 실패시 삭제될수 있습니다)
: 오늘의 명언을 naver로부터 정보를 받아와 출력합니다. (현재 HTTP ERROR 403으로 임시 명언)
- url : https://search.naver.com/search.naver?where=nexearch&sm=tab_etc&mra=blMy&query=%EA%B3%B5%EB%B6%80%20%EB%AA%85%EC%96%B8


◎ 파이썬 사용 모듈
- BeautifulSoup4
- regex
- datetime
- requests
- re
- random
- openurl

◎ ubuntu 사용 프로그램
- python
- apache
- Django
- venv

◎ 주로 사용한 ubuntu 명령어
- vi
- cd
- sudo apachectl -k restart
- crontab (시간이 UTC 0에 맞춰져 있어 crontab 사용시 주의)
- mkdir
- cp
- touch

◎ 서버
- Amazon Web Services Cloud
