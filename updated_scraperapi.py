# NOTE: for the excel sheet containing the names of the company names,
# The column containing the startup names should be labeled as Company (first letter in uppercase)
# Also note that the file should be saved in CSV format and not xlsx

# There are 2 things that needs to be changed upon using the code:
# 1) The name of the CSV file (which contains the names of the local startups)
# 2) The API key 

# Test if code is responding
print("Code is starting...")

# import pandas for data handling
import pandas as pd

# import statements for web scraping
import requests 
from bs4 import BeautifulSoup 
import urllib.parse

# import statement for optimisation of code
from multiprocessing import Pool

# This is a function to get the text from the website
def get_soup(url):
    try: 
        # Change the API key here
        # API helps to bypass in built anti bot measures on pitchbook
        payload = { 'api_key': '10d1b400970449ebfb6c41d4a7992d59', 'url': url }
        r = requests.get('https://api.scraperapi.com/', params=payload)
        # print(r.text)
   
        soup = BeautifulSoup(r.text, 'html.parser')
        
        return soup
    except Exception as error:
        print(error)

# This function scrapes the search results and narrows the search to 
# return one link which belongs to a locally owned company
def scrape_search_bar(keyword):
    try:
        # Create url to access the pitchbook search bar based on the company name
        url = f"https://pitchbook.com/profiles/search?q={urllib.parse.quote(keyword)}"
        print("this is the url: " + url)

        # Retrieve information from the search results
        soup = get_soup(url)

        # Get the links to each profile page from the pitchbook search bar
        links = soup.find_all("a", class_="py-xl-20 flex-centered-container")

        # Put the links into an array
        arr = ['https://pitchbook.com' + link["href"] for link in links]

        # Filter out the links to get the profiles of the startup
        # (Filter out investors or any other types of entities since we only want startups) 
        arr = list(filter(lambda link : "company" in link, arr))

        print("This is arr: ")
        print(arr)

        # If there is only one search result, that link is probably correct
        if len(arr) == 1:
            return arr
        else:
            # If there is more than one search result...
            print("we are in the else block")
            sg_companies = []

            count = 0

            # Iterate through the first 15 search results 
            for link in arr[:15]:
                # Go into each of the links and retrieve information about each of the companies
                company_soup = get_soup(link)
                desc = company_soup.find("ul", class_="list-type-none XL-12")
                count += 1

                # If the company is located in Singapore, take this search result
                if "Singapore" in desc.get_text():
                    print("This is the count")
                    print(count)
                    sg_companies.append(link)
                    break
                    

            print("array of sg companies: ", sg_companies)
            return sg_companies
    
    except:
        return "No records found"

# This function checks if the company has a patent
def check_patent(link):
    try: 
        # Retrieve information of the company through the company profile
        profile_soup = get_soup(link)

        # Retrieve the description of the company
        description = profile_soup.find("p", class_="pp-description_text mb-xl-0")

        # Retrieve the website of the company
        url = profile_soup.find("span", class_="ellipsis-XL d-block-XL")

        # If there is no company website found, return None (which is nothing)
        url_text = url.text if url else None

        # If there is no company description found, return None (which is nothing)
        description_text = description.text if description else None

        print(url_text)

        # Extracting the information if the startup has a patent FILED
        patent = profile_soup.find("h3", class_="pp-patents__value shift-top-XL-0 shift-bottom-XL-5")

        patent_boolean = None

        # If there is a value in the patent field on the company profile...
        if patent is not None:
            # Then there is a patent
            patent_boolean = "TRUE"    
        else:
            # Else, there is no patent filed by the company
            patent_boolean = "FALSE"

        # return information on the company website, description and TRUE/FALSE if there is a patent
        return url_text, description_text, patent_boolean
    
    except Exception as error:
        print("Error in check_patent function")
        print(error)
        return None, None, None

# This function checks if there are singaporean comapanies and if there is any, check for patents
# If not, return nothing
def litmus(keyword):
    sg_companies = scrape_search_bar(keyword)
    if not sg_companies:
        return "", "", ""
    elif len(sg_companies) == 1:
        company_link = sg_companies[0]
        url, desc, patent_boolean = check_patent(company_link)
        return url, desc, patent_boolean
    else:
        return "", "", ""

if __name__ == "__main__":
    # TODO: Change the name of the file
    # Read the CSV file of company names you would like to categorise
    startup_info = pd.read_csv(r"C:\Users\Gabrielle Gianna Tan\Downloads\2021.csv")

    # # Check if the file is reading 
    # print(startup_info.head())

    # Split the work up into pools so the code can run concurrently for different keywords
    with Pool(processes=4) as pool:
        results = pool.map(litmus, startup_info['Company'])

    # Extract the 'Company' column from startup_info
    companies = startup_info['Company'].values

    # Create new columns and put in the results for the company website, description and if there are patents
    results_df = pd.DataFrame(results, columns=['Website', 'Description', 'Patent (True/False)'])

    # Insert 'Company' column as the first column
    results_df.insert(0, 'Company', companies)

    # Write the result to a new CSV file
    results_df.to_csv("patent_startups_list.csv", index=False)
