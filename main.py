import requests
from bs4 import BeautifulSoup
import csv

website = 'https://www.linkedin.com/jobs/search?keywords=Junior%2BSoftware%2BDeveloper&location=Barcelona%2C%20Catalonia%2C%20Spain&geoId=&trk=public_jobs_jobs-search-bar_search-submit&position=1&pageNum=0'
res = requests.get(website)
soup = BeautifulSoup(res.text, 'html.parser')
companies = soup.select('.base-search-card__subtitle')
jobs = soup.select('.base-search-card__title')


def create_job_list(jobs, companies):
    job_list = []
    for i, j in enumerate(jobs):
        job_list.append([i, j.get_text().strip()])
    for i, c in enumerate(companies):
        job_list[i][0] = c.get_text().strip()
    return job_list


create_job_list(jobs, companies)

header = ['Company Name', 'Job Title']
data = create_job_list(jobs, companies)

with open('jobs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(header)
    writer.writerows(data)
