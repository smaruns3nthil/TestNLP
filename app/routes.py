from app import app
import json
from flask import render_template,redirect,flash,request
from spacyutils import parse

@app.route('/')
def parser():
    return render_template('main.html')
@app.route('/submitted_parse',methods=['POST'])
def submitted_parse():
    sentence=request.form['field3']
    choice=request.form['field4']
    print("choice is "+choice)
    span,b=parse(str(sentence))
    a=""
    print(span)
    if(len(span)>0):
        start=span[0][0]
        end=span[0][1]
        a=str(sentence[start:end])
    else:
        sentence="no span found"
    return render_template('submitted_main.html',a=a,sentence=sentence,choice=choice,span=json.dumps(span))
