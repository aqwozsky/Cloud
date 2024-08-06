import os
import ctypes
import sys
import requests
import zipfile
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk  # Pillow kütüphanesi gereklidir
import winreg

GITHUB_REPO_URL = 'https://github.com/aqwozsky/Cloud.git'  # GitHub repo URL'sini güncelleyin

class SetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cloud Setup")
        self.root.geometry("600x500")
        self.root.resizable(False, False)  # Pencere boyutlandırmayı devre dışı bırakır

        # Sağ tarafta fotoğraf için bir çerçeve (Şu an gizli)
        self.image_frame = tk.Frame(root, width=200, height=500)
        self.image_frame.pack(side=tk.RIGHT, fill=tk.Y)
        self.image_frame.pack_forget()  # Fotoğrafı gizle

        # Ana çerçeve
        self.main_frame = tk.Frame(root)
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.label = tk.Label(self.main_frame, text="Install Cloud")
        self.label.pack(pady=10)

        self.install_button = tk.Button(self.main_frame, text="Kurulum Yap", command=self.install)
        self.install_button.pack(pady=20)

        # Yükleniyor ve İptal Et butonları
        self.loading_label = tk.Label(self.main_frame, text="", fg="blue")
        self.cancel_button = tk.Button(self.main_frame, text="İptal Et", command=self.cancel_install, state=tk.DISABLED)
        
    def is_admin(self):
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def request_admin(self):
        if not self.is_admin():
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            self.root.destroy()
            return False
        return True

    def download_and_extract(self, url, extract_to):
        response = requests.get(url)
        with open('cloud.zip', 'wb') as file:
            file.write(response.content)

        with zipfile.ZipFile('cloud.zip', 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        os.remove('cloud.zip')

    def add_to_path(self, new_dir):
        if not self.request_admin():
            return

        # PATH çevresel değişkenine ekleme
        path_env = os.environ.get('PATH', '')
        if new_dir not in path_env:
            os.environ['PATH'] += os.pathsep + new_dir
            try:
                # Kayıt defterine PATH ekleme
                reg = winreg.ConnectRegistry(None, winreg.HKEY_CURRENT_USER)
                reg_key = winreg.OpenKey(reg, "Environment", 0, winreg.KEY_SET_VALUE)
                current_path = winreg.QueryValueEx(reg_key, "PATH")[0]
                if new_dir not in current_path:
                    new_path = current_path + os.pathsep + new_dir
                    winreg.SetValueEx(reg_key, "PATH", 0, winreg.REG_EXPAND_SZ, new_path)
                    print(f"PATH'e {new_dir} dizini eklendi.")
                else:
                    print(f"{new_dir} zaten PATH'e eklenmiş.")
                winreg.CloseKey(reg_key)
            except Exception as e:
                print(f"PATH güncellenirken bir hata oluştu: {e}")
        else:
            print(f"{new_dir} zaten PATH'e eklenmiş.")

    def install(self):
        if not self.request_admin():
            return

        self.install_button.config(state=tk.DISABLED)
        self.loading_label.config(text="Yükleniyor...", fg="blue")
        self.loading_label.pack(pady=10)
        self.cancel_button.config(state=tk.NORMAL)
        self.cancel_button.pack(pady=10)

        install_dir = os.path.join(os.path.expanduser("~"), "cloud")
        if not os.path.exists(install_dir):
            os.makedirs(install_dir)

        try:
            self.download_and_extract(GITHUB_REPO_URL, install_dir)
            self.add_to_path(install_dir)

            if messagebox.askyesno("PATH Limiti", "PATH limitini genişletmek istiyor musunuz? Bu işlem yönetici izinleri gerektirir."):
                self.increase_path_limit()

            messagebox.showinfo("Başarı", "Kurulum tamamlandı. Cloud yazılım diliniz PATH'e eklendi ve kullanılabilir.")
        finally:
            self.install_button.config(state=tk.NORMAL)
            self.loading_label.config(text="")
            self.cancel_button.config(state=tk.DISABLED)

    def cancel_install(self):
        response = messagebox.askyesno("İptal Et", "Kurulumu iptal etmek istediğinizden emin misiniz?")
        if response:
            self.root.destroy()  # Kurulumu iptal edip uygulamayı kapat

    def increase_path_limit(self):
        if not self.is_admin():
            messagebox.showerror("Yetki Hatası", "Bu işlemi gerçekleştirmek için yönetici izinlerine ihtiyaç var.")
            return
        
        try:
            reg = winreg.ConnectRegistry(None, winreg.HKEY_LOCAL_MACHINE)
            reg_key = winreg.OpenKey(reg, "SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment", 0, winreg.KEY_SET_VALUE)
            max_path_len = 1024  # PATH limitini genişletme değeri
            winreg.SetValueEx(reg_key, "PathLimit", 0, winreg.REG_DWORD, max_path_len)
            winreg.CloseKey(reg_key)
            messagebox.showinfo("Başarı", "PATH limiti başarıyla genişletildi.")
        except Exception as e:
            messagebox.showerror("Hata", f"PATH limiti genişletilirken bir hata oluştu: {e}")

def main():
    root = tk.Tk()
    app = SetupApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
