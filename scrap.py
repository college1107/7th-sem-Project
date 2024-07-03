import spacy
import requests
from bs4 import BeautifulSoup

nlp = spacy.load("en_core_web_lg")

def extract_entities(text):
    doc = nlp(text)
    entities = []
    
    print("Entities found:")
    for ent in doc.ents:
        ent = ent.lemma_
        print(f"{ent.text}: {ent.label_} ({spacy.explain(ent.label_)})")
        if ent.label_ == "PERSON":
            entities.append(ent.text)
        elif ent.label_ in ["NORP", "ORG", "GPE", "LOC", "PRODUCT"]:
            # Additional entity types you might be interested in
            entities.append(ent.text.lower())  # Store in lowercase for URLs
    for token in doc:
        if token.pos_ in ["NOUN", "PROPN"] and token.text.lower() not in entities:
            entities.append(token.text.lower())  # Store nouns and proper nouns in lowercase for URLs
    if not entities:
        print("No relevant entities found.")
    print(entities)
    return entities

def construct_wikipedia_url(entity):
    base_url = "https://en.wikipedia.org/wiki/"
    return base_url + entity.replace(" ", "_")

def scrape_wikipedia_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        content = soup.find(id="mw-content-text").get_text()
        return content
    return None

def extract_relevant_sections(content, num_paragraphs=2):
    paragraphs = content.split("\n\n")
    return paragraphs

# Example input
input_text = "What are neural networks?"
try:
    entities = extract_entities(input_text)
    all_content = {}

    # Construct URLs and scrape content for each entity
    for entity in entities:
        url = construct_wikipedia_url(entity)
        entity_content = scrape_wikipedia_page(url)
        if entity_content:
            all_content[entity] = extract_relevant_sections(entity_content)
        else:
            all_content[entity] = f"No information found for {entity}"

    # Print all relevant information
    for entity, content in all_content.items():
        print(f"Entity: {entity}\nContent:\n{content}\n")
except ValueError as e:
    print(e)
