from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import os
import time
import re
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
PROXY = "207.2.120.15:80"

# 🛠 Cấu hình Chrome để dùng proxy
chrome_options = Options()
chrome_options.add_argument(f"--proxy-server={PROXY}")

url = 'https://www.cafepress.com/'
s = Service(r"C:\Program Files (x86)\chromedriver.exe")

driver = webdriver.Chrome(service=s)

driver.get(url)

search = driver.find_element(By.ID, 'searchInput')
search.send_keys('dragonball')
search.send_keys(Keys.RETURN)

# 📂 Đường dẫn thư mục bạn muốn lưu ảnh
save_folder = r"D:\image_crawl"  # Thay đổi đường dẫn theo ý bạn

page = 1  # Biến đếm số trang

while True:
    time.sleep(2)
    listingGroup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "listingGroup"))
    )
    cards = driver.find_elements(By.CLASS_NAME, 'listing-item')
    for index,card in enumerate(cards):
        title = card.find_element(By.CLASS_NAME, 'listing-title').text + f" - {index}"
        title = re.sub(r'[<>:"/\\|?*]', '_', title)
        
        img_url = card.find_element(By.CLASS_NAME, 'listing-image').get_attribute('data-src')
        img_alt_url = card.find_element(By.CLASS_NAME, 'listing-image').get_attribute('data-alt-src')
        if img_url and img_alt_url:
            try:
                # 📂 Tạo thư mục riêng cho từng ảnh (theo index)
                image_folder = os.path.join(save_folder, str(title))
                os.makedirs(image_folder, exist_ok=True)

                # 📄 Đường dẫn file ảnh
                file_path = os.path.join(image_folder, f"image.jpg")
                # 🖼 Tải ảnh về
                response = requests.get(img_url, stream=True)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: {img_url}")

                # 📄 Đường dẫn file ảnh
                file_path = os.path.join(image_folder, f"mockup.jpg")
                # 🖼 Tải ảnh về
                response = requests.get(img_alt_url, stream=True)
                if response.status_code == 200:
                    with open(file_path, "wb") as f:
                        f.write(response.content)
                    print(f"Downloaded: {img_alt_url}")
            except Exception as e:
                print(f"Error downloading {img_alt_url}: {e}")

    # Tìm và nhấn nút "Next" hoặc "Tiếp theo"
    try:
        next_button = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#paginationBlock ul li:last-child:not(.disabled) > a"))
        )
        next_button.click()
        page += 1
    except NoSuchElementException:
        print("No more pages.")
        break

# Đóng trình duyệt
driver.quit()