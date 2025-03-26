from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import time
import os
import shutil
import glob

# === 설정 ===
download_dir = r"C:\새 폴더"
chrome_download_dir = r"경로"
user_id = "아이디"
user_pw = "비번"

station_list = [
    "목포", "보령", "부산", "성산포", "여수", "영광", "완도", "인천", "장항", "제주", "진도", "통영", "흑산도",
    "거문도", "거제도", "고흥발포", "군산", "대산", "마산", "모슬포", "묵호", "서귀포", "속초", "안산", "안흥",
    "어청도", "울릉도", "울산", "위도", "추자도", "평택", "포항", "후포"
]

# === 크롬 옵션 설정 ===
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("경로")
chrome_options.add_argument("profile-directory=Profile 3")
chrome_options.add_experimental_option("prefs", {
    "download.default_directory": chrome_download_dir,
    "download.prompt_for_download": False,
    "safebrowsing.enabled": True
})
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--disable-popup-blocking")

driver = webdriver.Chrome(options=chrome_options)

# === 다운로드 완료 대기 함수 ===
def wait_for_download_complete(download_path, timeout=60):
    print("  - 다운로드 완료 대기 중...")
    seconds = 0
    while True:
        time.sleep(1)
        crdownload_files = glob.glob(os.path.join(download_path, "*.crdownload"))
        if not crdownload_files:
            print("  -  다운로드 완료!")
            break
        seconds += 1
        if seconds > timeout:
            print("  - ⏰ 다운로드 대기 시간 초과 (계속 진행)")
            break

# === 다운로드 파일 이동 함수 ===
def move_recent_zip_files(station_name):
    station_dir = os.path.join(download_dir, station_name)
    if not os.path.exists(station_dir):
        os.makedirs(station_dir)

    zip_files = [f for f in os.listdir(chrome_download_dir) if f.endswith(".zip")]
    zip_files_with_time = [(f, os.path.getmtime(os.path.join(chrome_download_dir, f))) for f in zip_files]
    zip_files_sorted = sorted(zip_files_with_time, key=lambda x: x[1], reverse=True)

    for i in range(min(2, len(zip_files_sorted))):
        file_name = zip_files_sorted[i][0]
        src = os.path.join(chrome_download_dir, file_name)
        dst = os.path.join(station_dir, file_name)
        print(f"  - 이동: {file_name} → {station_dir}")
        shutil.move(src, dst)

# === 실행 ===
try:
    # 로그인
    driver.get("https://www.khoa.go.kr/oceangrid/cmm/login.do")
    time.sleep(2)
    driver.find_element(By.ID, "user_id").send_keys(user_id)
    driver.find_element(By.ID, "user_passwd").send_keys(user_pw)
    driver.find_element(By.ID, "btn_login").click()
    time.sleep(2)

    for station_name in station_list:
        print(f"\n▶ 관측소: {station_name}")
        driver.get("https://www.khoa.go.kr/oceangrid/gis/category/reference/distribution.do")
        time.sleep(3)

        # '관측자료' → '년별'
        driver.find_element(By.ID, "radioDivSearch").click()
        time.sleep(1)
        driver.find_element(By.ID, "yearTerm").click()
        time.sleep(1)

        # 관측소 유형 선택
        Select(driver.find_element(By.ID, "observerType")).select_by_value("DT")
        time.sleep(2)

        # 관측소 선택
        try:
            Select(driver.find_element(By.ID, "obsStation")).select_by_visible_text(station_name)
        except:
            print(f"  -  관측소 '{station_name}' 선택 실패 (스킵)")
            continue
        time.sleep(1)

        # 검색
        driver.find_element(By.XPATH, "//a[contains(@onclick, 'fn_search')]").click()
        time.sleep(3)

        # 1~2페이지 다운로드
        for page in range(1, 3):
            print(f"  - [{page}페이지] 다운로드 중...")

            if page == 1:
                checkbox = driver.find_element(By.ID, "checkboxAll")
                driver.execute_script("arguments[0].click();", checkbox)
            else:
                first_checkbox = driver.find_element(By.XPATH, "//input[@class='filedownList'][1]")
                driver.execute_script("arguments[0].click();", first_checkbox)

            time.sleep(1)

            download_button = driver.find_element(By.NAME, "zipdown")
            driver.execute_script("arguments[0].click();", download_button)

            # 다운로드 완료까지 대기
            wait_for_download_complete(chrome_download_dir, timeout=60)

            if page < 2:
                driver.execute_script(f"goPage({page+1});")
                time.sleep(3)

        # 다운로드 파일 이동
        move_recent_zip_files(station_name)

    print("\n 모든 관측소 다운로드 및 정리 완료!")

finally:
    print("\n브라우저를 종료합니다.")
    driver.quit()
