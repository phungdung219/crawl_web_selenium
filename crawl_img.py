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
from concurrent.futures import ThreadPoolExecutor, as_completed

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# 📂 Đường dẫn thư mục bạn muốn lưu ảnh
save_folder = r"D:\image_crawl"  # Thay đổi đường dẫn theo ý bạn

# 📂 File chứa link sản phẩm
links_file = r"D:\product_links.txt"

# 🔽 Đọc danh sách link từ file
with open(links_file, "r", encoding="utf-8") as f:
    product_links = [line.strip() for line in f.readlines()]

# 📌 Hàm kiểm tra trùng lặp tên thư mục
def get_unique_folder(base_path, folder_name):
    folder_path = os.path.join(base_path, folder_name)
    counter = 1
    while os.path.exists(folder_path):
        folder_path = os.path.join(base_path, f"{folder_name} ({counter})")
        counter += 1
    os.makedirs(folder_path)  # Tạo thư mục
    return folder_path

# 📌 Hàm tải ảnh
def download_image(url, save_path, max_retries=5):
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, timeout=10)  # Thêm timeout để tránh treo
            if response.status_code == 200:
                with open(save_path, 'wb') as file:
                    file.write(response.content)
                print(f"✅ Tải thành công: {save_path}")
                return True
            else:
                print(f"⚠️ Lỗi {response.status_code} khi tải {url}")
        except requests.exceptions.RequestException as e:
            print(f"🔄 Thử lại ({retries+1}/{max_retries}): {e}")
        time.sleep(2)  # Chờ 2 giây trước khi thử lại
        retries += 1

    print(f"❌ Không thể tải ảnh sau {max_retries} lần thử: {url}")
    return False

# 📌 Hàm mở trang sản phẩm và tải ảnh (chạy song song)
def process_product(product_url):
    # 🛠 Mở trình duyệt riêng biệt
    s = Service(r"C:\Program Files (x86)\chromedriver.exe")
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")  # Chạy nền để tăng tốc
    options.add_argument("--disable-gpu")  # Tắt GPU để tránh treo
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=s, options=options)
    
    driver.get(product_url)
    time.sleep(1)  # Đợi trang load

    # 📌 Lấy tên sản phẩm làm tên thư mục
    try:
        product_name = driver.title  # Thay bằng class thực tế
        product_name = re.sub(r'[<>:"/\\|?*]', '-', product_name)  # Xóa ký tự đặc biệt

        # 📂 Tạo thư mục theo tên sản phẩm (xử lý trùng tên)
        product_folder = get_unique_folder(save_folder, product_name)
        
        # 📷 Lấy tất cả ảnh sản phẩm
        productBox = WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.ID, "product-selector-box"))
        )
        images = productBox.find_elements(By.CSS_SELECTOR, ".standard-img-container img")
        image_urls = [img.get_attribute("src") for img in images if img.get_attribute("src")]

        print(f"📸 {len(image_urls)} ảnh cho {product_name}")
        
        # # 🔽 Tải ảnh bằng đa lớp
        for index, image_url in enumerate(image_urls):
            download_image(image_url, os.path.join(product_folder, f"image_{index + 1}.png"))
    except Exception as e:
        print(f"❌ Lỗi với {product_url}: {e}")

    driver.quit()

# 🚀 Dùng đa luồng để tăng tốc độ crawl
try:
    with ThreadPoolExecutor(max_workers=8) as executor:  # 8 luồng chạy song song
        future_to_url = {executor.submit(process_product, url): url for url in product_links}

        for future in as_completed(future_to_url):
            try:
                future.result()  # Đợi từng task hoàn thành
            except Exception as e:
                print(f"⚠️ Lỗi trong một luồng: {e}")

except KeyboardInterrupt:
    print("⛔ Bị gián đoạn! Đang dừng tất cả luồng...")
finally:
    print("🚀 Crawl hoàn tất!")