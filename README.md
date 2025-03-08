# FTP 클라이언트 프로그램

Windows Server 2019 환경에서 동작하는 FTP 클라이언트 프로그램입니다. 이 프로그램은 제목, 내용, 첨부파일을 FTP 서버에 업로드할 수 있는 기능을 제공합니다.

![FTP 클라이언트 스크린샷](screenshot.png)

## 주요 기능
- FTP 서버 연결 (호스트, 포트, 사용자명, 비밀번호 설정)
- 파일 업로드 (제목, 내용, 첨부파일)
- 직관적인 그래픽 사용자 인터페이스
- 안전한 연결 종료 처리

## 요구사항
- Python 3.12
- tkinter (Python 내장 라이브러리)
- tkcalendar 1.6.1

## 설치 방법
1. 저장소 클론
```bash
git clone https://github.com/사용자명/ftp-client.git
cd ftp-client
```

2. 가상환경 생성 및 활성화
```bash
python -m venv .venv
# Windows
.\.venv\Scripts\activate
# Linux/Mac
source .venv/bin/activate
```

3. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 실행 방법
```bash
python ftp_client.py
```

## 사용 방법
자세한 사용 방법은 [기능설명서.md](기능설명서.md) 파일을 참조하세요.

## 라이센스
MIT License

## 기여 방법
1. 이 저장소를 포크합니다.
2. 새 기능 브랜치를 생성합니다 (`git checkout -b feature/amazing-feature`)
3. 변경사항을 커밋합니다 (`git commit -m 'Add some amazing feature'`)
4. 브랜치에 푸시합니다 (`git push origin feature/amazing-feature`)
5. Pull Request를 생성합니다. # ftp-client
