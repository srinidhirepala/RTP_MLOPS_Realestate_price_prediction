import csv
import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#  Chrome options using your real profile
options = webdriver.ChromeOptions()
options.add_argument(r"--user-data-dir=C:/Users/valle/AppData/Local/Google/Chrome/User Data")
options.add_argument("--profile-directory=Default")  # Change to "Profile 1" if needed
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/123.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=Service(), options=options)

def scrape_99acres(area_url):
    all_data = []
    page = 1

    try:
        driver.get(area_url)
        time.sleep(5)

        while True:
            print(f"\n Scraping Page {page}...")

            try:
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "AI_LISTING"))
                )
            except:
                print(" Listings not loaded, skipping this page.")
                break

            # Scroll to load more listings
            for _ in range(5):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(random.uniform(2, 4))

            listings = driver.find_elements(By.XPATH, '//div[contains(@class, "tupleNew__outerTupleWrap")]')
            print(f" Found {len(listings)} listings.")

            for i, listing in enumerate(listings):
                try:
                    anchor_elements = listing.find_elements(By.TAG_NAME, 'a')
                    link = None
                    for a in anchor_elements:
                        href = a.get_attribute('href')
                        if href and "spid-" in href:
                            link = href
                            break

                    if not link:
                        print(f" Skipping listing {i+1} (no valid property link found)")
                        continue

                    driver.execute_script("window.open(arguments[0]);", link)
                    driver.switch_to.window(driver.window_handles[1])
                    time.sleep(random.uniform(3, 5))

                    try:
                        title = driver.find_element(By.XPATH, "//h1").text
                    except:
                        title = "N/A"

                    try:
                        price = driver.find_element(By.XPATH, '//*[@id="pdPrice2"]').text
                    except:
                        price = "N/A"

                    try:
                        location = driver.find_element(By.XPATH, '//*[@id="FactTableComponent"]/tbody/tr[2]/td[1]/div[2]').text
                    except:
                        location = "N/A"

                    try:
                        plot_area = driver.find_element(By.XPATH, '//*[@id="superArea_span"]').text
                    except:
                        plot_area = "N/A"

                    try:
                        facing = driver.find_element(By.XPATH, '//*[@id="facingLabel"]').text
                    except:
                        facing = "N/A"

                    try:
                        open_sides = driver.find_element(By.XPATH, '//*[@id="FactTableComponent"]/tbody/tr[4]/td[2]/div[2]').text
                    except:
                        open_sides = "N/A"

                    all_data.append({
                        "Title": title,
                        "Price": price,
                        "Location": location,
                        "Plot Area": plot_area,
                        "Facing": facing,
                        "Open Sides": open_sides,
                    })

                    print(f"{i+1}.  Scraped: {title}")

                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    time.sleep(random.uniform(2, 3))

                except Exception as e:
                    print(f" Error in listing {i+1}: {e}")
                    driver.close()
                    driver.switch_to.window(driver.window_handles[0])
                    continue

            #  Next Page
            try:
                next_btn = driver.find_element(By.XPATH, '//a[@class="pgsel"][1]/following-sibling::a')
                if "Next" in next_btn.text or next_btn.get_attribute("aria-label") == "Next":
                    driver.execute_script("arguments[0].click();", next_btn)
                    page += 1
                    time.sleep(5)
                else:
                    print(" No more pages left.")
                    break
            except:
                print(" No more pages left.")
                break

    finally:
        #  Save to CSV
        with open("99acres_patancheru_properties.csv", "w", newline='', encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["Title", "Price", "Location", "Plot Area", "Facing", "Open Sides"])
            writer.writeheader()
            writer.writerows(all_data)

        print(f"\n Done! {len(all_data)} properties saved to 99acres_patancheru_properties.csv")
        driver.quit()

#  URL for Patancheru Residential Plots
scrape_99acres("https://www.99acres.com/search/property/buy/residential-land/patancheru-hyderabad?city=269&locality=2630&property_type=3&preference=S&area_unit=1&res_com=R")
