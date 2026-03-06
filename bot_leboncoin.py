import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By																							
import os
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

TOKEN = os.getenv("8797243367:AAGvW2B1JkqNIUqB-QMNVc_FtpzS2UvQHOnU")
CHAT_IDS = os.getenv("1849711048, 8487334898").split(",")

SEARCH_URL = "https://www.leboncoin.fr/recherche?category=2&price=min-2000&mileage=min-200000&u_car_brand=AUDI,BMW,CITROEN,FORD,OPEL,PEUGEOT,RENAULT,VOLKSWAGEN,ALFA%20ROMEO,HONDA,HYUNDAI,KIA,NISSAN,TOYOTA&u_car_model=AUDI_A3,BMW_S%C3%A9rie%201,CITROEN_C1,CITROEN_C2,CITROEN_C3,OPEL_Corsa,PEUGEOT_107,PEUGEOT_207,PEUGEOT_206,PEUGEOT_307,PEUGEOT_306,PEUGEOT_308,RENAULT_Clio,RENAULT_Megane,RENAULT_Twingo,VOLKSWAGEN_Golf,VOLKSWAGEN_Polo&sort=time&order=desc"

seen = set()

SEEN_FILE = "seen_ads.txt"

try:
    with open(SEEN_FILE, "r") as f:
        seen = set(line.strip() for line in f)
except:
    seen = set()


def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    for chat_id in CHAT_IDS:
        requests.post(url, data={
            "chat_id": chat_id,
            "text": msg
        })

options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-infobars")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

send("🚀 Bot Leboncoin actif (mode visible) ✅")

while True:
    try:
        driver.get(SEARCH_URL)
        time.sleep(6)

        ads = driver.find_elements(By.CSS_SELECTOR, "a[href*='/ad/']")
        print("Annonces trouvées :", len(ads))

        for ad in ads:
            if ad not in seen:
                send(ad)
                seen.add(ad)

        with open(SEEN_FILE, "w") as f:
            for link in seen:
                f.write(link + "\n")


                send(f"🚗 Nouvelle annonce :\n\n{title}\n\n{link}")


        time.sleep(60)

    except Exception as e:
        print("Erreur détectée :", e)
        time.sleep(10)


