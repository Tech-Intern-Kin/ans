import csv
import time
import random
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# === Setup undetected Chrome ===
options = uc.ChromeOptions()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/122 Safari/537.36")

driver = uc.Chrome(options=options)
wait = WebDriverWait(driver, 10)

# === Search Vivino for wine and get image URL ===
def get_vivino_image(wine_name):
    try:
        search_url = f"https://www.vivino.com/search/wines?q={wine_name}"
        driver.get(search_url)
        time.sleep(3)

        # Locate first wine card figure element containing the image
        wine_card = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "figure.wine-card__image")))
        
        # Extract the background image URL from the CSS style
        img_style = wine_card.get_attribute("style")
        img_url = img_style.split("url(")[-1].split(")")[0].strip('"')

        # Full URL if relative path
        if img_url.startswith('//'):
            img_url = "https:" + img_url

        return img_url
    except Exception as e:
        print(f"❌ Failed to get Vivino image for '{wine_name}': {e}")
        return ""

# === Optional scroll helper ===
def human_scroll(driver, depth=2):
    for _ in range(depth):
        driver.find_element(By.TAG_NAME, "body").send_keys(Keys.PAGE_DOWN)
        time.sleep(random.uniform(0.8, 1.2))

# === Read wine names from CSV ===
input_csv_file = r"C:\Users\User\Desktop\Uni\Career\WS\MAIN\ans_trading\wine_list.csv"
wine_names = []

with open(input_csv_file, mode="r", encoding="utf-8") as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip header row
    for row in reader:
        if row and row[0].strip():
            wine_names.append(row[0].strip())

# === Loop through wines ===
for wine in wine_names:
    print(f"\n🔍 Searching Vivino for: {wine}")
    img_url = get_vivino_image(wine)
    print(f"📷 Image URL: {img_url}")

driver.quit()
