# GitHub 저장소 생성 및 업로드 방법

## 1. GitHub 계정 생성
아직 GitHub 계정이 없다면 [GitHub](https://github.com)에서 계정을 생성하세요.

## 2. 새 저장소(Repository) 생성
1. GitHub에 로그인합니다.
2. 오른쪽 상단의 '+' 버튼을 클릭하고 'New repository'를 선택합니다.
3. 저장소 이름을 'ftp-client'로 입력합니다.
4. 설명(Description)을 입력합니다: "Windows Server 2019용 FTP 클라이언트 프로그램"
5. 저장소를 Public 또는 Private으로 설정합니다.
6. 'Initialize this repository with a README' 옵션은 체크하지 않습니다.
7. 'Create repository' 버튼을 클릭합니다.

## 3. 로컬 Git 저장소 초기화 및 GitHub 연결
아래 명령어를 순서대로 실행하세요:

```bash
# 현재 디렉토리에서 Git 초기화
git init

# 모든 파일을 스테이징
git add .

# 첫 번째 커밋 생성
git commit -m "Initial commit"

# GitHub 저장소를 원격 저장소로 추가 (YOUR_USERNAME을 본인의 GitHub 사용자명으로 변경)
git remote add origin https://github.com/YOUR_USERNAME/ftp-client.git

# 메인 브랜치 이름 설정 (GitHub 기본값은 'main')
git branch -M main

# GitHub 저장소에 푸시
git push -u origin main
```

## 4. GitHub 인증
- 명령줄에서 GitHub 계정 정보를 입력하라는 메시지가 표시됩니다.
- 또는 GitHub CLI나 Personal Access Token을 사용할 수 있습니다.

## 5. 확인
- GitHub 웹사이트에서 저장소를 확인하여 모든 파일이 올바르게 업로드되었는지 확인합니다.
- README.md 파일이 저장소 메인 페이지에 표시됩니다.

## 6. 추가 변경사항 업로드
코드를 수정한 후 다음 명령어로 변경사항을 업로드할 수 있습니다:

```bash
git add .
git commit -m "변경 내용 설명"
git push
```

## 참고
- `.gitignore` 파일은 Git이 추적하지 않아야 할 파일을 지정합니다.
- 가상환경 폴더(.venv)와 같은 불필요한 파일은 이미 무시 목록에 포함되어 있습니다.
