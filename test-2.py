import time
import os
import webbrowser
import pyperclip
import pyautogui
import pygetwindow as gw

URL = "https://market4.pro/dota2/?new_auth=&sort_by=promo&sort_direction=DESC&filter=price%3D1_from-to_null"
TARGET_TITLES = ["Profile 1", "Google Chrome", "Chrome"]  # nombres a buscar en el título de la ventana
FOCUS_RETRIES = 6
RETRY_DELAY = 0.6

def find_chrome_window():
    wins = gw.getAllWindows()
    for w in wins:
        title = w.title or ""
        for t in TARGET_TITLES:
            if t.lower() in title.lower():
                return w
    # si no encontró por fragmento, intentar por "Chrome"
    for w in wins:
        if "chrome" in (w.title or "").lower():
            return w
    return None

def focus_and_paste(url):
    w = find_chrome_window()
    if w:
        try:
            w.restore()  # por si está minimizada
        except Exception:
            pass
        try:
            w.activate()
        except Exception:
            try:
                w.minimize(); time.sleep(0.1); w.restore(); w.activate()
            except Exception:
                pass
        # esperar a que la ventana reciba el foco
        for _ in range(FOCUS_RETRIES):
            time.sleep(RETRY_DELAY)
            # comprobar si está en primer plano por su posición
            # (no hay método 100% reliable en todas las máquinas, pero esto suele bastar)
            if gw.getActiveWindow() and gw.getActiveWindow().title == w.title:
                break

        time.sleep(0.2)
        pyperclip.copy(url)
        pyautogui.hotkey('ctrl', 'l')
        time.sleep(0.07)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(0.07)
        pyautogui.press('enter')
        return True
    else:
        return False

def main():
    # pequeño retraso para que tengas tiempo de cambiar de ventana si lo quieres
    time.sleep(0.5)
    ok = focus_and_paste(URL)
    if not ok:
        # fallback: abrir Chrome con la URL (no usa perfil específico)
        try:
            webbrowser.get("C:/Program Files/Google/Chrome/Application/chrome.exe %s").open(URL)
        except Exception:
            webbrowser.open(URL)
    print("Macro completado.")

if __name__ == "__main__":
    main()
