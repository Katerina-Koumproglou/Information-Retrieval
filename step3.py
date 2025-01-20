import json
from collections import defaultdict

with open('processed.json', 'r') as json_file:
    documents = json.load(json_file)

inverted_index = defaultdict(list)

for doc_id, document in enumerate(documents):
    for field, field_value in document.items():
        if isinstance(field_value, str):
            terms = field_value.split()
            
            for term in terms:
                if doc_id not in inverted_index[term]:
                    inverted_index[term].append(doc_id)

with open('inverted_index.json', 'w') as json_file:
    json.dump(inverted_index, json_file, indent=4)

print("The data has been saved to \"inverted_index.json\"")