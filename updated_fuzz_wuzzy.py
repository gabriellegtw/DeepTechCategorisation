import pandas as pd
from fuzzywuzzy import process
from concurrent.futures import ThreadPoolExecutor

# Load the CSV file
excel = pd.read_csv(r"C:\Users\Gabrielle Gianna Tan\Downloads\company_full (1).csv", low_memory=False)

# Extract the relevant columns
company = excel["Company"].values
compare = excel["Company_compare"].values

# Define the fuzzy matching function
def get_best_match(name, choices):
    best_match, score = process.extractOne(name, choices)
    return name, best_match, score

# Define a function to run fuzzy matching in parallel
def fuzzy_match_in_parallel(names, choices):
    results = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_best_match, name, choices) for name in names]
        for future in futures:
            print("future")
            results.append(future.result())
    return results

# Perform fuzzy matching in parallel and store results
results = fuzzy_match_in_parallel(company, compare)

# Convert the results to a DataFrame
results_df = pd.DataFrame(results, columns=['Company', 'Best_Match', 'Score'])

# Merge the results back to the original dataframe if needed
final_df = pd.merge(excel, results_df, on='Company', how='left')

# Save the final dataframe to a new CSV file
final_df.to_csv(r"C:\Users\Gabrielle Gianna Tan\Downloads\company_matched.csv", index=False)

print("CSV created successfully!")