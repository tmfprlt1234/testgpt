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

> 기본 설정은 SQLite(`USE_SQLITE=True`, `USE_POSTGRES=False`)라서 `.env.example` 복사 직후에도 `migrate`가 바로 동작합니다.

## 로컬 기본 실행(SQLite)
아무 설정을 바꾸지 않으면 SQLite로 실행됩니다.
```env
USE_SQLITE=True
USE_POSTGRES=False
```


## PostgreSQL로 실행
`.env`에서 아래처럼 바꾼 뒤 실행하세요.
```env
USE_SQLITE=False
USE_POSTGRES=True
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/company_data
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

5. PowerShell/cmd에 이전에 설정된 `PGPASSWORD`, `PGUSER`, `PGHOST` 같은 `PG*` 환경변수가 있다면 제거 후 재실행
6. `%APPDATA%\postgresql\pgpass.conf` 또는 서비스 설정(`PGSERVICE`)이 깨져있다면 임시로 비활성화
   - `POSTGRES_SERVICE`, `POSTGRES_PASSFILE`은 빈 문자열(`""`)로 두지 말고 완전히 비워두거나(미설정), 실제 값만 입력


추가 우회 방법(Windows 인코딩 충돌 시):
```env
# 비밀번호를 UTF-8 기준 Base64로 저장
POSTGRES_PASSWORD_B64=
```

예) 비밀번호가 `비밀번호123!`일 때 (Python):
```python
import base64
print(base64.b64encode("비밀번호123!".encode("utf-8")).decode())
```

예시:
```env
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/company_data
PGCLIENTENCODING=UTF8
POSTGRES_OPTIONS=-c client_encoding=UTF8
POSTGRES_DISABLE_PGSERVICE=True
POSTGRES_DISABLE_PGPASSFILE=True
```

> 참고: `staticfiles.W004` 경고는 `static/` 폴더가 없을 때 발생합니다. 본 프로젝트에는 기본 `static/` 폴더가 포함되어 있습니다.

## URL
- `/accounts/login/` : 로그인
- `/accounts/logout/` : 로그아웃
- `/` : 대시보드 (입력/조회/정렬/필터링/수정/삭제)
- `/admin/` : 관리자
