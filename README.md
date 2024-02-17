# Europass Webscraper

This Python script utilizes Selenium to scrape job listings from the Europass website based on specified keywords. The script then filters the jobs and saves positive results in both JSON and CSV formats.

## Prerequisites

Before running the script, make sure to install the required dependencies:

```bash
pip install selenium tqdm langdetect
```

## Configuration
Adjust the following parameters in the script according to your requirements:

- options.add_argument("--headless=new"): Uncomment to run in headless mode (without displaying the browser window).
- search_keywords: Main keywords to start the search.
- search_location: Preferred location of the jobs.  
- keywords: Results are shown positive if any of the word in this list is present in the job description.
- excluded_keywords: Exclude the results if any of the word in this list is present in the job title.
  - Eg. for entry level jobs, exclude words like 'senior', 'head' etc. 
- languages: Filter the job ads by this list of languages.
- N_pages: Set the number of pages to scrape.


## Output
The script saves positive results in the results directory:

- positive_results.json: JSON file with job details and URLs.
- positive_results.csv: CSV file with job titles and hyperlinked URLs.
