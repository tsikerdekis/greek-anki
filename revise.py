import csv
import spacy

# Load the Greek language model
nlp = spacy.load("el_core_news_lg")

# Define a custom CSV dialect to ignore "!" and quotes as delimiters
csv.register_dialect('custom', delimiter='\t', quotechar='"', quoting=csv.QUOTE_NONE, escapechar='\\')

# Function to derive forms of a Greek adjective
def derive_adjective_forms(word):
    doc = nlp(word)
    adjective_forms = []

    for token in doc:
        if token.pos_ == "ADJ":
            if token.text.endswith("ος"):
                # Adjective with 2-character ending, e.g., "τρελός"
                stem = token.text[:-2]  # Remove the ending "ος"
                masculine_form = stem + "ος"
                feminine_form = stem + "η"
                neuter_form = stem + "ο"
                adjective_forms = "%s, %s, %s" % (masculine_form, feminine_form, neuter_form)
            elif token.text.endswith("η"):
                # Adjective with 1-character ending "η," e.g., "τρελή"
                stem = token.text[:-1]  # Remove the ending "η"
                masculine_form = stem + "ος"
                feminine_form = stem + "η"
                neuter_form = stem + "ο"
                adjective_forms = "%s, %s, %s" % (masculine_form, feminine_form, neuter_form)
            elif token.text.endswith("ο"):
                # Adjective with 1-character ending "ο," e.g., "τρελό"
                stem = token.text[:-1]  # Remove the ending "ο"
                masculine_form = stem + "ος"
                feminine_form = stem + "η"
                neuter_form = stem + "ο"
                adjective_forms = "%s, %s, %s" % (masculine_form, feminine_form, neuter_form)

    return adjective_forms

# Function to check if a word is a Greek verb and get its infinitive form
def get_verb_infinitive(word):
    doc = nlp(word)
    for token in doc:
        if token.pos_ == "VERB":
            # Use spaCy's lemma_ attribute to get the lemma (infinitive form) of the verb
            infinitive_form = token.lemma_
            return infinitive_form
    return None

# Function to check if a word is a Greek noun, get its nominative form, and add the definite article heuristically
def get_noun_nominative_with_article(word):
    doc = nlp(word)
    for token in doc:
        if token.pos_ == "NOUN":
            # Use the lemma (base form) of the noun as its nominative form
            nominative_form = token.lemma_
            
            # Heuristically determine the appropriate definite article based on the noun's ending
            if nominative_form.endswith("η"):
                article = "η"
            elif nominative_form.endswith("ος"):
                article = "ο"
            elif nominative_form.endswith("ο"):
                article = "το"
            elif nominative_form.endswith("α"):
                article = "η"
            elif nominative_form.endswith("ι"):
                article = "το"
            else:
                article = ""  # Default to empty if ending not recognized
            
            noun_with_article = article + " " + nominative_form
            return noun_with_article
    return None

# Function to process and translate a list of Greek words
def process_and_translate_words(word_list):
    translated_words = []

    total_words = len(word_list)
    processed_words = 0

    for word_to_check in word_list:
        word_to_check = word_to_check.strip().lower()  # Convert to lowercase and strip whitespace
        print(f"Processing word {processed_words + 1}/{total_words}: {word_to_check}")
        
        adjective_forms = derive_adjective_forms(word_to_check)
        verb_infinitive = get_verb_infinitive(word_to_check)
        noun_nominative_with_article = get_noun_nominative_with_article(word_to_check)
        
        if adjective_forms:
            translated_words.append(adjective_forms)
        elif verb_infinitive:
            translated_words.append(verb_infinitive)
        elif noun_nominative_with_article:
            translated_words.append(noun_nominative_with_article)
        else:
            translated_words.append(word_to_check)
        
        processed_words += 1

    return translated_words

# Read words from the CSV file, filter out non-Greek words, and store them in a list
greek_words = []

with open("ell_wikipedia_2021_10K-words.txt", "r", encoding="utf-8", newline="") as csv_file:
    csv_reader = csv.reader(csv_file, dialect='custom')
    for row in csv_reader:
        if len(row) >= 2:  # Check if there are at least two columns in the row
            word = row[1].strip()  # Assuming the words are in the second column
            # Check if the word contains Greek characters or symbols
            if any('\u0391' <= char <= '\u03C9' for char in word):
                greek_words.append(word)

print(f"Total Greek words read: {len(greek_words)}")

# Process the Greek words while preserving the original order
translated_words = process_and_translate_words(greek_words)

print(f"Total translated words: {len(translated_words)}")

# Eliminate duplicates while preserving the order
translated_words = list(dict.fromkeys(translated_words))

# Write the translated words to a new CSV file without duplicates, in lowercase and stripped
with open("translated_greek_words.csv", "w", newline="", encoding="utf-8") as csv_file:
    csv_writer = csv.writer(csv_file)
    for word in translated_words:
        csv_writer.writerow([word.lower().strip()])  # Convert to lowercase and strip whitespace

print("Processing completed. Translated words without duplicates have been saved to 'translated_greek_words.csv'.")
