




import requests
from bs4 import BeautifulSoup
import csv
from itertools import zip_longest
import lxml





#lists
jobTitles=[]
companyNames=[]
locations=[]
experiences=[]
#fetch website
pageNumber= 0




while True:
    result = requests.get(f"https://wuzzuf.net/search/jobs/?a=hpb&q=python&start={pageNumber}")
    #get the content
    src = result.content
    #soup
    soup = BeautifulSoup(src,"lxml")
    #get elements
    jobTitle= soup.find_all("a",{"class":"css-o171kl","rel":"noreferrer"})
    companyName = soup.find_all("a",{"class":"css-17s97q8"})
    location = soup.find_all("span",{"class":"css-5wys0k"})
    experience = soup.find_all("div",{"class":"css-1lh32fc"})

    for i in range(len(jobTitle)):
        jobTitles.append(jobTitle[i].text)
        companyNames.append(companyName[i].text)
        locations.append(location[i].text)

    for exp in experience:
        filtering = exp.nextSibling.text
        experiences.append(filtering)
    pageLimit = int(soup.find("strong").text)
    if (pageNumber> pageLimit//15):
        print("end")
        break
    pageNumber+=1
    print("page switched")




fileLists = [jobTitles,companyNames,locations,experiences]
export =zip_longest(*fileLists)
with open("../../data/raw/data2.csv","w") as file:
    wr=csv.writer(file)
    wr.writerow(["Jobtitle","Companyname","Locations","Skills"])
    wr.writerows(export)

