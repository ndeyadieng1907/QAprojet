# import librairie
import json
from haystack import Pipeline, Document
from haystack.components.retrievers.in_memory import InMemoryBM25Retriever
from haystack.components.builders.prompt_builder import PromptBuilder
from haystack.document_stores.in_memory import InMemoryDocumentStore
from haystack import Document
from haystack.components.preprocessors import DocumentSplitter

## FONCTION QUI PERMET DE PREPARER LE CHARGEMENT DES RESUMES DES PUBLICATIONS 
def ingest_json(filename = "all_data_simple_dec_2023.json"):
    with open(filename,"r") as file :
        data  = json.load(file)

    mes_doc = []
    for item in data:
        if item["sommaire"] != None :
            doc = Document(
            content= item["sommaire"],
            meta={
                "name" : item["source"],
                "source" : "json",
                "indicateurs" : item["indicateurs"],
                "description" : item["description"]
                }
                )
            mes_doc.append(doc)

    print(f"taille json : {len(mes_doc)}")
    return mes_doc


## INITIALISATION DE LA BASE MEMOIRE POUR LA SAUVEGARDE DES DONN2ES

docstore = InMemoryDocumentStore()

### FONCION QUI PERMET DE DECOUPER LES TEXTES EN CHUNK CHACUN AVEC 200 MOTS VALEUR PAR DEFAUT
splitter = DocumentSplitter(split_by="word")

## RECUPERATION DES DONNEES DEPUIS LE FICHIER JSON
mes_doc = ingest_json()

## DECOUPAGE
mes_doc_split = splitter.run(mes_doc)

# INSTANCIATION DU DOCUMENT STORE EN MEMOIRE
document_store = InMemoryDocumentStore()

# CHARGEMENT DES DONNEES DANS LE IN MEMORY STORE

document_store.write_documents(mes_doc_split["documents"])

# PIPELINE POUR LA RECHERCHE D INFORMATION BASE SUR L ALGORITHME BEST MATCHING 25

pipe_simple = Pipeline()
pipe_simple.add_component("retriever", InMemoryBM25Retriever(document_store=document_store, top_k = 5))

## FONCTION QUI PREND UNE QUESTION, RECHERHCHE LES MEILLEURS "CHUNK" QUI POURRAIT CONTENIR LA REPONSE ET RENVOYER LES MEILLEIRS CONTENUES

def repondre(question):

    result = pipe_simple.run({
            "retriever": {"query": question}})

    answer = result["retriever"]["documents"][0].content
    relevant_documents = ""
    
    for i, doc in enumerate(result["retriever"]["documents"]):
        if doc.meta["name"] not in relevant_documents :
            relevant_documents+= f"publication {i+1} : {doc.meta['indicateurs']}, \n score : {doc.score} \n SOURCE :{doc.meta['name']}"
            relevant_documents+="\n\n"

    return answer, relevant_documents
if __name__ == "__main__" :
    question = "Quel est le pib du Sénégal en 2022?"
    print(repondre(question=question))
