import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random

def slow_typing(element, text, min_delay=0.07, max_delay=0.15):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))

# ✅ Chrome Setup
options = uc.ChromeOptions()
options.add_argument("--start-maximized")
driver = uc.Chrome(options=options)

try:
    # ✅ Step 1: Google Search for "online notepad"
    driver.get("https://www.google.com")
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "q")))
    search_box = driver.find_element(By.NAME, "q")
    slow_typing(search_box, "online notepad")
    search_box.send_keys(Keys.RETURN)

    # ✅ Step 2: Click First Organic Result (skip ads)
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div#search a h3")))
    results = driver.find_elements(By.CSS_SELECTOR, "div#search a h3")
    if results:
        driver.execute_script("arguments[0].click();", results[0])
    else:
        print("❌ No valid search results found.")
        driver.quit()
        exit()

    # ✅ Step 3: Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.TAG_NAME, "iframe")))
    time.sleep(2)

    # ✅ Step 4: Try Switching into Iframes to Find Editable Area
    notepad = None
    iframes = driver.find_elements(By.TAG_NAME, "iframe")
    for iframe in iframes:
        try:
            driver.switch_to.frame(iframe)
            textarea_tags = driver.find_elements(By.TAG_NAME, "textarea")
            contenteditable_divs = driver.find_elements(By.CSS_SELECTOR, "[contenteditable='true']")

            if textarea_tags:
                notepad = textarea_tags[0]
                break
            elif contenteditable_divs:
                notepad = contenteditable_divs[0]
                break
            driver.switch_to.default_content()
        except Exception as e:
            driver.switch_to.default_content()
            continue

    # ✅ Step 5: If no editor found in iframe, try main page
    if not notepad:
        driver.switch_to.default_content()
        textarea_tags = driver.find_elements(By.TAG_NAME, "textarea")
        contenteditable_divs = driver.find_elements(By.CSS_SELECTOR, "[contenteditable='true']")
        if textarea_tags:
            notepad = textarea_tags[0]
        elif contenteditable_divs:
            notepad = contenteditable_divs[0]

    # ✅ Step 6: Type into Notepad
    if notepad and notepad.is_displayed() and notepad.is_enabled():
        driver.execute_script("arguments[0].scrollIntoView(true);", notepad)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//textarea | //*[@contenteditable='true']")))
        notepad.click()
        slow_typing(notepad, "Hi, my name is Tabish Deshmukh. Nice to meet you!")
        notepad.send_keys(Keys.ENTER)
        slow_typing(notepad, "Bye", 0.1, 0.2)
        time.sleep(1)
    else:
        print("❌ Editable notepad area not found.")

finally:
    driver.quit()