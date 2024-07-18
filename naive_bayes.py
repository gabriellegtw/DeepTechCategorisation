import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

nltk.download("popular")
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('wordnet')

import pandas as pd
import numpy as np

def preprocess_words(words):

    # Converts to lower case
    words = words.lower()

    # Spilt the words up
    words = word_tokenize(words)

    # Checks if the words are actual words
    words = [w for w in words if w.isalpha()]

    # Get rid of stop words (ie words like "a", "is", "are", etc.)
    stop_words = set(stopwords.words('english'))
    words = [word for word in words if word not in stop_words]

    # Lemmatising the word (ie getting the base word [walking -> walk])
    lemmatizer = WordNetLemmatizer()
    words = [lemmatizer.lemmatize(word) for word in words]

    # Join words back
    words = ' '.join(words)

    return words


from sklearn.feature_extraction.text import TfidfVectorizer

data = pd.read_csv(r"C:\Users\Gabrielle Gianna Tan\Downloads\cleaned_2023 training.csv")

# Map the "Non Deep Tech" category to the number 0 and the "Deep Tech" category to the number 1
data['category_num'] = data.category.map({
    'Non Deep Tech': 0,
    'Deep Tech': 1
})

desc = data["pitchbook_description"].values

# Converting the data frame to a series first so we can apply the function
desc_series = pd.Series(desc)

# applying the preprocess_words function
new_desc = desc_series.map(preprocess_words)

repl_desc = new_desc.to_frame()

data["pitchbook_description"] = repl_desc

# df = new_desc.to_frame()

# print(data.head())

# Term Frequency Inverse Document Frequency
tfid = TfidfVectorizer()

# Generates a sparse matrix (meaning that most elements in the matrix are zero)
# adnd generates a tfidf score for each of the decriptions
output = tfid.fit_transform(new_desc)

# print(output)

from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    data.pitchbook_description,
    data.category_num,
    test_size=0.2,
    random_state=2022,
    stratify=data.category_num
)

# print(y_train.value_counts())

from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import confusion_matrix, classification_report
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.metrics import accuracy_score

# Pipeline to classify the text
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer()),  # Convert text to numerical TF-IDF features
    ('to_dense', FunctionTransformer(lambda x: x.toarray(), accept_sparse=True)),
    ('gnb', GaussianNB())          # Gaussian Naive Bayes classifier
])

# Fit the classifier to the data
pipeline.fit(X_train, y_train)

# Make predictions on the test data
y_pred = pipeline.predict(X_test)

# Printing the descriptions of the first 5 test results of the 
# testing set
print(X_test[:5])

# Printing the actual "answers" to the first 5 test results
print(y_test[:5])

# Printing out the answers given by the code
print(y_pred[:5])

# Output confusion matrix, classification report and accuracy score
print(confusion_matrix(y_test, y_pred))
print(classification_report(y_test, y_pred))
print(accuracy_score(y_test, y_pred))