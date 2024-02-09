#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Jay Saraf 2020438
import os
import nltk
import re
import json
import pickle
from tqdm.notebook import tqdm
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

nltk.download('punkt')
nltk.download('stopwords')


# In[2]:


def preprocess(text):
    # Lowercasing the text
    text = text.lower()
    # Performing tokenization
    tokens = word_tokenize(text)
    # Removing stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [word for word in tokens if not word in stop_words]
    # Removing punctuations
    #These lines commented below if uncommented will enable the data to be more information specific
    # This is because other kinds of punctuations are removed but not hyphen
#     split_tokens = []
#     for token in tokens:
#         if '=' in token or '/' in token:
#             split_tokens.extend(re.split(r'[=/]', token))
#         else:
#             split_tokens.append(token)

#     tokens = split_tokens

#     tokens = [word for word in tokens if word.isalpha() or '-' in word]
#     The below assumption separates all the words or terms in order to do punctuation
    
    tokens = re.split(r'[^a-zA-Z0-9]+', ' '.join(tokens))
    # Removing blank space tokens
    tokens = [word for word in tokens if word.strip()]
    return tokens


# In[3]:


def create_dict(tokens, filename, db):
    # Iterating over every token in the list of tokens
    for i, token in enumerate(tokens):
        if token in db:
            if filename in db[token]:
                db[token][filename].append(i)
            else:
                db[token][filename] = [i]
        else:
            db[token] = {filename: [i]}


# In[4]:


def build_index(directory):
    os.chdir(directory)
    db = {}
    for filename in tqdm(os.listdir()):
        with open(filename, 'r') as f:
            text = f.read()
        tokens = preprocess(text)
        create_dict(tokens, filename, db)
    return db


# In[5]:


db = build_index('C:/Users/JAYSA/Downloads/IR/modified_preprocessed_files')


# In[6]:


# print(len(db))


# In[7]:


# Saving indices to the pickle file
def save_index_to_pickle(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'wb') as f:
        pickle.dump(db, f)

# Saving indices in the text file in order to check values
def save_index_to_txt(filename):
    directory = os.path.dirname(filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if os.path.exists(filename):
        os.remove(filename)
    with open(filename, 'w') as f:
        f.write(json.dumps(db, indent=4))


# In[8]:


save_index_to_pickle('C:/Users/JAYSA/Downloads/IR/PositionalIndex/positional_index.pickle')
save_index_to_txt('C:/Users/JAYSA/Downloads/IR/PositionalIndex/positional_index.txt')


# In[9]:


def positional_query(phrase_query):
    # Preprocess the input phrase query
    sentence = preprocess(phrase_query)
    # If only one term is found in the preprocessed query
    if len(sentence) == 1:  
        # Then return the set of document IDs where the terms occurs
        posting_list = db.get(sentence[0], {})
        return posting_list.keys()  

    result = set()
    term_postings = [db.get(term, {}) for term in sentence]  # Get posting lists for each term

    # Find common documents containing all terms
    common_documents = set.intersection(*[set(postings.keys()) for postings in term_postings])

    # Check for consecutive positions in each common document
    for doc_id in common_documents:
        start_positions = [postings[doc_id] for postings in term_postings]
        for i in range(len(start_positions[0])):
            # Checking whether the terms are consecutively positioned in the query
            if all(start_positions[j][i] + 1 in start_positions[j+1] for j in range(len(sentence) - 1)):
                result.add(doc_id)
                break

    return result


# In[ ]:


def main():
    n = int(input("Enter the number of queries to execute:"))
    print("Enter queries below:")
    queries = [input() for query in range(n)]
    
    # Storing the dictionary
    with open('C:/Users/JAYSA/Downloads/IR/PositionalIndex/positional_index.pickle', 'rb') as f:
        db = pickle.load(f)

    # Iterating over all the queries
    for i, query in enumerate(queries):
        total_docs = positional_query(query)
        print(f"Number of documents retrieved for query {i+1} using positional index: {len(total_docs)}")
        print(f"Names of documents retrieved for query {i+1} using positional index: {total_docs}")

if __name__ == "__main__":
    main()

