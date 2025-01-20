from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from rank_bm25 import BM25Okapi
import json
import numpy as np

# Συνάρτηση για τη φόρτωση εγγράφων από ένα αρχείο JSON
def load_documents(filepath):
    with open(filepath, "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        # Αν το JSON περιέχει λίστα, επιστρέφου με τα περιεχόμενα του πεδίου "content"
        if isinstance(data, list):
            return [doc["content"] for doc in data if "content" in doc]
        # Αν το JSON περιέχει λεξικό (π.χ. το ανεστραμμένο ευρετήριο), επιστρέφουμε το λεξικό
        elif isinstance(data, dict):
            return data
        # Αν δεν είναι καμία από τις δύο μορφές, εμφανίζεται μήνυμα λάθους
        else:
            raise ValueError("Το αρχείο δεν έχει υποστηριζόμενη μορφή.")

# Boolean Search για αναζήτηση εγγράφων με βάση Boolean λογική (AND, OR, NOT)
def boolean_search(query, inverted_index):
    terms = query.lower().split()  # Διαχωρισμός του ερωτήματος σε λέξεις
    if not terms:  # Αν το ερώτημα είναι κενό, επιστρέφουμε κενό σύνολο
        return set()

    # Ξεκινάμε με τα έγγραφα που περιέχουν την πρώτη λέξη
    result_set = set(inverted_index.get(terms[0], []))
    i = 1
    while i < len(terms):  # Επεξεργασία των υπόλοιπων λέξεων και τελεστών
        operator = terms[i]  # Παίρνουμε τον Boolean τελεστή (AND, OR, NOT)
        if i + 1 >= len(terms):  # Αν δεν υπάρχει άλλη λέξη μετά τον τελεστή, σταματάμε
            break
        next_term = terms[i + 1]  # Επόμενη λέξη
        next_docs = set(inverted_index.get(next_term, []))  # Έγγραφα που περιέχουν τη λέξη
        # Εκτέλεση της αντίστοιχης Boolean λειτουργίας
        if operator == "and":
            result_set = result_set.intersection(next_docs)
        elif operator == "or":
            result_set = result_set.union(next_docs)
        elif operator == "not":
            result_set = result_set.difference(next_docs)
        i += 2  # Προχωράμε στον επόμενο τελεστή/λέξη
    return result_set

# TF-IDF Ranking για κατάταξη εγγράφων με βάση τη σχετικότητα (TF-IDF score)
def tfidf_ranking(query, documents):
    vectorizer = TfidfVectorizer()  # Δημιουργία του TF-IDF Vectorizer
    doc_vectors = vectorizer.fit_transform(documents)  # Υπολογισμός TF-IDF για τα έγγραφα
    query_vector = vectorizer.transform([query.lower()])  # Μετατροπή του ερωτήματος σε διάνυσμα
    scores = cosine_similarity(query_vector, doc_vectors).flatten()  # Υπολογισμός cosine similarity
    sorted_indices = np.argsort(scores)[::-1]  # Ταξινόμηση των εγγράφων με βάση τη βαθμολογία
    # Επιστροφή μόνο των εγγράφων με βαθμολογία > 0
    return [(idx, scores[idx]) for idx in sorted_indices if scores[idx] > 0.0]

# BM25 Ranking για κατάταξη εγγράφων με βάση το BM25
def bm25_ranking(query, documents):
    tokenized_docs = [doc.split() for doc in documents]  # Διαχωρισμός των εγγράφων σε λέξεις
    bm25 = BM25Okapi(tokenized_docs)  # Δημιουργία BM25 μοντέλου
    tokenized_query = query.split()  # Διαχωρισμός του ερωτήματος σε λέξεις
    scores = bm25.get_scores(tokenized_query)  # Υπολογισμός BM25 scores
    sorted_indices = np.argsort(scores)[::-1]  # Ταξινόμηση των εγγράφων με βάση τη βαθμολογία
    # Επιστροφή των εγγράφων με βαθμολογίες
    return [(idx, scores[idx]) for idx in sorted_indices if scores[idx] > 0.0]

# Κύρια συνάρτηση για την εκτέλεση της μηχανής αναζήτησης
def main():
    # Αρχεία εισόδου
    filepath_docs = "articles.json"  # Αρχείο με τα έγγραφα
    filepath_index = "inverted_index.json"  # Αρχείο με το ανεστραμμένο ευρετήριο
    documents = load_documents(filepath_docs)  # Φόρτωση των εγγράφων
    inverted_index = load_documents(filepath_index)  # Φόρτωση του ανεστραμμένου ευρετηρίου

    # Εμφάνιση επιλογών στον χρήστη
    print("Επιλέξτε αλγόριθμο ανάκτησης:")
    print("1. Boolean Retrieval")
    print("2. TF-IDF Ranking")
    print("3. BM25 Ranking")
    print("Πληκτρολογήστε 'exit' για έξοδο.")

    while True:
        choice = input("\nΕπιλογή: ").strip()  # Είσοδος επιλογής από τον χρήστη
        if choice.lower() == "exit":  # Έξοδος από το πρόγραμμα
            print("Έξοδος από τη Μηχανή Αναζήτησης!")
            break

        query = input("Ερώτημα: ").strip()  # Είσοδος ερωτήματος
        if not query:  # Αν το ερώτημα είναι κενό
            print("Το ερώτημα δεν μπορεί να είναι κενό.")
            continue

        if choice == "1":  # Boolean Retrieval
            results = boolean_search(query, inverted_index)
            if results:
                print("\nBoolean Results:")
                for idx in results:
                    if idx < len(documents):  # Έλεγχος αν το έγγραφο υπάρχει
                        print(f"Έγγραφο {idx}")
                    else:
                        print(f"Το έγγραφο {idx} δεν υπάρχει στο articles.json.")
            else:
                print("Δεν βρέθηκαν αποτελέσματα.")

        elif choice == "2":  # TF-IDF Ranking
            results = tfidf_ranking(query, documents)
            print("\nTF-IDF Results:")
            for idx, score in results:
                if idx < len(documents):  # Έλεγχος αν το έγγραφο υπάρχει
                    print(f"Έγγραφο {idx} (Σκορ: {score:.4f})")
                else:
                    print(f"Το έγγραφο {idx} δεν υπάρχει στο articles.json.")

        elif choice == "3":  # BM25 Ranking
            results = bm25_ranking(query, documents)
            print("\nBM25 Results:")
            for idx, score in results:
                if idx < len(documents):  # Έλεγχος αν το έγγραφο υπάρχει
                    print(f"Έγγραφο {idx} (Σκορ: {score:.4f})")
                else:
                    print(f"Το έγγραφο {idx} δεν υπάρχει στο articles.json.")

        else:  # Μη έγκυρη επιλογή
            print("Μη έγκυρη επιλογή. Παρακαλώ προσπαθήστε ξανά.")

# Εκκίνηση προγράμματος
if __name__ == "__main__":
    main()
