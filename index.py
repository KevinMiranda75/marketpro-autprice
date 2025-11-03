import os
import shutil
import time
import pyperclip
import pyautogui
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

PROFILE_TO_USE = "Profile 1"
URL_TO_PASTE = "https://market4.pro/dota2/?new_auth=&sort_by=promo&sort_direction=DESC"

user_data_dir = os.path.join(os.environ.get("USERPROFILE", ""), "AppData", "Local", "Google", "Chrome", "User Data")
original_profile_path = os.path.join(user_data_dir, PROFILE_TO_USE)
temp_profile_path = os.path.join(user_data_dir, "TempProfile")

if os.path.exists(temp_profile_path):
    shutil.rmtree(temp_profile_path)

shutil.copytree(original_profile_path, temp_profile_path)

options = Options()
options.add_argument(f"--user-data-dir={user_data_dir}")
options.add_argument(f"--profile-directory=TempProfile")
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

time.sleep(2)  # esperar a que la ventana abra (breve)
pyperclip.copy(URL_TO_PASTE)

# Asegurarse que la ventana de Chrome esté en primer plano
try:
    driver.maximize_window()
except Exception:
    pass

time.sleep(0.5)
pyautogui.hotkey('ctrl', 'l')   # foco en la barra de direcciones
time.sleep(0.1)
pyautogui.hotkey('ctrl', 'v')   # pega la URL desde el portapapeles
time.sleep(0.1)
pyautogui.press('enter')        # ir a la URL

# Fin del script: el navegador queda abierto en la URL pegada.
# NOTA: No borramos TempProfile mientras Chrome esté usando esa carpeta.
print("URL pegada en la barra de direcciones. El script ha terminado.")

