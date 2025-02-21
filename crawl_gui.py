import tkinter as tk
from tkinter import messagebox
import subprocess

# Đường dẫn file Python xử lý crawl
CRAWL_URL_SCRIPT = "crawl_url.py"
CRAWL_IMAGE_SCRIPT = "crawl_img.py"

def start_crawl_urls():
    keyword = keyword_entry.get().strip()
    if not keyword:
        messagebox.showwarning("Warning", "Please enter a search keyword!")
        return
    
    messagebox.showinfo("Info", "Crawling URLs, please wait...")
    try:
        subprocess.run(["python", CRAWL_URL_SCRIPT, keyword], check=True)
        messagebox.showinfo("Success", "Crawling URLs completed!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to crawl URLs!")

def start_crawl_images():
    messagebox.showinfo("Info", "Crawling Images, please wait...")
    try:
        subprocess.run(["python", CRAWL_IMAGE_SCRIPT], check=True)
        messagebox.showinfo("Success", "Crawling Images completed!")
    except subprocess.CalledProcessError:
        messagebox.showerror("Error", "Failed to crawl images!")

# GUI Setup
root = tk.Tk()
root.title("Web Crawler")
root.geometry("400x200")

tk.Label(root, text="Enter Search Keyword:").pack(pady=5)
keyword_entry = tk.Entry(root, width=40)
keyword_entry.pack(pady=5)

tk.Button(root, text="Start Crawl URLs", command=start_crawl_urls).pack(pady=10)
tk.Button(root, text="Start Crawl Images", command=start_crawl_images).pack(pady=10)

root.mainloop()
