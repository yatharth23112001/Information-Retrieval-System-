# from docx import Document

docid = 0 # giving documents id
posting = {} # posting list {keyword: [list of doc id's containing it], position of word in docid }
documents = {} # shows which document belongs to which doc id and total no. of words in it

from glob import glob
listDoc = glob('Documents_new\corpus\*')

import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer=WordNetLemmatizer()


def for_text_doc(listDoc, docid):
    for docname in listDoc:
        doc = 0
        with open(docname,'r',encoding='utf-8') as file:
            doc = file.read()
        print(docname)
        docname = docname.split('\\')[-1]
        documents[docid] = [docname,0] 
        position = 0
        for word in doc.split():
            newword = ''.join(e for e in word if e.isalnum()) # keeping only alpha numerics
            newword = newword.lower()
            newword = lemmatizer.lemmatize(newword)
            if newword in posting:
                if docid in posting[newword]:
                    posting[newword][docid].append(position)
                else:
                    posting[newword][docid] = [position]
            else:
                posting[newword] = {docid:[position]}
            documents[docid][1] += 1 
                # [documents[docname],[]]
            # posting[newword] = {documents[docname]: positionList.append(position)}
            # print(newword)
            position+= 1
        docid += 1
        # print(sentence) 

for_text_doc(listDoc, docid)  

# print(posting['classification'])
print(len(posting))
print(documents[2])
import pickle

with open('posting.pickle','wb') as file:
    pickle.dump(posting,file)
with open('documentID.pickle','wb') as file:
    pickle.dump(documents,file)
