import json
from collections import defaultdict

# Διαβάζω τα επεξεργασμένα δεδομένα από το αρχείο processed.json
with open('processed.json', 'r') as json_file:
    documents = json.load(json_file)  # Φορτώνουμε το JSON σε μορφή λίστας/λεξικού

# Αντίστροφο ευρετήριο (inverted index)
inverted_index = defaultdict(lambda: [0] * len(documents))  # Δημιουργία λίστας με μηδενικά για κάθε έγγραφο

# Επεξεργασία κάθε έγγραφου
for doc_id, document in enumerate(documents):
    # Σπλιτάρω και αποθηκεύω στο terms όλα τα κομμάτια
    for field, field_value in document.items():
        if isinstance(field_value, str):  # Ελέγχω αν το πεδίο είναι string
            terms = field_value.split()  # Χωρίζω το κείμενο σε όρους
            
            # Δημιουργία του αντεστραμμένου ευρετηρίου μετρώντας τις εμφανίσεις κάθε λέξης
            for term in terms:
                inverted_index[term][doc_id] += 1  # Αυξάνουμε την εμφάνιση του όρου στο έγγραφο

# Αποθήκευση του αντεστραμμένου ευρετηρίου σε ένα αρχείο JSON
with open('inverted_index.json', 'w') as json_file:
    json.dump(inverted_index, json_file, indent=4)  # Προσθέτουμε το indent για καλύτερη αναγνωσιμότητα

# Δοκιμαστική εκτύπωση μερικών όρων
print("The inverted index has been saved:")
for term, occurrences in list(inverted_index.items())[:10]:
    print(f"{term}: {occurrences}")
