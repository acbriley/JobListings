import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time

# set up driver and environment variables

load_dotenv()
s = Service('/Users/andrewbriley/chromedriver')
driver = webdriver.Chrome(service=s)

# log into linkedin

driver.get('https://linkedin.com/uas/login')
email = os.getenv('USER_EMAIL')
password = os.getenv("USER_PASS")

time.sleep(5)

username = driver.find_element(By.ID, 'username')
pword = driver.find_element(By.ID, 'password')
username.send_keys(email)
pword.send_keys(password)

driver.find_element(By.XPATH, "//button[@type='submit']").click()

driver.get('https://www.linkedin.com/jobs/collections/recommended/')
# web driver waits to perform next action until it can find elements w/ speciifc class
try:
    WebDriverWait.until(EC.presence_of_all_elements_located((
        By.CLASS_NAME, 'job-card-list__title')))

except Exception as e:
    print(e)

# simulate scrolling
driver.execute_script(
    'res = document.querySelector("#main > div > section.scaffold-layout__list > div"); res.scrollTo(0, res.scrollHeight)')
time.sleep(2)

job_src = driver.page_source

# parse HTML to find elements of job post
soup = BeautifulSoup(job_src, 'html.parser')
job_cards = soup.select('.job-card-list__entity-lockup')
job_list_html = soup.select('.job-card-list__title')
# for job in job_list_html:
#     job_list = []
#     job_list.append(job.text)
#     print(job_list)

links = soup.select('.job-card-container__link')
company_list_html = soup.select('.job-card-container__company-name')


def create_job_list(job_list_html, company_list_html, links):
    job_list = []
    for i, j in enumerate(job_list_html):
        job_list.append([i, j.get_text().strip()])
    for i, c in enumerate(company_list_html):
        job_list[i][0] = c.get_text().strip()
    for i, l in enumerate(links):
        job_list[i].append(l.get('href'))
    return job_list


print(create_job_list(job_list_html, company_list_html, links))

# header = ['Company Name', 'Job Title',  'URL']
# data = create_job_list(jobs, companies, links)

# with open('jobs.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)

#     writer.writerow(header)
#     writer.writerows(data)
