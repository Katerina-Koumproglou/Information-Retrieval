# Information Retrieval System
This group project is an implementation of a simple search engine built entirely in Python. It starts by collecting real articles from Wikipedia, then cleans and processes the text using basic natural language processing (NLP) techniques like tokenization, lemmatization, and stop word removal.

Once the data is cleaned, the system builds an inverted index — basically a way to track which words appear in which articles — so it can search through the content efficiently.

From there, you can search the articles using Boolean retrieval (AND, OR, NOT queries), or try ranked search methods like TF-IDF or BM25, which sort the results based on how relevant they are to your query.

*You can read everything about the project while simultaneously running it using the jupyter file, which is in Greek.*

---

### Technologies Used
- Python 3

- BeautifulSoup for web scraping

- NLTK for NLP preprocessing

- pandas for data manipulation

- scikit-learn for TF-IDF vectorization

- rank-bm25 for BM25 implementation
  
---

### Project Structure
| <!-- -->    | <!-- -->    |
|-------------|-------------|
| step1.py     |            Scrapes Wikipedia articles and stores them in a JSON file|
| step2.py       |          Cleans and preprocesses article content|
| step3.py      |           Builds inverted index from processed data|
| step4a.py      |          CLI-based Boolean search over the inverted index|
| step4b.py       |         CLI-based ranked retrieval using TF-IDF and BM25|
| articles.json    |        Raw article data (scraped)|
| processed.json    |       Cleaned article data (tokenized, lemmatized, etc.)|
| inverted_index.json   |   Generated inverted index for search|
