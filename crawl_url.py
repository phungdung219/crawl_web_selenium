import os
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import random

# 🛠 Khởi động WebDriver
url = 'https://www.cafepress.com/'
s = Service(r"C:\Program Files (x86)\chromedriver.exe")
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # Chạy nền để tăng tốc
options.add_argument("--disable-gpu")  # Tắt GPU để tránh treo
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-blink-features=AutomationControlled") 
driver = webdriver.Chrome(service=s, options=options)

driver.get(url)
# Tìm kết quản tìm kiếm
search = driver.find_element(By.ID, 'searchInput')
search.send_keys('customize star phone and tech')
search.send_keys(Keys.RETURN)

# 📂 Tên file chứa link sản phẩm
links_file = r"D:\product_links.txt"

# 🔽 Đọc danh sách link cũ từ file (nếu có)
if os.path.exists(links_file):
    with open(links_file, "r", encoding="utf-8") as f:
        existing_links = set(line.strip() for line in f.readlines())
else:
    existing_links = set()

# 📌 Set để lưu link mới (lọc trùng)
product_links = set(existing_links)  # Copy link cũ để tránh trùng lặp


while True:
    time.sleep(random.uniform(1, 2)) 
    listingGroup = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "listingGroup"))
    )
    products = driver.find_elements(By.CLASS_NAME, 'listing-item')
    for index,product in enumerate(products):
        try:
            product_link = product.find_element(By.TAG_NAME, "a").get_attribute("href")  # Lấy href
            if product_link:
                product_links.add(product_link)  # Thêm vào set (tự động lọc trùng)
        except Exception as e:
            print(f"❌ Lỗi: {e}")
    # Tìm và nhấn nút "Next" hoặc "Tiếp theo"
    try:
        next_button = driver.find_element(By.CSS_SELECTOR, "#paginationBlock ul li:last-child:not(.disabled) > a")
        next_button.click()
    except NoSuchElementException:
        print("No more pages.")
        break

# 📝 Lưu link sản phẩm vào file
with open(links_file, "w", encoding="utf-8") as f:
    for link in sorted(product_links):  # Sắp xếp để dễ kiểm tra
        f.write(link + "\n")

print(f"✅ Đã lưu {len(product_links)} link vào {links_file}")

# Đóng trình duyệt
driver.quit()
