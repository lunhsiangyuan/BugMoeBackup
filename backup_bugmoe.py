import os
import sys
import shutil
import argparse
import logging
import zipfile
from datetime import datetime
from tqdm import tqdm
import hashlib
import tkinter as tk
from tkinter import filedialog, ttk, messagebox

def calculate_total_size(source_path):
    total_size = 0
    for dirpath, dirnames, filenames in os.walk(source_path):
        for f in filenames:
            fp = os.path.join(dirpath, f)
            total_size += os.path.getsize(fp)
    return total_size

def calculate_file_hash(file_path, chunk_size=8192):
    """計算檔案的 MD5 hash"""
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_with_progress(src, dst):
    """複製檔案並顯示進度"""
    total_size = os.path.getsize(src)
    with open(src, 'rb') as fsrc:
        with open(dst, 'wb') as fdst:
            with tqdm(total=total_size, unit='B', unit_scale=True, desc=os.path.basename(src)) as pbar:
                while True:
                    buf = fsrc.read(8192)
                    if not buf:
                        break
                    fdst.write(buf)
                    pbar.update(len(buf))

class BackupGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BugMoe 地圖備份工具")
        self.root.geometry("600x400")
        
        # 設定視窗樣式
        style = ttk.Style()
        style.configure("TButton", padding=6)
        style.configure("TLabel", padding=6)
        
        # 建立主框架
        main_frame = ttk.Frame(root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 來源路徑
        ttk.Label(main_frame, text="BugMoe 地圖資料夾:").grid(row=0, column=0, sticky=tk.W)
        self.source_path = tk.StringVar()
        source_entry = ttk.Entry(main_frame, textvariable=self.source_path, width=50)
        source_entry.grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="瀏覽", command=self.browse_source).grid(row=0, column=2)
        
        # 目標路徑
        ttk.Label(main_frame, text="備份儲存位置:").grid(row=1, column=0, sticky=tk.W)
        self.dest_path = tk.StringVar()
        dest_entry = ttk.Entry(main_frame, textvariable=self.dest_path, width=50)
        dest_entry.grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="瀏覽", command=self.browse_dest).grid(row=1, column=2)
        
        # 進度條
        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=2, column=0, columnspan=3, pady=20)
        
        # 狀態標籤
        self.status_var = tk.StringVar(value="請選擇來源和目標資料夾")
        self.status_label = ttk.Label(main_frame, textvariable=self.status_var)
        self.status_label.grid(row=3, column=0, columnspan=3)
        
        # 開始備份按鈕
        self.backup_button = ttk.Button(main_frame, text="開始備份", command=self.start_backup)
        self.backup_button.grid(row=4, column=1, pady=20)
        
        # 設定視窗大小可調整
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)

    def browse_source(self):
        path = filedialog.askdirectory(title="選擇 BugMoe 地圖資料夾")
        if path:
            self.source_path.set(path)
            
    def browse_dest(self):
        path = filedialog.askdirectory(title="選擇備份儲存位置")
        if path:
            self.dest_path.set(path)
    
    def update_progress(self, current, total):
        progress = (current / total) * 100
        self.progress['value'] = progress
        self.root.update_idletasks()
    
    def create_zip_file(self, source_path, zip_path):
        """建立壓縮檔案並更新進度條"""
        # 計算總大小
        total_size = sum(os.path.getsize(os.path.join(dirpath, filename))
                        for dirpath, _, filenames in os.walk(source_path)
                        for filename in filenames)
        
        current_size = 0
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as zipf:
            for root, _, files in os.walk(source_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_path)
                    
                    # 更新進度
                    file_size = os.path.getsize(file_path)
                    zipf.write(file_path, arcname)
                    current_size += file_size
                    self.update_progress(current_size, total_size)
                    self.status_var.set(f"正在壓縮: {arcname}")
                    self.root.update_idletasks()
    
    def start_backup(self):
        source = self.source_path.get()
        dest = self.dest_path.get()
        
        if not source or not dest:
            messagebox.showerror("錯誤", "請選擇來源和目標資料夾")
            return
            
        if not os.path.exists(source):
            messagebox.showerror("錯誤", "來源資料夾不存在")
            return
            
        try:
            # 建立日誌檔案
            os.makedirs(dest, exist_ok=True)
            log_file = os.path.join(dest, 'backup.log')
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_file),
                    logging.StreamHandler(sys.stdout)
                ]
            )
            
            # 建立壓縮檔案名稱
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            zip_filename = f'BugMoe_backup_{timestamp}.zip'
            zip_path = os.path.join(dest, zip_filename)
            
            # 開始備份
            self.status_var.set("正在計算檔案大小...")
            self.backup_button.state(['disabled'])
            
            # 建立壓縮檔
            self.create_zip_file(source, zip_path)
            
            # 完成
            if os.path.exists(zip_path):
                zip_size = os.path.getsize(zip_path)
                success_msg = f"備份完成！\n壓縮檔大小: {zip_size / (1024*1024*1024):.2f} GB\n儲存於: {zip_path}"
                messagebox.showinfo("完成", success_msg)
                self.status_var.set("備份完成")
            else:
                messagebox.showerror("錯誤", "壓縮檔建立失敗")
                self.status_var.set("備份失敗")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"備份過程發生錯誤：\n{str(e)}")
            logging.error(f"Error during backup: {str(e)}")
            self.status_var.set("備份失敗")
        
        finally:
            self.backup_button.state(['!disabled'])
            self.progress['value'] = 0

def main():
    if len(sys.argv) > 1:
        # 命令列模式
        parser = argparse.ArgumentParser(description='Backup BugMoe Minecraft Map')
        parser.add_argument('source', help='Source folder path')
        parser.add_argument('destination', help='Destination folder path')
        args = parser.parse_args()
        
        print(f"Starting backup from {args.source} to {args.destination}")
        backup = BackupGUI(None)
        backup.source_path.set(args.source)
        backup.dest_path.set(args.destination)
        backup.start_backup()
    else:
        # GUI 模式
        root = tk.Tk()
        app = BackupGUI(root)
        root.mainloop()

if __name__ == "__main__":
    main() 