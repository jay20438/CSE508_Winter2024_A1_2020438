#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Jay Saraf 2020438
import os
import re
import pickle 
from nltk.tokenize import word_tokenize
import json
import nltk
from nltk.corpus import stopwords


# In[2]:


os.chdir('C:/Users/JAYSA/Downloads/IR/modified_preprocessed_files')
all_docs = os.listdir()

def preprocess(text):

    # Converting the text to lowercase.
    text = text.lower()
    # Performing tokenization
    tokens = word_tokenize(text)
    # Removing stopwords from the text
    stop_words = set(stopwords.words('english'))
    tokens = [w for w in tokens if not w in stop_words]

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

    # Removing blank spaces in the tokens
    tokens = [w for w in tokens if w.strip()]

    # Removal of repeated tokens and preserving the order of tokens in the list
    tokens = list(dict.fromkeys(tokens))
    return tokens


# In[3]:


store_dictionary = {}

def create_dict(tokens, filename):
    for token in tokens:
        if token in store_dictionary:
            store_dictionary[token][0].append(filename)
            store_dictionary[token][1] += 1
        else:
            store_dictionary[token] = [[filename], 1]

for filename in os.listdir():
    with open(filename, 'r') as f:
            text = f.read()
    tokens = preprocess(text)
    create_dict(tokens, filename)

# save the dictionary in a pickle file
os.chdir("C:/Users/JAYSA/Downloads/IR/InvertedIndex/")
# delete file with given filename in directory
if os.path.exists('inverted_index.pickle'):
    os.remove('inverted_index.pickle')

# save the dictionary in a pickle file
with open('inverted_index.pickle', 'wb') as f:
    pickle.dump(store_dictionary, f)


# In[4]:


# delete file with given filename in directory
if os.path.exists('inverted_index.txt'):
    os.remove('inverted_index.txt')

with open('inverted_index.txt', 'w') as f:
    f.write(json.dumps(store_dictionary, indent=4))


# In[5]:


print(len(store_dictionary))


# In[6]:


os.chdir('C:/Users/JAYSA/Downloads/IR/InvertedIndex')


# In[7]:


#load the invertedindex data
with open('inverted_index.pickle', 'rb') as handle:
    invertedindex = pickle.load(handle)

def get_posting_list(term):
    if term in invertedindex:
        return invertedindex[term][0]
    else:
        return []

def get_posting_listsize(term):
    if term in invertedindex:
        return invertedindex[term][1]


# In[8]:


print(len(all_docs))


# In[21]:


print(invertedindex)


# In[22]:


def and_operation(posting_list1,posting_list2,size_posting1,size_posting2):
    result = []
    i = 0
    j = 0
#     print("posting_list2:", posting_list2)
#     print("length of list1 ",len(posting_list1))
#     print("length of list2 ",len(posting_list2))
#     print("posting_list1:", posting_list1)
    while i < size_posting1 and j < size_posting2:
        if posting_list1[i] == posting_list2[j]:
            result.append(posting_list1[i])
            print("Updated result",result)
            print("posting_list1:", posting_list1[i])
            i += 1
            j += 1
        elif posting_list1[i] < posting_list2[j]:
            i += 1
        else:
            j += 1
    print(result)
    print("len(result)",len(result))
    return result


# In[23]:


def or_operation(posting_list1,posting_list2,size_posting1,size_posting2):
#     print("****** size_posting1 *****",type(size_posting1))
#     print("****** size_posting2 *****",size_posting2)
#     print(posting_list1)
#     print(posting_list2)
    or_result = []
    i,j = 0,0
    while i < size_posting1 and j < size_posting2:
        if posting_list1[i] == posting_list2[j]:
            or_result.append(posting_list1[i])
            i += 1
            j += 1
        elif posting_list1[i] > posting_list2[j]:
            or_result.append(posting_list2[j])
            j += 1
        else:
            or_result.append(posting_list1[i])
            i += 1
    
    if i < size_posting1:
        or_result.extend(posting_list1[i::])
    if j < size_posting2:
        or_result.extend(posting_list2[j::])
    
    return or_result


