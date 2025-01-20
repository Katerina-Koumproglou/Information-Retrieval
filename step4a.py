import json

def load_inverted_index(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

def boolean_search(query, inverted_index):
    terms = query.lower().split()
    if not terms:
        return None, "Το ερώτημα είναι κενό."

    if len(terms) % 2 == 0:
        return None, f"Λάθος: Λείπει όρος μετά τον τελεστή '{terms[-1]}'."

    result_set = set(inverted_index.get(terms[0], []))
    
    i = 1
    while i < len(terms):
        operator = terms[i]  #AND, OR, NOT
        
        next_term = terms[i + 1]
        next_docs = set(inverted_index.get(next_term, []))
        
        # Εκτέλεση της λειτουργίας
        if operator == "and":
            result_set = result_set.intersection(next_docs)
        elif operator == "or":
            result_set = result_set.union(next_docs)
        elif operator == "not":
            result_set = result_set.difference(next_docs)
        else:
            return None, f"Λάθος: Άγνωστος τελεστής '{operator}'."
        
        i += 2
    
    return result_set, None

def main():
    filepath = "inverted_index.json"  
    inverted_index = load_inverted_index(filepath)

    print("Καλωσήρθατε στη Μηχανή Αναζήτησης!")
    print("Πληκτρολογήστε το ερώτημά σας χρησιμοποιώντας Boolean τελεστές (AND, OR, NOT) ή 'exit' για έξοδο.")
    
    while True:
        query = input("\nΕρώτημα: ").strip()
        
        if query.lower() == "exit":
            print("Έξοδος από τη Μηχανή Αναζήτησης!")
            break
        
        results, error = boolean_search(query, inverted_index)
        
        if error:
            print(error)
        elif results:
            print(f"Αποτελέσματα για το ερώτημα '{query}': {results}")
        else:
            print(f"Δεν βρέθηκαν αποτελέσματα για το ερώτημα '{query}'.")


if __name__ == "__main__":
    main()
