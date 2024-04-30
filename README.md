# Europass Webscraper

This Python script utilizes Selenium to scrape job listings from the Europass website based on specified keywords. The script then filters the jobs and saves positive results in both JSON and CSV formats.

## Prerequisites

The program uses Google Chrome to navigate through the website. So you must have Python and Google Chrome installed.

Before running the script, make sure to install the required dependencies:

```bash
pip install selenium tqdm langdetect
```
If you want to use the Google Gemini API or OpenAI API for intelligent job filtering, install:
```bash
pip install -U google-generativeai
pip install openai
```
## Configuration

To use WebScraper, simply import the **search_jobs** function from the **webscraper** module and pass the following arguments:
- **search_keywords** : Main keywords to start the search.
- **search_location** : Preferred location of the jobs.  
- **keywords** : List of words. Results are shown positive if any of these words are present in the job description.
- **excluded_keywords** : List of words. Exclude results if any of these words are present in the job title.
  - Eg. for entry level jobs, exclude words like 'senior', 'head' etc. 
- **languages** : List of languages to filter job ads.
- **N_pages** : Number of pages to scrape.
- **show_window** : set to True if you want to see the Chrome window  during the scraping process.
- **search_mode** : Flag to chose if you want to use the Google Gemini API to fliter the jobs according to your profile. The options are 'basic', 'openai' and 'gemini'.

## Using Gemini/OpenAI API

- Save your Gemini API key as an environment variable **GEMINI_API_KEY** or OpenAI API key as **OPENAI_API_KEY**.
- Get the Gemini API key from: https://ai.google.dev/ . It is free to use right now.
- Get OpenAI API key from: https://platform.openai.com/
- For users in Europe, the API access is not yet available. One work around is using a VPN.
- Modify the *profile.txt* file in the directory to describe your desired job level, skills etc.
- Don't change the formatting of the text file.

Example usage:

```python
from webscraper import search_jobs

search_keyword = "deep learning, machine learning"      # The keyword to search for jobs
search_location = "Luxembourg"                          # Preferred location of the jobs
keywords = ["data science", "physics", "science", "scientist", "trainee", "machine learning", "deep learning"]  # Keywords for job filtering
excluded_keywords = ["senior","head"]   # Keywords to exclude in the job title.
languages = ["en"]                      # List here the languages of the advertisement you are interested in.
                                        # See the documentation https://pypi.org/project/langdetect/ for abbreviations
N_pages = 1   # No.of pages to scrape through

jobs = search_jobs(search_keyword, search_location, keywords, excluded_keywords, languages, N_pages, show_window=True, search_mode='gemini')
```

## Output
The script saves positive results in the results directory:

- positive_results.json: JSON file with job details, URLs, and flags showing the suitability of the job with the user profile.
- positive_results.csv: CSV file with job titles, hyperlinked URLs, and flags showing the suitability of the job with the user profile.
