import math
import pickle
import nltk
from nltk.stem import WordNetLemmatizer

lemmatizer=WordNetLemmatizer()

def tfidf(input_query):
    with open('posting.pickle','rb') as file:
        posting = pickle.load(file)
    with open('documentID.pickle','rb') as file:
        documents = pickle.load(file)

    from glob import glob
    listDoc = glob('Documents_new/corpus/*')
    N = len(listDoc) # temporary
    # print(listDoc)

    query = input_query
    query = query.lower()
    queryWords = query.split()
    posOfWords = []
    for word in queryWords:
        newword = ''.join(e for e in word if e.isalnum())
        newword = lemmatizer.lemmatize(newword)
        if newword in posting:
            posOfWords.append((newword,posting[newword])) ## array containing dict of {docid: positions} of the words from phrase query

    # termFrequency = {docid:len(freq) for i in posOfWords for docid,freq in i.items()}
    # print(termFrequency)

    posOfWordsnew = []
    for word in queryWords:
        newword = ''.join(e for e in word if e.isalnum())
        newword = lemmatizer.lemmatize(newword)
        if newword in posting:
            posOfWordsnew.append(posting[newword]) ## array containing {docid: positions} of the words from phrase query

    relevantDocId = set(posOfWords[0][1])
    for i,j in posOfWords:
        relevantDocId = set(j.keys()) | relevantDocId ## gets docid's which contains words from phrase query 
                                                    ## (| == set union operator)
    # print(relevantDocId)

    relevantDocIdnew = set(posOfWords[0][1])
    for i,j in posOfWords:
        relevantDocIdnew = set(j.keys()) & relevantDocIdnew ## gets docid's which contains words from phrase query 
                                                    ## (| == set union operator)
    # print(relevantDocId)

    # find best match
    def arrIntersection(arr1, arr2, diff):
        i,j = 0,0
        intersect = []
        n = len(arr1)
        m = len(arr2)
        while i < n and j < m:
            if arr1[i] + diff < arr2[j]:
                i += 1
            elif arr2[j] + diff < arr1[i]:
                j += 1
            else:
                intersect.append(arr1[i])
                i += 1
                j += 1
        return intersect
    # print(posting['capability'])
    # print(relevantDocId)
    present = 0 # index of queryWords[0]
    location = {}
    diff = 0
    for index in range(1,len(posOfWordsnew)):
        after = index # index of queryWords[i]
        for id in relevantDocIdnew:
            if id in location:
                intersect = set(count-diff for count in arrIntersection(posOfWordsnew[present][id],posOfWordsnew[after][id],1))
                # print(intersect)
                location[id] = intersect & location[id]
            else:
                location[id] = set(arrIntersection(posOfWordsnew[present][id],posOfWordsnew[after][id],1))
        # print(location)
        diff += 1
        present = after

    print(location)

    idf_t = {} # inverse document frequency of terms
    for term,docs in posOfWords:
            docFreq = len(docs)
            idf_t[term] = math.log10(N/(docFreq)) if (docFreq > 0) else 0
            # print(docFreq,N)

    # print(idf_t)

    ScoreOfDocs = []
    for docid in relevantDocId:
        noOfTermsInDocid = 0
        score = 0
        for term,docs in posOfWords:
            for doc,pos in docs.items():
                if docid == doc:
                    noOfTermsInDocid = len(pos)
                    break
            termFreq = noOfTermsInDocid/documents[docid][1] # documents[docid][1] contains total no. of words in the document
            score += termFreq * idf_t[term] # summation of tf-idf
        ScoreOfDocs.append((docid,score))
    # print(ScoreOfDocs)

    sortedScore = sorted(ScoreOfDocs,key= lambda x : x[1])
    # sortedScore.reverse()
    sortedScoresum = 0
    for i in sortedScore:
        sortedScoresum += i[1]

    sortedScore = [(i,(j/sortedScoresum) * 100) for (i,j) in sortedScore[::-1]]
    # print(sortedScore)

    sortedScore = [(i,100) for i in location.keys()] + [(i,j) for (i,j) in sortedScore if i not in location.keys()]
    return sortedScore