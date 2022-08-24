import requests
from bs4 import BeautifulSoup
import pprint

root = 'https://www.linkedin.com/jobs/search?keywords=Junior%2BSoftware%2BDeveloper&location=Barcelona%2C%2BCatalonia%2C%2BSpain&geoId=105088894&distance=25&f_E=2&currentJobId=3212513876&position=2&pageNum=0'
# for page in range(1, 10):
website = f'{root}'
res = requests.get(website)
soup = BeautifulSoup(res.text, 'html.parser')
jobs = soup.select('.base-search-card__title')


def get_jobs(jobs):
    job_posts = []
    for title in jobs:
        job_posts.append(title.get_text().strip())
    print(job_posts)


get_jobs(jobs)
