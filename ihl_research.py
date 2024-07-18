# NOTE the for the excel sheet containing the names of the company names,
# The column containing the startup names should be labeled as Company (first letter in upper case)
# Also note that the file should be saved in CSV format and not xlsx

# There are 3 things that needs to be changed upon using the code:
# 1) The name of the CSV file (which contains the names of the local startups)
# 2) The API key 

# Test if code is responding
print("Code is starting...")

# import pandas for data handling
import pandas as pd

# import statements for web scraping
import os
import requests 
from bs4 import BeautifulSoup 
import urllib.parse
import re

# importing selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# import statement for optimisation of code
from multiprocessing import Pool

# This is a function to get the text from the website
def get_soup(url):
    try: 
        payload = { 'api_key': '99a541542a2746c4544b32d8e9000769', 'url': url}
        r = requests.get('https://api.scraperapi.com/', params=payload)
        # print(r.text)
   
        # soup = BeautifulSoup(r.text, 'lxml')
        soup = BeautifulSoup(r.text, 'html.parser')
        
        return soup
    except Exception as error:
        print("error occurred in get_soup function")
        print(error)

# This function scrapes the startups supported by sginnovate and a*star
def scrape_dynamic():
    try:

        # urls = ["https://www.a-star.edu.sg/enterprise/innovation-platforms/a-startcentral/our-community", 
        #        "https://www.sginnovate.com/apprenticeship/organisations", "https://www.sginnovate.com/power-x-talent",
        #        "https://www.sginnovate.com/our-portfolio"]

        urls = ["https://www.a-star.edu.sg/enterprise/innovation-platforms/a-startcentral/our-community"]
        
        names = ["A*STAR"]

        # url = "https://www.a-star.edu.sg/enterprise/innovation-platforms/a-startcentral/our-community"

        for url, name in zip(urls, names):

            driver = webdriver.Chrome()

            driver.get(url)

            img_tags = driver.find_elements(By.TAG_NAME, 'img')

            companies = []
            for tag in img_tags:
                alt_text = tag.get_attribute('alt')
                if alt_text:
                    companies.append(alt_text)

            # print(companies)

            results = pd.DataFrame(companies, columns=["Startups"])

            results.insert(0, 'Organisation', name)

            # print(results)

        return results
    
    except Exception as error:
        print("error ocurred in scrape_dynamic function")
        print(error)

    finally:
        driver.quit()


if __name__ == "__main__":

    # nus = pd.read_csv('nus.csv')

    # ntu = pd.read_csv('ntu.csv')

    others = scrape_dynamic()

    # merged_df = pd.concat([nus, ntu, others], ignore_index=True)

    print("Merging CSVs...")

    others.to_csv('merged_data.csv', index=False)

    print("Merged successfully")