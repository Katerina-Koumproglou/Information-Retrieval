import json

# Φόρτωση ανεστραμμένου ευρετηρίου
def load_inverted_index(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

# Boolean Search Function
def boolean_search(query, inverted_index):
    # Διαχωρισμός όρων και τελεστών
    terms = query.lower().split()  # Διαχωρισμός βάσει κενού
    if not terms:
        return set()  # Επιστρέφει άδειο σύνολο αν το ερώτημα είναι κενό

    result_set = set(inverted_index.get(terms[0], []))  # Ξεκινάμε με τον πρώτο όρο
    
    i = 1
    while i < len(terms):
        operator = terms[i]  # AND, OR, NOT
        
        # Επαλήθευση αν υπάρχει ο επόμενος όρος
        if i + 1 >= len(terms):
            print(f"Λάθος: Λείπει όρος μετά τον τελεστή '{operator}'")
            break
        
        next_term = terms[i + 1]
        next_docs = set(inverted_index.get(next_term, []))  # Έγγραφα για τον επόμενο όρο
        
        # Εκτέλεση της λειτουργίας
        if operator == "and":
            result_set = result_set.intersection(next_docs)
        elif operator == "or":
            result_set = result_set.union(next_docs)
        elif operator == "not":
            result_set = result_set.difference(next_docs)
        else:
            print(f"Λάθος: Άγνωστος τελεστής '{operator}'")
            break
        
        i += 2  # Επόμενος τελεστής ή όρος
    
    return result_set

# main Συνάρτηση
def main():
    # Φόρτωσε το ανεστραμμένο ευρετήριο
    filepath = "inverted_index.json"  
    inverted_index = load_inverted_index(filepath)

    print("Καλωσήρθατε στη Μηχανή Αναζήτησης!")
    print("Πληκτρολογήστε το ερώτημά σας χρησιμοποιώντας Boolean τελεστές (AND, OR, NOT) ή 'exit' για έξοδο.")
    
    while True:
        # Εισαγωγή ερωτήμ,ατος από τον χρήστη
        query = input("\nΕρώτημα: ").strip()
        
        # Έξοδος αν ο χρήστης πληκτρολογήσει "exit"
        if query.lower() == "exit":
            print("Έξοδος από τη Μηχανή Αναζήτησης!")
            break
        
        # Εκτέλεση Boolean Search
        results = boolean_search(query, inverted_index)
        
        # Εμφάνιση αποτελεσμάτων
        if results:
            print(f"Αποτελέσματα για το ερώτημα '{query}': {results}")
        else:
            print(f"Δεν βρέθηκαν αποτελέσματα για το ερώτημα '{query}'.")


if __name__ == "__main__":
    main()