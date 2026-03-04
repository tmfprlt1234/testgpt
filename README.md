# 사내 데이터 관리 웹 (Django + PostgreSQL)

요청하신 대로 웹 부분은 **Django**로 구성했습니다.
엑셀의 한계를 대체하기 위해, 회사 사용자가 로그인 후 데이터 입력/조회/수정/삭제를 할 수 있는 서버 렌더링 웹 앱입니다.

## 주요 기능
- Django 기본 인증 기반 로그인/로그아웃
- 사용자별 데이터 CRUD (본인 데이터만 접근)
- 데이터 조회 시 정렬/필터링
  - 정렬: 등록일, 금액, 제목, 카테고리
  - 필터: 카테고리, 검색어, 최소/최대 금액
- PostgreSQL 연동 (운영)
- SQLite 모드 지원 (개발/테스트)

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

## 로컬 테스트용 SQLite
PostgreSQL이 없는 환경에서는 `.env`에 아래 값을 추가해 실행할 수 있습니다.
```env
USE_SQLITE=True
```

## 테스트
```bash
USE_SQLITE=True python manage.py test
```

## Windows에서 migrate 시 인코딩/연결 오류가 날 때
아래를 순서대로 점검하세요.

1. `.env` 파일을 **UTF-8(권장: UTF-8 with BOM)** 으로 저장
2. 비밀번호에 특수문자가 있으면 `DATABASE_URL`에는 URL 인코딩해서 입력
3. `.env`에 `PGCLIENTENCODING=UTF8` 설정
4. PostgreSQL 접속 확인 후 재실행

예시:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/company_data
PGCLIENTENCODING=UTF8
```

> 참고: `staticfiles.W004` 경고는 `static/` 폴더가 없을 때 발생합니다. 본 프로젝트에는 기본 `static/` 폴더가 포함되어 있습니다.

## URL
- `/accounts/login/` : 로그인
- `/accounts/logout/` : 로그아웃
- `/` : 대시보드 (입력/조회/정렬/필터링/수정/삭제)
- `/admin/` : 관리자
