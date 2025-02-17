
from webscraper import search_jobs

search_keyword = "deep learning, machine learning"      # The keyword to search for jobs
search_location = "Netherlands"                          # Preferred location of the jobs
keywords = ["data science", "physics", "science", "scientist", "trainee", "machine learning", "deep learning"]  # Keywords for job filtering
excluded_keywords = ["senior","head","Sr ","Sr."]   # Keywords to exclude in the job title.
languages = ["en"]                      # List here the languages of the advertisement you are interested in.
                                        # See the documentation https://pypi.org/project/langdetect/ for abbreviations
N_pages = 10   # No.of pages to scrape through

jobs = search_jobs(search_keyword, search_location, keywords, excluded_keywords, languages, N_pages, 
                   show_window=True, search_mode='openai')


