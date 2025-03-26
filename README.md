# KHOA 해양자료 자동 다운로드 스크립트

이 스크립트는 대한민국 해양조사원(KHOA)의 해양자료 배포 페이지에서 조위관측소별로 연도별 .zip 파일을 자동으로 다운로드하고 정리합니다.

## ✅ 주요 기능

- KHOA 자동 로그인
- 33개 조위관측소의 연도별 데이터 다운로드
- 1~2페이지 .zip 자료 자동 선택 및 다운로드
- 다운로드 완료 대기 후 파일 정리
- 관측소별 폴더로 자동 이동

## ⚙️ 사전 준비

1. Chrome 브라우저 설치
2. Chrome 사용자 프로필 경로 확인 (자동 로그인에 필요)
3. [ChromeDriver](https://sites.google.com/chromium.org/driver/) 설치
4. Python 3.x 설치

## 🛠 설정 항목

스크립트 상단의 값을 본인 환경에 맞게 수정하세요:

- \`download_dir\`: 다운로드된 파일을 정리할 최종 폴더
- \`chrome_download_dir\`: Chrome 기본 다운로드 폴더
- \`user_id\`, \`user_pw\`: KHOA 로그인 계정 정보
- Chrome 프로필 경로 및 이름

예시:

\`\`\`python
download_dir = r"C:\\Data\\KHOA"
chrome_download_dir = r"C:\\Users\\user\\Downloads"
user_id = "my_id"
user_pw = "my_password"
chrome_options.add_argument("user-data-dir=C:/Users/user/AppData/Local/Google/Chrome/User Data")
chrome_options.add_argument("profile-directory=Profile 3")
\`\`\`

## ▶ 실행 방법

```bash
python download_script.py
