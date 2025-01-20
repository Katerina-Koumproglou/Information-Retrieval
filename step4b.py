from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import json
import numpy as np

def load_documents(filepath):
    with open(filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        if isinstance(data, list):
            return [doc["content"] for doc in data if "content" in doc]
        elif isinstance(data, dict):
            return data
        else:
            raise ValueError("Το αρχείο δεν έχει υποστηριζόμενη μορφή.")

#Boolean Search
def boolean_search(query, inverted_index):
    terms = query.lower().split()
    if not terms:
        return set()

    result_set = set(inverted_index.get(terms[0], []))
    i = 1
    while i < len(terms):
        operator = terms[i]
        if i + 1 >= len(terms):
            break
        next_term = terms[i + 1]
        next_docs = set(inverted_index.get(next_term, []))
        if operator == "and":
            result_set = result_set.intersection(next_docs)
        elif operator == "or":
            result_set = result_set.union(next_docs)
        elif operator == "not":
            result_set = result_set.difference(next_docs)
        i += 2
    return result_set

#TF-IDF Ranking
def tfidf_ranking(query, documents):
    vectorizer = TfidfVectorizer()
    doc_vectors = vectorizer.fit_transform(documents)
    query_vector = vectorizer.transform([query.lower()])
    scores = cosine_similarity(query_vector, doc_vectors).flatten()
    sorted_indices = np.argsort(scores)[::-1]
    return [(idx, scores[idx]) for idx in sorted_indices if scores[idx] > 0.0]

#BM25 Ranking
def bm25_ranking(query, documents):
    tokenized_docs = [doc.split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = query.split()
    scores = bm25.get_scores(tokenized_query)
    sorted_indices = np.argsort(scores)[::-1]
    return [(idx, scores[idx]) for idx in sorted_indices if scores[idx] > 0.0]


def main():
    filepath_docs = "articles.json"
    filepath_index = "inverted_index.json"
    documents = load_documents(filepath_docs)
    inverted_index = load_documents(filepath_index)

    print("Επιλέξτε αλγόριθμο ανάκτησης:")
    print("1. Boolean Retrieval")
    print("2. TF-IDF Ranking")
    print("3. BM25 Ranking")
    print("Πληκτρολογήστε 'exit' για έξοδο.")

    while True:
        choice = input("\nΕπιλογή: ").strip()
        if choice.lower() == "exit":
            print("Έξοδος από τη Μηχανή Αναζήτησης!")
            break

        query = input("Ερώτημα: ").strip()
        if not query:
            print("Το ερώτημα δεν μπορεί να είναι κενό.")
            continue

        if choice == "1":   #Boolean Retrieval
            results = boolean_search(query, inverted_index)
            if results:
                print("\nBoolean Results:")
                for idx in results:
                    if idx < len(documents):
                        print(f"Έγγραφο {idx}")
                    else:
                        print(f"Το έγγραφο {idx} δεν υπάρχει στο articles.json.")
            else:
                print("Δεν βρέθηκαν αποτελέσματα.")

        elif choice == "2":  #TF-IDF Ranking
            results = tfidf_ranking(query, documents)
            print("\nTF-IDF Results:")
            for idx, score in results:
                if idx < len(documents):
                    print(f"Έγγραφο {idx} (Σκορ: {score:.4f})")
                else:
                    print(f"Το έγγραφο {idx} δεν υπάρχει στο articles.json.")

        elif choice == "3":  #BM25 Ranking
            results = bm25_ranking(query, documents)
            print("\nBM25 Results:")
            for idx, score in results:
                if idx < len(documents):
                    print(f"Έγγραφο {idx} (Σκορ: {score:.4f})")
                else:
                    print(f"Το έγγραφο {idx} δεν υπάρχει στο articles.json.")

        else:
            print("Μη έγκυρη επιλογή. Παρακαλώ προσπαθήστε ξανά.")

if __name__ == "__main__":
    main()
