import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, WordNetLemmatizer
import string

# Κατέβασμα απαραίτητων πόρων
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')

# Συνάρτηση για επεξεργασία κειμένου
def process_content(text):
    if not isinstance(text, str):  # Έλεγχος ότι η είσοδος είναι string
        return text
    
    # Tokenization
    words = word_tokenize(text)
    processed_words = []
    
    for word in words:
        if word.isdigit():  # Αν είναι αριθμός, το προσθέτουμε απευθείας
            processed_words.append(word)
        else:
            # Αφαίρεση ειδικών χαρακτήρων
            word = word.strip(string.punctuation)
            
            # Lemmatization
            lemmatizer = WordNetLemmatizer()
            word = lemmatizer.lemmatize(word)
            
            # Αφαίρεση stop words
            stop_words = set(stopwords.words('english'))
            if word.lower() not in stop_words:
                processed_words.append(word.lower())
    
    return ' '.join(processed_words)

# Ανάγνωση δεδομένων από αρχείο JSON
try:
    dataframe = pd.read_json("articles.json")  # Σωστή διαδρομή αρχείου
except Exception as e:
    print(f"Error reading JSON file: {e}")
    exit()

# Επεξεργασία δεδομένων DataFrame
for column in dataframe.columns:
    dataframe[column] = dataframe[column].apply(process_content)

# Μετονομασία στηλών
new_columns = {
    dataframe.columns[0]: 'Title',
    dataframe.columns[1]: 'Url',
    dataframe.columns[2]: 'Content'
}
dataframe = dataframe.rename(columns=new_columns)

# Αποθήκευση επεξεργασμένων δεδομένων σε νέο αρχείο JSON
dataframe.to_json("processed.json", orient='records', indent=4)

print("Process complete. Processed data saved to 'processed.json'.")
