#%%
import pandas as pd
import time 
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC 
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService

# %%
service = ChromeService('chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://indeks.kompas.com/?site=tekno"
driver.get(url)
driver.maximize_window()

all_articles_data = []
page = 1
max_articles = 500 

# %%
def scrape_contents(link):
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    driver.get(link)

    content_text = ""
    try:
        # ambil isi artikel
        content_element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'read__content'))
        )
        content_text = content_element.text
    except Exception as e:
        print(f"Error scraping content from {link}: {e}")

    driver.close()
    driver.switch_to.window(original_window)
    return content_text

# %%
while True:
    if len(all_articles_data) >= max_articles:
        print("Reached maximum article limit.")
        break

    print("Scraping page:", page)
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'sectionBox'))
        )
        print("Articles section loaded.")
    except Exception as e:
        print(f"Articles section did not load: {e}")
        break
    
    articles = driver.find_elements(By.XPATH, '//div[@class="articleList -list"]/div[@class="articleItem"]')
    print(f"Found {len(articles)} articles on page {page}")

    for article in articles:
        if len(all_articles_data) >= max_articles:
            break

        try:
            title_element = article.find_element(By.CLASS_NAME, 'articleTitle')
            link_element = article.find_element(By.TAG_NAME, 'a')
            date_element = article.find_element(By.CLASS_NAME, 'articlePost-date')
            description_element = ""
            content_element = scrape_contents(link_element.get_attribute('href'))

            all_articles_data.append({
                "title": title_element.text,
                "link": link_element.get_attribute('href'),
                "date": date_element.text,
                "description": description_element,
                "content": content_element
            })

            print(f"Scraped article: {title_element.text}")
            print("-" * 80)

        except Exception as e:
            print(f"Error extracting article details: {e}")
            continue
    
    if len(all_articles_data) >= max_articles:
        print("Reached maximum article limit.")
        break

    try:
        next_button = driver.find_elements(By.XPATH, '//a[@class="paging__link paging__link--next"]')
        if next_button:
            next_page = next_button[0].get_attribute('href')
            driver.get(next_page)
            page += 1
            time.sleep(2)  
        else:
            print("No more pages found.")
            break
    except Exception as e:
        print("No more pages or error navigating to next page:", e)
        break

print(f"Total articles scraped: {len(all_articles_data)}")
driver.quit()

# %%
df = pd.DataFrame(all_articles_data)
df.to_csv("kompas_tekno_terbaru.csv", index=False, encoding="utf-8-sig")
print("Data saved to kompas_tekno.csv")

# %%
