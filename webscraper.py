# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:14:01 2024

Web scraping script using Selenium to find job listings on Europa website.
@author: arjun
"""

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time
import json
import csv

# Set up a controllable Chrome instance in headless mode
service = Service()
options = webdriver.ChromeOptions()
#options.add_argument("--headless=new")  # Uncomment to run in headless mode / without displaying the browser window
driver = webdriver.Chrome(service=service, options=options)

# Open the target page in the browser
#driver.get("https://europa.eu/europass/en/find-jobs?keyword=data&location=Germany&order=relevance&form_build_id=form-Kwm_IYWWCd_v29y--AcXtfd0Bra0I9e3xI-WTJz1K7I&form_id=jobs_search")
driver.get("https://europa.eu/europass/en/find-jobs")
time.sleep(2)

# Accept cookies
cookies = driver.find_element(By.LINK_TEXT, "Accept only essential cookies")
cookies.click()
WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cookie-consent-banner']/div/div/div[2]/button"))).click()

search_keyword = "Scientist"    # The keyword to search for jobs
search_location = "Germany"     # Preferred location of the job

driver.find_element(By.XPATH,"//*[@id='edit-keyword']").send_keys(search_keyword)
driver.find_element(By.XPATH,"//*[@id='edit-location']").send_keys(search_location)
driver.find_element(By.CSS_SELECTOR,".search-submit").click()
time.sleep(2)
driver.find_element(By.CSS_SELECTOR,".search-submit").click()

# Keywords for job filtering
keywords = ["data science", "physics", "science", "scientist", "machine learning", "deep learning","english"]

# Scraping logic...
job_cards = driver.find_elements(By.CSS_SELECTOR, ".row")
jobs = []
positive = 0
N_pages = 5

for i, page in enumerate(tqdm(range(N_pages))):
    time.sleep(2)
    job_cards = driver.find_elements(By.CSS_SELECTOR, ".row")
    
    for job in job_cards:
        try:
            # Extract job details
            title_ele = job.find_element(By.CSS_SELECTOR, ".jobs--title")
            title_text = title_ele.text
            description_ele = job.find_element(By.CSS_SELECTOR, ".node-content")
            description_text = description_ele.text

            # Check if job description contains any of the keywords
            if any(word.lower() in description_text.lower() for word in keywords):
                job_details = {
                    "Title": title_text.strip(),
                    "Description": description_text.strip(),
                    "Link": str(job.find_element(By.CSS_SELECTOR, ".boxButtonslist a:nth-child(2)").get_attribute("href")).split('?')[0]
                }
                jobs.append(job_details)
                positive += 1
                print(str(positive) + " : " + title_text + "\n")

        except Exception as e:
            print(f"Something went wrong while fetching data: {e}")
            pass
    
    try:
        # Navigate to the next page
        nextpage_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ecl-pagination__item--next')))
        nextpage_button.click()
    except Exception as e:
        print(f"Something went wrong while clicking next: {e}")
        break

# Save results in JSON file
with open('results/positive_results.json', 'w', encoding='utf-8') as f:
    json.dump(jobs, f, ensure_ascii=False, indent=4)

# Save results in CSV file
with open('results/positive_results.csv', 'w', newline='') as file:
    csv_writer = csv.writer(file)
    csv_writer.writerow(["Title", "URL"])
    
    for job in jobs:
        csv_writer.writerow([job["Title"], f'=HYPERLINK("{job["Link"]}","{job["Link"]}")'])

print(f"\nFound {positive} jobs with matching keywords in {N_pages} pages!")

# Close the browser and free up resources
time.sleep(2)
driver.quit()
