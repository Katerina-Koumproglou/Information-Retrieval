import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

text = ["hello", "kbeiei", "world"]
def process_content(text):
    #Tokenization
    words = word_tokenize(str(text))
    processed_words = []

    for word in words:
        if word.isdigit():
            processed_words.append(str(word))
        else:
            #Removing special characters
            word = word.strip(string.punctuation)
            lemmatizer = WordNetLemmatizer()
            word = lemmatizer.lemmatize(word)

            #remove stop words(σβήνω λέξεις χωρίς νόημα)
            stop_words = set(stopwords.words('english'))
            if word.lower() not in stop_words:
                processed_words.append(word.lower())

    return ' '.join(processed_words)

#process_content(text)

dataframe = pd.read_json(r'(\"articles.json\")')

for column in dataframe.columns:
    dataframe[column] = dataframe[column].apply(process_content)

new_columns = {0: 'Title', 1: 'Url', 2: 'Content'}

dataframe = dataframe.rename(columns = new_columns)

dataframe.to_json('processed.json', orient = 'records', lines = True)

print("Process complete")