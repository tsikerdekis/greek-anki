import genanki
import csv
import os

# Define a unique model ID
model_id = 1607392319

# Define the Anki model for your deck
my_model = genanki.Model(
    model_id,
    'Greek to English',
    fields=[
        {'name': 'Greek'},
        {'name': 'English'},
        {'name': 'Pronunciation'},  # Add this field for audio
        {'name': 'Sentence'},  # Add this field for the sentence
    ],
    templates=[
        {
            'name': 'Card 1',
            'qfmt': '{{Greek}}<br />{{Pronunciation}}',
            'afmt': '{{FrontSide}}<hr id="answer"><div class="centered-text"><b>English:</b> {{English}}<br><br><b>Sentence:</b> {{Sentence}}</div>',
        },
    ])

# Define a unique deck ID
deck_id = 2059400110

# Define the Anki deck
my_deck = genanki.Deck(
    deck_id,
    'Greek Vocabulary')

# Create a list to store the media files (audio)
media_files = []

# Read data from the CSV file and add notes to the deck, skipping the first line
with open('greek-english.csv', newline='', encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile)
    next(reader)  # Skip the first line (titles)
    for index, row in enumerate(reader):  # Start index at 0
        greek_word, english_word, sentence = row  # Add sentence
        audio_index = index + 1  # Adjust index to start from 1 for audio files
        pronunciation_file = f'[sound:{audio_index}.mp3]'  # Format pronunciation field
        # Bold the Greek word in the sentence using HTML formatting
        sentence_with_bold = sentence.replace(greek_word, f'<b>{greek_word}</b>')
        my_note = genanki.Note(
            model=my_model,
            fields=[greek_word, english_word, pronunciation_file, sentence_with_bold],  # Include sentence
        )

        my_deck.add_note(my_note)

        # Add each audio file to the media_files list
        audio_file_path = os.path.join('el', f'{audio_index}.mp3')
        media_files.append(audio_file_path)

# Package the deck and write it to an .apkg file
my_package = genanki.Package(my_deck)
my_package.media_files = media_files  # Specify individual audio files
my_package.write_to_file('output.apkg')
