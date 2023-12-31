import csv
import nltk
from nltk.corpus import stopwords
import re
from googletrans import Translator
import time
import pickle
import atexit
import difflib

# Initialize an empty list to store the filtered words and their translations
filtered_words_with_translations = []

# Download the NLTK Greek stopwords if you haven't already
nltk.download('stopwords')

# Define a list of Greek stopwords, including articles (ο, η, το)
greek_stopwords = stopwords.words('greek') + ['ο', 'η', 'το']

# Define a regular expression pattern to match Greek characters
greek_pattern = re.compile('[Α-Ωα-ωίϊΐόάέύϋΰήώ]')

# Initialize a translator object
translator = Translator()

# Open the CSV file for reading
file_path = "ell_wikipedia_2021_10K-words.txt"

# Initialize a list to collect filtered words
filtered_words = []

# Function to save translations to a CSV file
def save_translations_to_csv():
    csv_file_path = "greek-english.csv"
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(["Greek Word", "English Translation", "Similar", "Example Sentence"])
        for word_info in filtered_words_with_translations:
            csv_writer.writerow([word_info["Greek Word"], word_info["English Translation"],
                                 word_info["Similar"], word_info["Example Sentence"]])
    print(f"Translations saved to '{csv_file_path}'")

# Register the function to save translations on exit
atexit.register(save_translations_to_csv)

# Load sentences from the example sentences file (get only the second column)
sentences_file_path = "ell_wikipedia_2021_10K-sentences.txt"
sentences = []
try:
    with open(sentences_file_path, 'r', encoding='utf-8') as sentences_file:
        sentences = [line.strip().split('\t')[1] for line in sentences_file.readlines()]
except FileNotFoundError:
    print(f"File '{sentences_file_path}' not found.")
except Exception as e:
    print(f"An error occurred while reading sentences: {str(e)}")

# Function to calculate string similarity between two words using SequenceMatcher
def string_similarity(word1, word2):
    return difflib.SequenceMatcher(None, word1, word2).ratio()

try:
    with open(file_path, 'r', encoding='utf-8') as csv_file:
        # Read each line from the file
        for i, line in enumerate(csv_file):
            # Split each line into columns using tabs as the delimiter
            columns = line.strip().split('\t')
            
            # Ensure there are three columns in each row
            if len(columns) == 3:
                # Get the second column (word)
                word = columns[1]
                
                # Tokenize the word using whitespace as the delimiter
                tokens = word.split()
                
                # Remove stopwords and symbols
                filtered_tokens = [token for token in tokens if token not in greek_stopwords and token.isalnum()]
                
                # Join the remaining tokens to form the cleaned word
                cleaned_word = ' '.join(filtered_tokens)
                
                # Check if the cleaned word contains only Greek characters and lowercase it
                if cleaned_word and all(greek_pattern.match(char) for char in cleaned_word):
                    filtered_words.append(cleaned_word.lower())

    # Calculate string similarity using a threshold
    similarity_threshold = 0.8  # Adjust the similarity threshold as needed

    # Initialize counters for translations
    total_translations = 0
    max_translations = 15000  # Set the maximum number of translations

    # Load translations from a pickle file if it exists
    translations_file_path = "translations.pkl"
    if translations_file_path:
        try:
            with open(translations_file_path, "rb") as translations_file:
                filtered_words_with_translations = pickle.load(translations_file)
        except FileNotFoundError:
            pass

    # Function to check if a word is similar to any existing word using string similarity
    def is_similar_to_existing(word, existing_words, threshold):
        most_similar_word = None
        most_similarity = threshold  # Initialize with the threshold
        for existing_word_info in existing_words:
            existing_word = existing_word_info["Greek Word"]
            result = string_similarity(word, existing_word)
            if result > most_similarity:
                most_similarity = result
                most_similar_word = existing_word
        return most_similar_word if most_similarity < 1.0 else None

    # Iterate through the filtered words and add them to the final list
    for word in filtered_words:
        # Check if the word is similar to any word already in the list
        most_similar = is_similar_to_existing(word, filtered_words_with_translations, similarity_threshold)
        
        # Translate the word (for testing, translate only a limited number of words)
        if total_translations < max_translations:
            total_translations += 1
            print(f"Translating ({total_translations}/{len(filtered_words)}): {word}")
            # Check if the translation exists in the saved translations
            for saved_word_info in filtered_words_with_translations:
                if saved_word_info["Greek Word"] == word:
                    word_info = saved_word_info
                    print(f"Using saved translation: {word} -> {word_info['English Translation']}")
                    break
            else:
                # Search for the word in example sentences and add the first match as the example sentence
                for sentence in sentences:
                    if word in sentence:
                        example_sentence = sentence
                        break
                else:
                    example_sentence = ""  # No example sentence found
                translation = translator.translate(word, src='el', dest='en').text
                word_info = {
                    "Greek Word": word,
                    "English Translation": translation,
                    "Similar": most_similar,
                    "Example Sentence": example_sentence
                }
                filtered_words_with_translations.append(word_info)
                time.sleep(3)  # Sleep for 3 seconds between translations
                print(f"Translated: {word} -> {translation}")
                # Save the translations to a pickle file
                with open(translations_file_path, "wb") as translations_file:
                    pickle.dump(filtered_words_with_translations, translations_file)
        else:
            break  # Stop after translating the specified number of words

except KeyboardInterrupt:
    print("Interrupt detected. Saving translations to CSV...")
    save_translations_to_csv()
except FileNotFoundError:
    print(f"File '{file_path}' not found.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

# Print the filtered Greek words with translations and example sentences
print("Filtered Greek words with translations and example sentences:")
for word_info in filtered_words_with_translations:
    print(f"Greek Word: {word_info['Greek Word']}, English Translation: {word_info['English Translation']}, Similar: {word_info['Similar']}, Example Sentence: {word_info['Example Sentence']}")
save_translations_to_csv()
