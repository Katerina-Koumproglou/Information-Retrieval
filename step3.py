import json

#διαβάζω τα επεξεργασμένα δεδομένα από το αρχείο processed.json
with open('processed_articles.json', 'r') as file:
    documents = file.readlines()

#λίστα που θα περιέχει όλους τους όρους για όλα τα έγγραφα
all_terms = []

#αντίστροφο ευρετήριο
inverted_index = {}

#επεξεργασία κάθε έγγραφου
for doc_id, document in enumerate(documents):
    json_data = json.loads(document)
    
    #σπλιταρω και αποθηκευω στο terms μονο τα κομματια περιληψεων
    #terms = json_data.get('Abstract', "").split()
    #αποθηκευω στο terms όλα τα κομμάτια
    for field, field_value in json_data.items():
       if isinstance(field_value, str):  #ελέγχω αν το πεδίο είναι string
           terms = field_value.split()
           all_terms.extend(terms)  #προσθήκη όρων στη λίστα για όλα τα έγγραφα
    
           #δημιουργία του ανεστραμμένου ευρετηρίου
           for term in terms:
            if term in inverted_index:
             inverted_index[term].append(doc_id)
            else:
             inverted_index[term] = [doc_id]

#αποθήκευση του ανεστραμμένου ευρετηρίου σε ένα αρχείο, π.χ., inverted_index.json
with open('inverted_index.json', 'w') as json_file:
    json.dump(inverted_index, json_file)

#δοκιμαστικη εκτύπωση μερικων όρων
print(all_terms[:10])