#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Jay Saraf 2020438
import os
import re
import json
import nltk
import pickle
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess_file(input_path, output_path):
    with open(input_path, 'r') as input_file:
        # Specifying file number for printing
        file_no = int(input_path.split("/")[-1].split(".")[0][4:])
        
        content = input_file.read()

        # Lower casing the content
        content = content.lower()
        if 1 <= file_no <= 5:
            print("[Step a] : After Lower casing the text")
            print(content)

        # Tokenizing the content
        tokens = word_tokenize(content)
        if 1 <= file_no <= 5:
            print("[Step b] : After tokenizing the text")
            print(tokens)

        # Removing the stopwords from the tokens
        tokens = [token for token in tokens if token not in stop_words]
        if 1 <= file_no <= 5:
            print("[Step c] : After removing the stopwords from the text")
            print(tokens)

        # Removing the punctuations
        #These lines commented below if uncommented will enable the data to be more information specific
        # This is because other kinds of punctuations are removed but not hyphen
#         split_tokens = []
#         for token in tokens:
#             if '=' in token or '/' in token:
#                 split_tokens.extend(re.split(r'[=/]', token))
#             else:
#                 split_tokens.append(token)

#         tokens = split_tokens
#         if 1 <= file_no <= 5:
#             print("After splitting tokens containing '=' or '/'")
#             print(tokens)
            
#         tokens = [word for word in tokens if word.isalpha() or '-' in word]
        
        #This assumption takes all the words or terms separately by removing every kind of punctuation
        tokens = re.split(r'[^a-zA-Z0-9]+', ' '.join(tokens))
        
        if 1 <= file_no <= 5:
            print("[Step d] : After removing punctuations from text")
            print(tokens)
            
        # Removing the blank spaces
        tokens = [token for token in tokens if token.strip()]
        if 1 <= file_no <= 5:
            print("[Step e] : After removing blank spaces from text")
            print(tokens)

    with open(output_path, 'w') as output_file:
        output_file.write(' '.join(tokens))


# In[2]:


def main():
    for i in range(1, 1000):
        file_no = str(i)
        input_path = 'C:/Users/JAYSA/Downloads/IR/text_files-20240130T135916Z-001/text_files/file{}.txt'.format(file_no)
        output_folder = 'C:/Users/JAYSA/Downloads/IR/modified_preprocessed_files'
        output_path = os.path.join(output_folder, 'preprocessed_file{}.txt'.format(file_no))

        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        if i in range(1, 6):
            print("File {} before preprocessing:".format(i))
            with open(input_path, 'r') as f:
                for line in f:
                    print(line)
                    print()

        # This does all the preprocessing and prints the first 5 files
        preprocess_file(input_path, output_path)

        if i in range(1, 6):
            print("File {} after preprocessing:".format(i))
            with open(output_path, 'r') as f:
                for line in f:
                    print(line)
                    print()

if __name__ == "__main__":
    main()

