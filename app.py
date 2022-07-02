from re import I
from flask import Flask,request,redirect
from flask.templating import render_template
import textblob
import tfidf
import pickle
from textblob import Word
from textblob import TextBlob
from spellchecker import SpellChecker

app = Flask(__name__)

@app.route("/", methods=['GET','POST'])
def hello_world():
    data = []
    documents = {}
    with open('documentID.pickle','rb') as file:
        documents = pickle.load(file)
    
    with open('summary.pickle','rb') as file:
        summary = pickle.load(file)

    misspelled=0
    correctspell = ""
    query = "Default Input"
    if request.method=='POST':
        query = request.form['query']
        if query == "":
            return redirect("/")
        # spell = SpellChecker()
        # misspelled = spell.unknown(query)
        # misspelled = list(misspelled)
        correctspell = ""
        # print(misspelled)
        # if len(misspelled) != 0:
        
        correctspell = TextBlob(query)
        # using TextBlob.correct() method
        correctspell = correctspell.correct()

        if query != correctspell:
            misspelled = 1

        data = tfidf.tfidf(str(query))
        
        # for text summarization
        # data = [(documents[i], j, 'Documents_new\\corpus\\'+documents[i][0],summarize.run_summarization('Documents_new\\corpus\\'+documents[i][0]))for i,j in data]

        data = [(documents[i], j, 'Documents_new\\corpus\\'+documents[i][0], summary[i])for i,j in data]
        # if len(misspelled) == 0:
        #     return render_template("index.html", data = data)
    return render_template("index.html", data = data, misspelled = misspelled, correctspell = correctspell, query=query)

@app.route('/document', methods=['POST'])
def documents():
    data = 0
    if request.method=='POST':
        name = request.form['url']
        with open(name,'r+',encoding='utf-8') as file:
            data = file.read()
        nameofdoc = name.split('\\')[-1]
    return render_template("retdocs.html", data = data, nameofdoc = nameofdoc)

@app.route('/video_feed')
def video_feed():
    return render_template("index.html")

if __name__ == "__main__":  
    app.run(debug=True)