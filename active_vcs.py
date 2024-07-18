# NOTE the for the excel sheet containing the names of the company names,
# The column containing the investor names should be labeled as Company (first letter in upper case)
# Also note that the file should be saved in CSV format and not xlsx

# There are 3 things that needs to be changed upon using the code:
# 1) The name of the CSV file (which contains the names of the local startups)
# 2) The API key 
# 3) The lower and upper bound of the threshold dates

# Test if code is responding
print("Code is starting...")

# import pandas for data handling
import pandas as pd

# import statements for web scraping
import os
import requests 
from bs4 import BeautifulSoup 

# import statement for optimisation of code
from multiprocessing import Pool

# This is a function to get the text from the website
def get_soup(url):
    try: 
        # TODO
        # Type new ZenRows API Key here
        api_key = 'e63f59e54aa1acb46e6e94a9ffde8956d0a93c16'
        response = requests.get(f'https://api.zenrows.com/v1/?apikey={api_key}&url={url}')
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except:
        print("Oh no, get another ZenRows API Key!")
        return "Oh no, get another ZenRows API Key!"

# This function scrapes the search results and narrows the search to 
# return one link which belongs to a locally owned company
def scrape_search_bar(keyword):
    try:
        url = 'https://pitchbook.com/profiles/search?q=' + keyword
        soup = get_soup(url)
        links = soup.find_all("a", class_="py-xl-20 flex-centered-container")
        arr = ['https://pitchbook.com' + link["href"] for link in links]
        arr = list(filter(lambda link : "investor" in link, arr))

        if len(arr) == 1:
            return arr
        else:
            sg_companies = []

            for link in arr[:10]:
                company_soup = get_soup(link)
                desc = company_soup.find("ul", class_="list-type-none XL-12")

                if "Singapore" in desc.get_text():
                    sg_companies.append(link)

            return sg_companies
    
    except:
        return "No records found"

# This function checks if the company is active
def check_year(link):
    profile_soup = get_soup(link)
    date = profile_soup.find("td", class_="data-table__cell data-table__cell_max90 align-left font-color-black pl-xl-10")

    if date is not None:

        year = date.get_text()[-4:]

        if year.isdigit():
            # TODO
            # Change this (upper and lower bound for years)
            return int(year) >= 2023 and int(year) <= 2024
        else:
            return "Year undetected"
        
    else:
        return "Date not found in " + link

# Litmus test if the company is active or not
def litmus(keyword):
    sg_companies = scrape_search_bar(keyword)
    if not sg_companies:
        return "No Singapore-based investors found"
    elif len(sg_companies) == 1:
        company_link = sg_companies[0]
        bool = check_year(company_link)
        return bool
    else:
        return "More than 1 entity found"

if __name__ == "__main__":
    # TODO: Change the name of the file
    # Read the CSV file
    vc_info = pd.read_csv(r"C:\Users\Gabrielle Gianna Tan\Downloads\VCs_complete_test.csv")

    # # Check if the file is reading 
    # print(vc_info.head())

    # Split the work up into pools so the code can run concurrently for different keywords
    with Pool(processes=4) as pool:
        results = pool.map(litmus, vc_info['Company'])

    # Add the results to the DataFrame
    vc_info['Active (True/False)'] = results

    # Write the result to a new CSV file
    vc_info.to_csv("active_vcs_list.csv", index=False)
