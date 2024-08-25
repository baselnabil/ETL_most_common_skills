import os
filename = os.path.basename(__file__)
yellow_text = "\033[93m"
print(f"{yellow_text}Intializing {filename}...")

import re
import csv
from jobspy import scrape_jobs
import spacy
from spacy.matcher import PhraseMatcher
from skillNer.general_params import SKILL_DB
from skillNer.skill_extractor_class import SkillExtractor
from collections import Counter
import math

 
#### CONSTANTS
RESULTS_WANTED = 40
HOURS_OLD = 168
SPACY_MODEL = "en_core_web_lg"
OUTPUT_FILE = '../../data/raw/data3.csv'


print(f"{yellow_text}{filename}: Fetching jobs...")

jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
    search_term="Data engineer",
    location="New York, NY",
    results_wanted=RESULTS_WANTED,
    hours_old=HOURS_OLD, # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='USA',  # only needed for indeed / glassdoor
    
    
)

descriptions = jobs['description'].dropna().tolist()

print(f"{yellow_text}{filename}: Found {len(jobs)} jobs, of which {len(descriptions)} had valid descriptions.")

print(f"{yellow_text}{filename}: Loading spacy model ({SPACY_MODEL}) and skill extractor...")

nlpp = spacy.load(SPACY_MODEL)
skill_extractor = SkillExtractor(nlpp, SKILL_DB, PhraseMatcher)
skill_counter = Counter()


print(f"{yellow_text}{filename}: Processing job descriptions...")

for description in descriptions:
    lines = [line for line in description.splitlines() if line.strip()]
    
    for line in lines:
        try:
            doc = nlpp(line) 
            sanitized_text = re.sub(r'[^a-zA-Z\s]', '', doc.text)
            annotations = skill_extractor.annotate(sanitized_text)
            
            for item in annotations['results']['ngram_scored']:
                skill = item['doc_node_value'].lower()
                score = item['score']
                toAddScore = math.floor(score)
                if toAddScore == 0:
                    continue
                skill_counter[skill] += toAddScore
        except IndexError as e:
            print(f"Error processing line: {line[:50]}...") 
            continue
        except ValueError as ee:
            print(f"Error processing line: {line[:50]}...") 
            continue



most_common_skills = skill_counter.most_common()


with open(OUTPUT_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Skill', 'Count'])
    
    writer.writerows(most_common_skills)

print(f"Most common skills have been written to {OUTPUT_FILE}")




# custom_stopwords = {"knowledge", "comment", "degree", "experience", "good", "must", "solid", 
#                     "understanding", "years", "working", "teams", "projects", "results", 
#                     "responsibilities", "comments", "develop", "engineering", "systems", "tools",
#                     "development", "standards", "value", "cost", "generate", "needed", "documentation", "our", "your"
#                     "diagrams", "analyse", "business", "performance", "security", "methodology", "multidisciplinary areas", "all",
#                     "plus", "influence", "overall", "a must", "the standards", "all levels", "the", "why", "master", "customers", "a ", "national", "veteran"}

# #stopwords = STOP_WORDS.union(custom_stopwords)



