# 사내 데이터 관리 웹 (Django + PostgreSQL)

좋아요. 웹 부분을 **Django** 기반으로 바꿨습니다.
엑셀의 한계를 대체하기 위해, 회사 사용자가 로그인 후 데이터 입력/조회/수정/삭제를 할 수 있는 서버 렌더링 웹 앱입니다.

## 주요 기능
- Django 기본 인증 기반 로그인/로그아웃
- 사용자별 데이터 CRUD (본인 데이터만 접근)
- 데이터 조회 시 정렬/필터링
  - 정렬: 등록일, 금액, 제목, 카테고리
  - 필터: 카테고리, 검색어, 최소/최대 금액
- PostgreSQL 연동

## 기술 스택
- Django 5
- PostgreSQL
- Bootstrap 5 (템플릿 UI)

## 실행 방법
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

접속: `http://127.0.0.1:8000`

## URL
- `/accounts/login/` : 로그인
- `/accounts/logout/` : 로그아웃
- `/` : 대시보드 (입력/조회/정렬/필터링/수정/삭제)
- `/admin/` : 관리자