# In[24]:


def or_not_operation(posting_list1,posting_list2,size_posting1,size_posting2):
#     print("size_posting2 : ",size_posting2)
#     print("size_posting1 : ",size_posting1)
#     print("posting_list2",posting_list2)
#     print("posting_list1",posting_list1)
    output = []

    diff = list(set(all_docs) - set(posting_list2))
#     print("length of diff",len(diff))
    output = or_operation(posting_list1,diff,size_posting1,len(diff))
#     print("the output is :",output)
    output = list(set(output))
#     print("length of output", len(output))
    return output


# In[25]:


def and_not_operation(posting_list1, posting_list2, size_posting1, size_posting2):
    print("size_posting2 : ",size_posting2)
    print("size_posting1 : ",size_posting1)
    print("posting_list2",posting_list2)
    print("posting_list1",posting_list1)
    output = []

    diff = list(set(all_docs) - set(posting_list2))
#     print("length of diff",len(diff))
    output = and_operation(posting_list1,diff,size_posting1,len(diff))
#     print(diff)
#     print("the output is :",output)
    output = list(set(output))
#     print("length of output", len(output))
    return output


# In[27]:


def main():
    n = int(input("Enter the number of queries you want to run:"))
    phrase = []
    operators = []
    for k in range(n):
        input_sequence = input("Enter the query phrase:")
        operations = input("Enter the operator (in a comma separated manner):")
        
        while len(word_tokenize(input_sequence)) != len(operations.split(',')) + 1:
            print("Number of tokens should be one more than the number of operators. Please re-enter.")
            input_sequence = input("Enter the query phrase:")
            operations = input("Enter the operator (in a comma-separated manner):")
        
        
        phrase.append(input_sequence)
        operators.append(operations)
#         print(operators)
    for i in range(n):
        query = phrase[i]
        query = query.lower()
        query = preprocess(query)
        op = operators[i]
        op = op.split(',')
        op = [ele.strip() for ele in op]
#         print("The query is", query)
        result = get_posting_list(query[0])
        size = get_posting_listsize(query[0])
        index = 0
#         print("query[index+1]",query[index+1])
        while index < len(op):
            if op[index] == 'AND':
                result = and_operation(result, get_posting_list(query[index+1]), size, get_posting_listsize(query[index+1]))
                size = len(result)
            elif op[index] == 'OR':
                result = or_operation(result, get_posting_list(query[index+1]), size, get_posting_listsize(query[index+1]))
                size = len(result)
            elif op[index] == 'AND NOT':
                result = and_not_operation(result, get_posting_list(query[index+1]), size, get_posting_listsize(query[index+1]))
                size = len(result)
            elif op[index] == 'OR NOT':
                result = or_not_operation(result, get_posting_list(query[index+1]), size, get_posting_listsize(query[index+1]))
                size = len(result)
            else:
                print("Invalid operator:", op[index])
                print("Please re-enter the operator.")
                op[index] = input("Enter the operator:")

                # Keep prompting until a correct operator is entered
                while op[index] not in ['AND', 'OR', 'AND NOT', 'OR NOT']:
                    stop_further = input("Do you want to quit?(Yes/No):")
                    if stop_further == "Yes":
                        break
                    else:
                        print("Please re-enter the operator.")
                        print("Invalid operator:", op[index])
                        op[index] = input("Enter the operator:")
                    
            index += 1
        # Construct the query string using the corresponding elements of query and op
        query_given = query[0]
        for j in range(len(op)):
            query_given += ' ' + op[j] + ' ' + query[j+1]

        print(f"Query {i+1} : {query_given}")
        print(f"Number of documents retrieved for query {i+1} {len(result)}")
        print(f"Names of the documents retrieved for query {i+1} : {result}")

if __name__ == "__main__":
    main()


# In[ ]:




