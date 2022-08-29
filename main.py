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

# find job button and click it
jobs = driver.find_element(
    By.XPATH, '//*[@id="global-nav"]/div/nav/ul/li[3]/a')

jobs.click()

job_src = driver.page_source

# parse HTML to find elements of job post
soup = BeautifulSoup(job_src, 'html.parser')
job_cards = soup.select('.job-card-list__entity-lockup ')
job_list_html = soup.select('.job-card-list__title')
print(job_list_html)

for card in job_cards:
    print(card.text)


# job_list = []
# job_list.append(job.get_text())
# print(job_list)

links = soup.select('.base-card__full-link ')
company_list_html = soup.select('.job-card-container__primary-description')


# def create_job_list(job_list_html, company_list_html, links):
#     job_list = []
#     for i, j in enumerate(job_list_html):
#         job_list.append([i, j.get_text().strip(), i+1])
#     for i, c in enumerate(company_list_html):
#         job_list[i][0] = c.get_text().strip()
#     for i, l in enumerate(links):
#         job_list[i][2] = l.get('href')
#     return job_list


# print(create_job_list(job_list_html, company_list_html, links))

# header = ['Company Name', 'Job Title',  'URL']
# data = create_job_list(jobs, companies, links)

# with open('jobs.csv', 'w', encoding='UTF8', newline='') as f:
#     writer = csv.writer(f)

#     writer.writerow(header)
#     writer.writerows(data)
