import csv
from jobspy import scrape_jobs
import pandas as pd 





jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
    search_term="Data engineer",
    location="New York, NY",
    results_wanted=1,
    hours_old=168, # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='USA',  # only needed for indeed / glassdoor
    
    # linkedin_fetch_description=True # get full description , direct job url , company industry and job level (seniority level) for linkedin (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    
)
print(f"Found {len(jobs)} jobs")
print(jobs.head())
cleaned_df = pd.DataFrame(jobs)
cleaned_df=cleaned_df.drop('description',axis=1)
cleaned_df.to_csv("../../data/raw/data1.csv", quoting=csv.QUOTE_NONNUMERIC, escapechar="\\", index=False) # to_excel