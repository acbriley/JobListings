import requests
from dotenv import load_dotenv
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import csv
import time

load_dotenv()
s = Service('/Users/andrewbriley/chromedriver')
driver = webdriver.Chrome(service=s)
driver.get('https://linkedin.com/uas/login')
email = os.getenv('USER_EMAIL')
password = os.getenv("USER_PASS")

time.sleep(5)

username = driver.find_element(By.ID, 'username')
pword = driver.find_element(By.ID, 'password')
username.send_keys(email)
pword.send_keys(password)

driver.find_element(By.XPATH, "//button[@type='submit']").click()

jobs = driver.find_element(
    By.XPATH, "//a[contains(@class, 'app-aware-link')]/span")
jobs.click()

job_src = driver.page_source
soup = BeautifulSoup(job_src, 'html.parser')
company_list_html = soup.select('.job-card-container__primary-description')
job_list_html = soup.find_all(class_='job-card-list__title')
links = soup.select('.base-card__full-link ')

for i, job in enumerate(job_list_html):
    job_list = []
    job_list.append(job.get_text())
    print(job_list)

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
