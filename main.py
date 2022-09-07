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

driver.get('https://www.linkedin.com/jobs/search/?currentJobId=3235585779&distance=25&f_E=2%2C3&f_TPR=r604800&geoId=105088894&keywords=software%20developer&location=Barcelona%2C%20Catalonia%2C%20Spain&refresh=true&sortBy=DD')
driver.set_window_size(1920, 1080)

# web driver waits to perform next action until it can find elements w/ speciifc class
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
        By.CLASS_NAME, 'job-card-container')))

except Exception as e:
    print(e)

# simulate scrolling
driver.execute_script(
    'res = document.querySelector("#main > div > section.scaffold-layout__list > div"); res.scrollBy(0, 1080)')
time.sleep(2)
job_src = driver.page_source

# parse HTML to find elements of job post
soup = BeautifulSoup(job_src, 'html.parser')

job_list_html = soup.select('.job-card-list__title')
# chain 2 classes to get only job post link
links = soup.select('.job-card-container__link.job-card-list__title')
company_list_html = soup.select('.job-card-container__company-name')

# function to add job information into a list


def create_job_list(job_list_html, company_list_html, links):
    job_list = []
    for i, j in enumerate(job_list_html):
        job_list.append([i, j.get_text().strip()])
    for i, c in enumerate(company_list_html):
        job_list[i][0] = c.get_text().strip()
    for i, l in enumerate(links):
        link = l.get('href')
        job_list[i].append('https://linkedin.com' + link)
    return job_list


# CSV file logic
header = ['Company Name', 'Job Title',  'LinkedIn URL']
data = create_job_list(job_list_html, company_list_html, links)
# create CSV file w/ writing mode
with open('linkedin-jobs.csv', 'w', encoding='UTF8', newline='') as f:
    writer = csv.writer(f)

    writer.writerow(header)
    writer.writerows(data)

driver.close()
