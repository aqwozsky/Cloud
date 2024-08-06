import winreg
import os

def set_file_extension_icon(extension, icon_path):
    try:
        # Dosya uzantısı anahtarını oluşturma
        key_path = r'SOFTWARE\Classes\.' + extension
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path) as key:
            winreg.SetValueEx(key, '', 0, winreg.REG_SZ, 'CustomFileType')

        # Dosya türü anahtarını oluşturma
        file_type_key = r'SOFTWARE\Classes\CustomFileType'
        with winreg.CreateKey(winreg.HKEY_CURRENT_USER, file_type_key) as key:
            winreg.SetValueEx(key, '', 0, winreg.REG_SZ, 'Custom File Type')
            icon_key = os.path.join(file_type_key, 'DefaultIcon')
            with winreg.CreateKey(winreg.HKEY_CURRENT_USER, icon_key) as icon_key:
                winreg.SetValueEx(icon_key, '', 0, winreg.REG_SZ, icon_path)

        print(f"İkon başarıyla ayarlandı: {extension} -> {icon_path}")
    except Exception as e:
        print(f"İkon ayarlanırken bir hata oluştu: {e}")

# Kullanım
set_file_extension_icon('cl', '/logos/cloud.ico')
