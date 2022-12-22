from dotenv import load_dotenv
import os
from selenium import webdriver
import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import date
import pandas as pd
import re

# set up driver and environment variables

load_dotenv()
chromedriver_autoinstaller.install()
driver = webdriver.Chrome()

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
jobs_info = []
for page in range(2, 3):
    print(f"Scraping Page: {page}")
    jobs_list = driver.find_elements(
        By.CSS_SELECTOR, '.jobs-search-results__list-item')
    n = 0
    for i in jobs_list:
        n += 1
        driver.execute_script("arguments[0].scrollIntoView();", jobs_list[n-1])
    time.sleep(10)

    link_element = driver.find_elements(
        By.CLASS_NAME, 'job-card-container__link')

    for link in link_element:
        if link.get_property('href') not in links and link.get_property('href').startswith('https://www.linkedin.com/jobs/view'):
            links.append(link.get_property('href').strip())

    driver.find_element(By.XPATH,
                        f"//button[@aria-label='Page {page}']").click()
    time.sleep(3)
for link in links:
    driver.get(link)
    time.sleep(2)
    try:
        if not driver.find_element(
                By.CSS_SELECTOR, '.jobs-unified-top-card__job-title'):
            break
        else:
            job_title = driver.find_element(
                By.CSS_SELECTOR, '.jobs-unified-top-card__job-title').text
            company = driver.find_element(
                By.CSS_SELECTOR, '.jobs-unified-top-card__company-name'
            ).text
            location = driver.find_element(
                By.CSS_SELECTOR, '.jobs-unified-top-card__bullet').get_property('innerHTML').strip()
            job_details = driver.find_element(
                By.CSS_SELECTOR, '#job-details').get_property('innerHTML')
            if driver.find_element(
                    By.CSS_SELECTOR, '.jobs-unified-top-card__workplace-type'):
                workplace_type = driver.find_element(
                    By.CSS_SELECTOR, '.jobs-unified-top-card__workplace-type').text
            else:
                workplace_type = ' '
            pattern = '<.*?>'
            job_details = re.sub(pattern, '', job_details)
            second_pattern = '\n'
            job_details = re.sub(second_pattern, '', job_details).strip()
            url = driver.current_url
            jobs_info.append(
                (job_title, company, location, workplace_type,  url, job_details))
    except Exception as err:
        print(err)


job_results = pd.DataFrame(
    jobs_info, columns=['Position', 'Company', 'Location', 'Workplace Type', 'Link', 'Job Details'])

# create an excel file
job_results.to_excel('data/linkedin-jobs' +
                     str(date.today()) + '.xlsx', index=False)

driver.close()
