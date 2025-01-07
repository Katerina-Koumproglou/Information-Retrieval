import json
from collections import defaultdict

# Διαβάζουμε τα επεξεργασμένα δεδομένα από το αρχείο processed.json
with open('processed.json', 'r') as json_file:
    documents = json.load(json_file)  # Φορτώνουμε το JSON σε μορφή λίστας/λεξικού

# Αντίστροφο ευρετήριο (inverted index)
inverted_index = defaultdict(list)  # Χρησιμοποιούμε defaultdict για να αποθηκεύσουμε τα IDs των εγγράφων

# Επεξεργασία κάθε έγγραφου
for doc_id, document in enumerate(documents):
    # Σπλιτάρω και αποθηκεύω στο terms όλα τα κομμάτια
    for field, field_value in document.items():
        if isinstance(field_value, str):  # Ελέγχω αν το πεδίο είναι string
            terms = field_value.split()  # Χωρίζω το κείμενο σε όρους
            
            # Δημιουργία του αντεστραμμένου ευρετηρίου (αντί για αριθμό εμφανίσεων, αποθηκεύουμε τα doc_id)
            for term in terms:
                if doc_id not in inverted_index[term]:  # Ελέγχουμε αν το doc_id είναι ήδη στη λίστα
                    inverted_index[term].append(doc_id)

# Αποθήκευση του αντεστραμμένου ευρετηρίου σε αρχείο JSON
with open('inverted_index.json', 'w') as json_file:
    json.dump(inverted_index, json_file, indent=4)  


print("The data has been saved to \"inverted_index.json\"")

