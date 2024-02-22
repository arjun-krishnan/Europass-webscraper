# -*- coding: utf-8 -*-
"""
Created on Mon Jan 22 15:14:01 2024

Web scraping script using Selenium to find job listings on Europa website.
@author: arjun
"""

from langdetect import detect
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tqdm import tqdm
import time
import json
import csv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

def search_jobs(search_keyword, search_location, keywords, excluded_keywords, languages=['en'], N_pages=10, show_window=False):

    # Set up a controllable Chrome instance in headless mode
    service = Service()
    options = webdriver.ChromeOptions()
    if not show_window:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(service=service, options=options)

    # Open the target page in the browser
    driver.get("https://europa.eu/europass/en/find-jobs")
    time.sleep(2)

    # Accept cookies
    cookies = driver.find_element(By.LINK_TEXT, "Accept only essential cookies")
    cookies.click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cookie-consent-banner']/div/div/div[2]/button"))).click()

    driver.find_element(By.XPATH,"//*[@id='edit-keyword']").send_keys(search_keyword)
    driver.find_element(By.XPATH,"//*[@id='edit-location']").send_keys(search_location)
    driver.find_element(By.CSS_SELECTOR,".search-submit").click()
    time.sleep(5)
    driver.find_element(By.CSS_SELECTOR,".search-submit").click()

    jobs = []
    positive = 0

    for i_page, page in enumerate(tqdm(range(N_pages))):
        time.sleep(2)
        job_cards = driver.find_elements(By.CSS_SELECTOR, ".row")

        for job in job_cards:
            try:
                # Extract job details
                title_ele = job.find_element(By.CSS_SELECTOR, ".jobs--title")
                title_text = title_ele.text
                description_ele = job.find_element(By.CSS_SELECTOR, ".node-content")
                description_text = description_ele.text

                # Check if job description matches your criteria
                keywords_True = any(word.lower() in description_text.lower() for word in keywords)
                excluded_True = all(word.lower() not in title_text.lower() for word in excluded_keywords)
                language_True = detect(description_text) in languages

                if keywords_True and excluded_True and language_True:
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

    filename = f"{search_location}_{search_keyword}_results"
    save_results(filename, jobs)

    print(f"\nFound {positive} jobs with matching keywords in {i_page+1} pages!")

    # Close the browser and free up resources
    driver.quit()

    return jobs


def save_results(filename, jobs):
    # Check if the file exists
    if os.path.exists(f"results/{filename}.json") or os.path.exists(f"{filename}.csv"):
        # If the file exists, find a unique filename by appending a suffix
        suffix = 1
        while True:
            new_filename = f"{filename}_{suffix}"
            if not os.path.exists(f"results/{new_filename}.json"):
                break
            suffix += 1
        filename = new_filename

    # Save results in JSON file
    with open(f"results/{filename}.json", 'w', encoding='utf-8') as file:
        json.dump(jobs, file, ensure_ascii=False, indent=4)

    # Save results in CSV file
    with open(f"results/{filename}.csv", 'w', newline='', encoding='utf-8') as file:
        csv_writer = csv.writer(file)
        csv_writer.writerow(["Title", "URL"])

        for job in jobs:
            csv_writer.writerow([job["Title"], f'=HYPERLINK("{job["Link"]}","{job["Link"]}")'])

    return
