import csv
from gtts import gTTS
import os

# Create a folder 'el' if it doesn't exist
output_folder_el = 'el'
if not os.path.exists(output_folder_el):
    os.makedirs(output_folder_el)

# Create a folder 'en' if it doesn't exist
output_folder_en = 'en'
if not os.path.exists(output_folder_en):
    os.makedirs(output_folder_en)

# Load the CSV file
csv_filename = 'greek-english.csv'  # Replace with your CSV file name
with open(csv_filename, 'r', encoding='utf-8') as csv_file:
    csv_reader = csv.reader(csv_file)
    
    # Skip the header if it exists
    next(csv_reader, None)
    
    for index, row in enumerate(csv_reader, start=1):
        if len(row) >= 2:  # Assuming Greek words are in the first column and English words in the second
            greek_word = row[0]
            english_word = row[1]
            
            # Define the audio file paths for Greek and English
            audio_filename_el = os.path.join(output_folder_el, f'{index}.mp3')
            audio_filename_en = os.path.join(output_folder_en, f'{index}.mp3')
            
            # Check if the audio file already exists for Greek word
            if not os.path.exists(audio_filename_el):
                # Create a gTTS object and generate the audio pronunciation for Greek word
                tts_el = gTTS(text=greek_word, lang='el')
                
                # Save the audio file in the 'el' folder
                tts_el.save(audio_filename_el)
                
                print(f'Saved Greek audio for word {greek_word} as {audio_filename_el}')
            else:
                print(f'Greek audio for word {greek_word} already exists as {audio_filename_el}')
            
            # Check if the audio file already exists for English word
            if not os.path.exists(audio_filename_en):
                # Create a gTTS object and generate the audio pronunciation for English word
                tts_en = gTTS(text=english_word, lang='en')
                
                # Save the audio file in the 'en' folder
                tts_en.save(audio_filename_en)
                
                print(f'Saved English audio for word {english_word} as {audio_filename_en}')
            else:
                print(f'English audio for word {english_word} already exists as {audio_filename_en}')
