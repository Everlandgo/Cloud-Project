# Cloud-Project
---

## 1. 필수 설치

아래 도구들이 설치되어 있어야 합니다.

* Git
* Docker
* Docker Compose

확인:

```bash
docker -v
docker-compose -v
git -v
```

---

## 2. 프로젝트 클론

```bash
git clone git@github.com:Everlandgo/Cloud-Project.git
cd Cloud-Project
```

---

## 3. Docker 이미지 빌드 & 실행

```bash
docker-compose up --build
```

실행 후 접속:

| 서비스      | 주소                                                       |
| -------- | -------------------------------------------------------- |
| Frontend | [http://localhost:5173](http://localhost:5173)           |
| Backend  | [http://localhost:8000](http://localhost:8000)           |
| API Docs | [http://localhost:8000/docs](http://localhost:8000/docs) |
| MySQL    | localhost:3306                                           |

---

## 4. 컨테이너 종료

```bash
Ctrl + C
```

완전 종료:

```bash
docker-compose down
```

---

## 5. 패키지 설치 방식

### Backend (FastAPI)

```dockerfile
RUN pip install -r requirements.txt
```

### Frontend (Vite + React)

```dockerfile
RUN npm install
RUN npm run build
```

---

## 6. MySQL 설정

```yaml
MYSQL_ROOT_PASSWORD: root
MYSQL_DATABASE: cloud_project
```

접속 정보:

* Host: `mysql`
* Port: `3306`
* User: `root`
* Password: `root`
* DB: `cloud_project`

---

## 7. 배포 방식

Docker 이미지는 GitHub에 업로드하지 않습니다.
각 환경에서 직접 빌드합니다.

```bash
docker-compose up --build
```

---

## 8. 불필요한 파일 (.gitignore)

```gitignore
node_modules/
__pycache__/
.env
mysql/data/
```

---

## 9. 사용 기술

* Docker / Docker Compose
* FastAPI
* MySQL
* React (Vite)

---

## 10. 작성 목적

클라우드 배포 및 인프라 실습용 포트폴리오 프로젝트

---
