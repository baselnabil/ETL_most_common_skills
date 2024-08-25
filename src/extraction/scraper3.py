
import re
import csv
from jobspy import scrape_jobs
import spacy
from spacy import displacy
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.matcher import PhraseMatcher

from skillNer.general_params import SKILL_DB
# import skill extractor
from skillNer.skill_extractor_class import SkillExtractor

from collections import Counter
import math





jobs = scrape_jobs(
    site_name=["indeed", "linkedin", "zip_recruiter", "glassdoor"],
    search_term="Data engineer",
    location="New York, NY",
    results_wanted=10,
    hours_old=168, # (only Linkedin/Indeed is hour specific, others round up to days old)
    country_indeed='USA',  # only needed for indeed / glassdoor
    
    # linkedin_fetch_description=True # get full description , direct job url , company industry and job level (seniority level) for linkedin (slower)
    # proxies=["208.195.175.46:65095", "208.195.175.45:65095", "localhost"],
    
)
print(f"Found {len(jobs)} jobs")




print(jobs.loc[1].description)




nlpp = spacy.load("en_core_web_lg")
skill_extractor = SkillExtractor(nlpp, SKILL_DB, PhraseMatcher)
skill_counter = Counter()

descriptions = jobs['description'].dropna().tolist()

for doc in nlpp.pipe(descriptions, batch_size=30): 
    try:
        if not doc.text.strip():
            continue
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
        print(f"Error processing description: {doc.text[:50]}...") 
        continue
    except ValueError as ee:
        print(f"Error processing description: {doc.text[:50]}...") 
        continue
skill_counter




most_common_skills = skill_counter.most_common()

output_file = '../../data/raw/data3.csv'

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)
    
    writer.writerow(['Skill', 'Count'])
    
    writer.writerows(most_common_skills)

print(f"Most common skills have been written to {output_file}")




# custom_stopwords = {"knowledge", "comment", "degree", "experience", "good", "must", "solid", 
#                     "understanding", "years", "working", "teams", "projects", "results", 
#                     "responsibilities", "comments", "develop", "engineering", "systems", "tools",
#                     "development", "standards", "value", "cost", "generate", "needed", "documentation", "our", "your"
#                     "diagrams", "analyse", "business", "performance", "security", "methodology", "multidisciplinary areas", "all",
#                     "plus", "influence", "overall", "a must", "the standards", "all levels", "the", "why", "master", "customers", "a ", "national", "veteran"}

# #stopwords = STOP_WORDS.union(custom_stopwords)



