import requests
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 2000)

url = 'https://www.cvmarket.lt/'

service = Service(ChromeDriverManager().install())
service.start()

driver = webdriver.Chrome(service=service)

job_data = []
driver.get(url)



# print(response)

category_select_list = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#search\[categories\]\[\]_Label')))
category_select_list.click()
category_select = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#search\[categories\]\[\]_Dropdown > ul:nth-child(1) > li:nth-child(10)')))
driver.execute_script('arguments[0].scrollIntoView();', category_select)
time.sleep(3)
category_select.click()
apply = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#search\[categories\]\[\]_Apply')))
apply.click()
search = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
    (By.CSS_SELECTOR, '#button_65b26ad061e98')))
time.sleep(3)
search.click()
time.sleep(100)
for _ in range(0, 5):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    ads = soup.find_all('article', {'data-component':'jobad'})
    for ad in ads:
        job_title = ad.find('h2', class_='xl:text-xl font-bold mt-2 hover:underline').text.strip()
        company = ad.find('span', class_='job-company mr-5').text.strip()
        salary_min_d = ad.find('div', {'data-salary-from': True})
        if salary_min_d:
            salary_min = salary_min_d['data-salary-from']
        else:
            salary_min = 'N/A'
        salary_max_d = ad.find('div', {'data-salary-to': True})
        if salary_max_d:
            salary_max = salary_max_d['data-salary-to']
        else:
            salary_max = 'N/A'
        salary_type_d = ad.find('span', class_='text-slate-200 visited-group:text-gray-300 text-sm font-bold mt-0.5 salary-type')
        if salary_type_d:
            salary_type = salary_type_d.text.strip()
        else:
            salary_type = 'N/A'
        location = ad.find('span', class_='bg-blue-50 text-slate-500 py-1.5 px-3 font-bold text-sm rounded-full flex w-fit h-fit justify-center items-center space-x-1.5 cursor-defaults leading-4 location').text.strip()
        salary_period_data = ad.find('div', class_='inline-block mt-2.5 lg:mt-0 salary-block mr-5')
        if salary_period_data:
            if 'mėn' in salary_period_data.text.strip():
                salary_period = 'Mėnesinis'
            elif 'val' in salary_period_data.text.strip():
                salary_period = 'Valandinis'
        else:
            salary_period = 'Unknown'
        posted_when = ad.find('div', class_='whitespace-nowrap').text.strip()
        job_data.append({
            'Pavadinimas': job_title,
            'Įmonė': company,
            'Min atlyginimas': salary_min,
            'Max atlyginimas': salary_max,
            'Atlyginimo tipas': salary_type,
            'Atlyginimo tipas2': salary_period,
            'Patalpinta': posted_when
        })

df = pd.DataFrame(job_data)
df = df.drop_duplicates()
print(df)