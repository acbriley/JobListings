import requests
from bs4 import BeautifulSoup
import csv

website = 'https://www.linkedin.com/jobs/search?keywords=Junior%2BSoftware%2BDeveloper&location=Barcelona%2C%20Catalonia%2C%20Spain&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
res = requests.get(website)
soup = BeautifulSoup(res.text, 'html.parser')
companies = soup.select('.base-search-card__subtitle')
jobs = soup.select('.base-search-card__title')
links = soup.select('.base-card__full-link ')


def create_job_list(jobs, companies, links):
    job_list = []
    for i, j in enumerate(jobs):
        job_list.append([i, j.get_text().strip(), i+1])
    for i, c in enumerate(companies):
        job_list[i][0] = c.get_text().strip()
    for i, l in enumerate(links):
        job_list[i][2] = l.get('href')
    return job_list


create_job_list(jobs, companies, links)

header = ['Company Name', 'Job Title',  'URL']
data = create_job_list(jobs, companies, links)

with open('jobs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(header)
    writer.writerows(data)
