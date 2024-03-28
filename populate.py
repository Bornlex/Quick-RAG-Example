import sys

from src import db, llm


cw = db.ClientWrapper()
documents = cw.search('')

counter = 1

for d in documents:
    processed_document = d
    string = f"Un contrat de type {d['nature']} concernant {d['objet']} dans le département de {d['lieuExecution']['nom']}."
    embeddings, exception = llm.LLM().get_embeddings(string)
    if not embeddings:
        print(d)
        print(exception)
        break
    cw.update_vector(processed_document['id'], embeddings)

    if counter % 10 == 0:
        sys.stdout.write('.')
        if counter % 100 == 0:
            sys.stdout.write(f'\n[{counter}]')

    counter += 1
