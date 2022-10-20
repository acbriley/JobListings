from turtle import pos
from dotenv import load_dotenv
import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

# set up driver and environment variables

load_dotenv()
s = Service('/Users/andrewbriley/downloads/chromedriver')
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
job_src = driver.page_source

# web driver waits to perform next action until it can find elements w/ speciifc class
try:
    WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((
        By.CLASS_NAME, 'job-card-container')))

except Exception as e:
    print(e)

links = []
companies = []
positions = []
for page in range(2, 11):
    print(f"Scraping Page: {page}")
    jobs_list = driver.find_elements(
        By.CSS_SELECTOR, '.jobs-search-results__list-item')
    n = 0
    for i in jobs_list:
        n += 1
        driver.execute_script("arguments[0].scrollIntoView();", jobs_list[n-1])
    time.sleep(10)

    job_position_element = driver.find_elements(
        By.CLASS_NAME, 'job-card-list__title')
    for job in job_position_element:
        positions.append(job.get_property('innerHTML').strip())

    company_element = driver.find_elements(
        By.CLASS_NAME, 'job-card-container__company-name')
    for company in company_element:
        companies.append(company.get_property('innerHTML').strip())

    link_element = driver.find_elements(
        By.CLASS_NAME, 'job-card-container__link')
    for link in link_element:
        if link.get_property('href') not in links and link.get_property('href').startswith('https://www.linkedin.com/jobs/view'):
            links.append(link.get_property('href').strip())

    driver.find_element(By.XPATH,
                        f"//button[@aria-label='Page {page}']").click()
    time.sleep(3)

job_results = pd.DataFrame({
    'Job Title': positions,
    'Hiring Company': companies,
    'Links': links
})

# create an excel file
job_results.to_excel('linkedin-jobs.xlsx', index=False)

driver.close()
