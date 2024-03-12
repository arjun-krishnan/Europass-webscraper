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
from gemini_gpt_functions import read_profile, profile_match
from tqdm import tqdm
import time
import json
import csv
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
os.chdir(dir_path)

profile = read_profile("profile.txt")

def search_jobs(search_keyword, search_location, keywords, excluded_keywords, languages=['en'], N_pages=10, show_window=False, search_mode='basic'):

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
    #WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='cookie-consent-banner']/div/div/div[2]/button"))).click()

    driver.find_element(By.XPATH,"//*[@id='edit-keyword']").send_keys(search_keyword)
    driver.find_element(By.XPATH,"//*[@id='edit-location']").send_keys(search_location)

    while True:
        driver.find_element(By.CSS_SELECTOR,".search-submit").click()
        try:
            WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.CSS_SELECTOR, ".jobs--title")))
            break
        except:
            continue

    jobs = []
    positive, good_match = 0, 0

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
                        "Link":
                            str(job.find_element(By.CSS_SELECTOR, ".boxButtonslist a:nth-child(2)").get_attribute("href")).split('?')[0]
                    }
                    positive += 1

                    if search_mode == 'gemini' or search_mode == 'openai':
                        results, match = profile_match(description_text, profile, search_mode)
                        job_details.update({
                            "Job-level match": results[0],
                            "Skills match": results[1],
                            "Good match": match
                        })
                        if match:
                            good_match += 1
                        print(f"\n{positive}: {title_text}\nJob-level match: {results[0]}\t Skills match: {results[1]}")

                    jobs.append(job_details)

                    if search_mode == 'basic':
                        print(f"\n{positive}: {title_text}")

            except Exception as e:
                print(f"Something went wrong while fetching data: {e}")
                pass

        try:
            # Navigate to the next page
            nextpage_button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'li.ecl-pagination__item--next')))
            nextpage_button.click()
        except Exception as e:
            print(f"Something went wrong while clicking next: {e}")
            break

    filename = f"{search_location}_{search_keyword}_results"
    save_results(filename, jobs, search_mode)

    if search_mode == 'basic':
        print(f"\nFound {positive} jobs with matching keywords in {i_page+1} pages!")
    else:
        print(f"\nFound {positive} jobs with matching keywords with {good_match} good matches in {i_page + 1} pages!")
    # Close the browser and free up resources
    driver.quit()

    return jobs


def save_results(filename, jobs, mode=None):
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

        if mode == 'gemini':
            csv_writer.writerow(["Title", "Job-level match", "Skills match", "Good match", "URL"])
            for job in jobs:
                csv_writer.writerow([job["Title"], job["Job-level match"], job["Skills match"], job["Good match"], f'=HYPERLINK("{job["Link"]}","Link")'])
        else:
            csv_writer.writerow(["Title", "URL"])
            for job in jobs:
                csv_writer.writerow([job["Title"], f'=HYPERLINK("{job["Link"]}","Link")'])


    return
