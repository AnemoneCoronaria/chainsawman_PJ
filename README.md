
pip 패키지 설치
pip install Flask Flask-Login Flask-SQLAlchemy PyMySQL


* app.py
  메인 flask 앱
  프로그램의 진입점
  앱 전체를 실행시키는 파일

* login_manager.py
  Flask_Login 초기화
  사용자 로그인 상태 관리
  사용자 세션 관리 전용 모듈

* controllers.py
  URI와 View를 연결
  라우팅 정의
  사용자 요청과 화면을 연결, DB 쿼리 담당

* models.py
  DB 테이블 정의
  SQLAlchemy를 사용해 Flask ORM으로 DB 모델 정의
  각 테이블과 컬럼 구조를 정의 --->  Python 객체로 DB 조작 가능



