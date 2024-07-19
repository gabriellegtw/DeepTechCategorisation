# DeepTechCategorisation

Motivation: I was tasked with categorising startups by their type (ie Deep Tech or Non Deep Tech) and was provided with an excel sheet of the names of the startups. A Deep Tech startup is defined as one that has filed for patents or are doing existing research with a higher institute of learning (IHLs) (eg. universities or other research focussed entities). Doing this manually for a large number of startups would take a large amount of time as I would have to google each of the names, find the website, read their descriptions and find out if they have patents and/or done research with IHLs.

Workflow:

1) Run the updated_scraper.py file to extract the descriptions of the startups
The code scrapes Pitchbook to obtain the descriptions of the startups, their websites adn a boolean (TRUE/FALSE) as to whether the startup has filed a patent or not. The startups with patents can be automatically classfied as a Deep Tech startup

2) Run 
