# -*- coding: utf-8 -*-
"""DataExtractionNLP.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1XxBagfjmQ0Kd0JJzyMfN1GISs5n_OcB3

1. Import Libraries
"""

import pandas as pd
from textblob import TextBlob
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.probability import FreqDist

"""2. Download NLTK Resources"""

nltk.download('punkt')
nltk.download('stopwords')

"""3. Define Functions"""

def calculate_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity, blob.sentiment.subjectivity

def count_syllables(word):
    # Simple syllable count approx
    vowels = "aeiouy"
    word = word.lower()
    if word[0] in vowels:
        count += 1
    for index in range(1, len(word)):
        if word[index] in vowels and word[index - 1] not in vowels:
            count += 1
    if word.endswith("e"):
        count -= 1
    if count == 0:
        count += 1
    return count

def calculate_text_statistics(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Calculate text statistics
    avg_sentence_length = sum(len(sent.split()) for sent in sent_tokenize(text)) / len(sent_tokenize(text))
    total_words = len(words)
    complex_words = [word for word in words if len(word) > 6]  # Adjust the criteria for complex words
    percentage_complex_words = (len(complex_words) / total_words) * 100 if total_words > 0 else 0
    fog_index = 0.4 * (avg_sentence_length + percentage_complex_words)

    return avg_sentence_length, percentage_complex_words, fog_index, total_words / len(sent_tokenize(text)), len(complex_words), total_words

def calculate_personal_pronouns(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Define personal pronouns
    personal_pronouns = ['I', 'me', 'my', 'mine', 'myself', 'you', 'your', 'yours', 'yourself']

    # Count personal pronouns
    personal_pronoun_count = sum(word.lower() in personal_pronouns for word in words)

    return personal_pronoun_count

def calculate_avg_word_length(text):
    # Tokenize the text into words
    words = word_tokenize(text)

    # Calculate average word length
    avg_word_length = sum(len(word) for word in words) / len(words) if len(words) > 0 else 0

    return avg_word_length

"""4. Read Input Data"""

df = pd.read_excel('/content/Input.xlsx')

"""5. Apply Functions"""

df['POSITIVE SCORE'], df['NEGATIVE SCORE'] = zip(*df['URL'].apply(lambda x: calculate_sentiment(x)))
df['AVG SENTENCE LENGTH'], df['PERCENTAGE OF COMPLEX WORDS'], df['FOG INDEX'], df['AVG NUMBER OF WORDS PER SENTENCE'], df['COMPLEX WORD COUNT'], df['WORD COUNT'] = zip(*df['URL'].apply(lambda x: calculate_text_statistics(x)))
df['PERSONAL PRONOUNS'] = df['URL'].apply(lambda x: calculate_personal_pronouns(x))
df['AVG WORD LENGTH'] = df['URL'].apply(lambda x: calculate_avg_word_length(x))
df['POLARITY SCORE'], df['SUBJECTIVITY SCORE'] = zip(*df['URL'].apply(calculate_sentiment))
df['SYLLABLE PER WORD'] = df['URL_ID'].apply(lambda x: sum(count_syllables(word) for word in x.split()) / len(x.split()))

"""6. Save Output"""

df.to_excel('OutputDataStructure.xlsx', index=False)

# Download the file to your local machine
from google.colab import files
files.download('OutputDataStructure.xlsx')