import json
import math
from collections import Counter

def user_interface():
    print("Καλώς ήρθατε στην μηχανή αναζήτησης ακαδημαϊκών εργασιών!")

    while True:
        query = input("Εισαγάγετε το ερώτημά σας ή γράψτε exit για έξοδο: ").strip().lower()

        if query == 'exit':
            print("Ευχαριστούμε που χρησιμοποιήσατε τη μηχανη αναζήτησης μας.")
            break

        algorithm_choice = input("Επιλέξτε αλγόριθμο ανάκτησης:\n1) Boolean Retrieval\n2) Vector Space Model (VSM)\n3) Probabilistic Retrieval Models(OKAPI BM25)\nΕπιλογή: ").strip()

        if algorithm_choice == '1':
            boolean_retrieval(query)
            break
        elif algorithm_choice == '2':
            vector_space_model(query)
            break
        elif algorithm_choice == '3':
            probabilistic_retrieval(query)
            break
        else:
            print("Μη έγκυρη επιλογή αλγορίθμου. Παρακαλώ εισάγετε έναν έγκυρο αριθμό.")

#φορτώνω τα στοιχεία του inverted_index.json 
def load_inverted_index(file_path='inverted_index.json'):
    try:
        with open(file_path, 'r') as json_file:
            inverted_index = json.load(json_file)
        return inverted_index
    except FileNotFoundError:
        print(f"Το αρχείο {file_path} δεν βρέθηκε.")
        return None
            
#Η συνάρτηση απλά ελέγχει το ανεστραμμένο ευρετήριο για κάθε όρο του ερωτήματος και
#συγκεντρώνει τα έγγραφα που περιέχουν τους όρους με τη χρήση των λογικών τελεστών
# AND, OR και NOT.
#!!ειναι ένωση των αποτελεσμάτων και όχι τομή
def boolean_retrieval(query):
    inverted_index = load_inverted_index()

    if inverted_index is None:
        print("Η λειτουργία Boolean Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return

    terms = query.split()
    print(f"Εκτέλεση Boolean Retrieval για το ερώτημα: {terms}")

    result = set()

    for term in terms:
        if term.lower() in inverted_index:
            result.update(inverted_index[term.lower()])

    print(f"Αποτελέσματα Boolean Retrieval: {result}")
    
#Στο Vector Space Model (VSM), κάθε έγγραφο και το ερώτημα αναπαρίστανται σαν σύνολα λέξεων.
#Για κάθε λέξη, υπολογίζουμε ένα βάρος (TF-IDF) που δείχνει πόσο σημαντική είναι σε κάθε έγγραφο.
#
#Το TF-IDF (Term Frequency-Inverse Document Frequency) λειτουργεί ως εξής:
#Term Frequency (TF): Μετράει πόσες φορές εμφανίζεται μια λέξη σε ένα έγγραφο.
#
#Inverse Document Frequency (IDF): Υπολογίζει πόσο σπάνια είναι μια λέξη σε όλα τα έγγραφα.
#Το TF-IDF βοηθά στο να δώσουμε υψηλό βάρος σε λέξεις που είναι σημαντικές για ένα συγκεκριμένο
#έγγραφο, αλλά σπάνιες σε όλα τα έγγραφα.
#
#Έπειτα, υπολογίζουμε την ομοιότητα (cosine similarity) μεταξύ του ερωτήματος και κάθε έγγραφου.
# Η cosine similarity μετράει τη γωνία μεταξύ των διανυσμάτων του ερωτήματος και του έγγραφου στο
#χώρο χαρακτηριστικών. Αν η γωνία είναι μικρή, η ομοιότητα είναι υψηλή, προτείνοντας ότι το 
#έγγραφο είναι σχετικό με το ερώτημα.
#
#!!Αν δώσω περισσότερα από ένα tokens, το VSM θα αξιοποιήσει όλα τα δοσμένα tokens για να
#υπολογίσει την ομοιότητα.(ένωση παλι)
def vector_space_model(query):
    inverted_index = load_inverted_index()

    if inverted_index is None:
        print("Η λειτουργία Vector Space Model δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return

    terms = query.split()
    print(f"Εκτέλεση Vector Space Model για το ερώτημα: {terms}")

    document_vectors = {}
    query_vector = Counter(terms)

    for term, query_term_freq in query_vector.items():
        lower_term = term.lower()
        if lower_term in inverted_index:
            idf = math.log10(len(inverted_index) / len(inverted_index[lower_term]))

            for doc_id in inverted_index[lower_term]:
                doc_term_freq = inverted_index[lower_term].count(doc_id)
                tf_idf = doc_term_freq * idf

                if doc_id in document_vectors:
                    document_vectors[doc_id] += tf_idf * query_term_freq
                else:
                    document_vectors[doc_id] = tf_idf * query_term_freq

    # Ταξινόμηση των εγγράφων βάσει του cosine similarity
    ranked_documents = sorted(document_vectors.items(), key=lambda x: x[1], reverse=True)

    print(f"Αποτελέσματα Vector Space Model: {ranked_documents}")

#Στον Probabilistic Retrieval, κάθε έγγραφο χαρακτηρίζεται από τη πιθανότητα να ανταποκριθεί σε ένα ερώτημα.
#Η πιθανότητα αυτή υπολογίζεται με βάση την πιθανότητα εμφάνισης των όρων του ερωτήματος στο έγγραφο.


def probabilistic_retrieval(query):
    inverted_index = load_inverted_index()

    if inverted_index is None:
        print("Η λειτουργία Probabilistic Retrieval δεν είναι δυνατή λόγω απουσίας αρχείου inverted_index.json.")
        return

    # Constants
    k1 = 1.5
    b = 0.75
    N = len(inverted_index)  # Total number of documents
    avgdl = sum(len(doc) for doc in inverted_index.values()) / N  # Average document length

    terms = query.split()
    scores = {}

    for doc_id, doc_terms in inverted_index.items():
        # Initialize BM25 score for the document
        score = 0

        # Compute document-specific parameters
        doc_length = len(doc_terms)

        for term in terms:
            # Term frequency in the document
            ft = doc_terms.count(term)

            # Document frequency of the term
            df = sum(1 for doc in inverted_index.values() if term in doc)
          
            # Inverse Document Frequency (IDF)
            idf = math.log((N - df + 0.5) / (df + 0.5))

            # Term frequency normalization
            tf = ft * (k1 + 1) / (ft + k1 * (1 - b + b * (doc_length / avgdl)))

            # BM25 score for the term in the document
            score += idf * tf

        # Update document score
        scores[doc_id] = score

    # Sort documents by score in descending order
    ranked_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)

    print(f"Αποτελέσματα Probabilistic Retrieval για το ερώτημα '{query}': {ranked_documents}")


# Κώδικας για χρήση της συνάρτησης:
# probabilistic_retrieval("your_query_here")




if __name__ == "__main__":
    user_interface()
