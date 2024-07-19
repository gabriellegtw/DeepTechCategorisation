# DeepTechCategorisation

Motivation: I was tasked with categorising startups by their type (ie Deep Tech or Non Deep Tech) and was provided with an excel sheet of the names of the startups. A Deep Tech startup is defined as one that has filed for patents or is doing existing research with a higher institute of learning (IHLs) (eg. universities or other research focussed entities). Doing this manually for a large number of startups would take a large amount of time as I would have to google each of the names, find the website, read their descriptions and find out if they have patents and/or done research with IHLs.

Workflow:

1) Run the updated_scraperapi.py file to extract the descriptions of the startups (Made using Beautiful Soup and Pandas)
The code scrapes Pitchbook to obtain the descriptions of the startups, their websites and a boolean (TRUE/FALSE) as to whether the startup has filed a patent or not. The startups with patents can be automatically classified as a Deep Tech startup

2) Run the ihl_rsearch.py file to scrape websites of IHLs to obtain a list of startups which the IHLs have collaborated with (Made using Selenium)
This generates a csv file of startups which the IHLs have collaborated with. A vlookup can be done with the original excel sheet to check which startups have done research with the IHLs. As there may be some cases where the company names may not be an exact match (eg. "Company X" and "Company X Pte Ltd"), updated_fuzz_wuzzy.py (made using the FuzzyWuzzy library in python) can be used to detect these matches. Companies with research backing can be automatically classified as a Deep Tech startup.

3) [In progress] Run the naive_bayes.py file to categorise remaining startups based on their descriptions (Made using Scikit-Learn and Natural Language Processing Toolkit)
There may be some startups that have not filed patents on research but produce novel products (and hence can be classfied as a deep tech startup). Using the Naive Bayes algorithm and NLTK, I plan to be able to automatically categorise the startups based on their descriptions. I have also tried other algorithms such as Random Forest, Logistic Regression and K-Nearest, but Naive Bayes yielded the highest accuracy, precision and f1-score.
