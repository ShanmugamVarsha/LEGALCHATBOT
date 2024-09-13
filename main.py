from spacy.lang.en import English
import numpy
from flask import Flask, render_template, request
import json
import pickle
import os
import time
import tensorflow as tf
from tensorflow.keras import layers, models, regularizers
# from voc import voc
import random
from flask import Flask,redirect,url_for,render_template,request,redirect,session
import os
from werkzeug.utils import secure_filename
from flask import Flask,render_template,url_for,request

nlp = English()
tokenizer = nlp.Defaults.create_tokenizer(nlp)
PAD_Token=0
UPLOAD_FOLDER = os.path.join('static', 'images')
app = Flask(__name__)
     
model= models.load_model('mymodel.h5')
        
with open("mydata.pickle", "rb") as f:
    data = pickle.load(f)

def predict(ques):
    ques= data.getQuestionInNum(ques)
    ques=numpy.array(ques)
   # ques=ques/255
    ques = numpy.expand_dims(ques, axis = 0)
    y_pred = model.predict(ques)
    res=numpy.argmax(y_pred, axis=1)
    return res
    

def getresponse(results):
    tag= data.index2tags[int(results)]
    response= data.response[tag]
    return response

def chat(inp):
    while True:
        inp_x=inp.lower()
        results = predict(inp_x)
        response= getresponse(results)
        return random.choice(response)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = 'This is your secret key to utilize session in Flask'
@app.route("/")
def main():
    return render_template("main.html")

@app.route("/passhome")
def passhome():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template('about.html')
@app.route("/translate")
def translate():
    return render_template("translate.html")


@app.route("/predict11",methods=["POST","GET"])

def predict11():
    if request.method=="POST":
        sentence=request.form["firstname"]
        lang=request.form["language"]
        from translate import Translator
        from gtts import gTTS
        import os

        def text_to_speech(text, lang='en'):
            tts = gTTS(text=text, lang=lang)
            tts.save("output.mp3")
            os.system("start output.mp3") 

        # Example usage
        text = sentence
        text_to_speech(text)
       

        def translate_to_languages(sentence,lang):
            lang=str(lang)
            translator = Translator(to_lang=lang)  
            # Initialize translator for Hindi
            translation = translator.translate(sentence)

            return {'Sentense is':translation}
 
        # Example usage
        translations = translate_to_languages(sentence,lang)
        for language, translation in translations.items():
            print(f'{language}: {translation}')

        return render_template('translate.html',val=translation)
@app.route("/contact")
def contact():
    return render_template('contact.html')
@app.route("/register",methods=["POST","GET"])
def register():
    
    if request.method=="POST":
        name=request.form["firstname"]
        lname=request.form["lastname"]
        uemail=request.form["email"]
        Password=request.form["password"]
        print(name,lname,uemail,Password)
        import sqlite3
        con=sqlite3.connect("test1.db")
        print(con)
        cur=con.cursor()
        a=f"select email from emp where email='{uemail}'"
        cur.execute(a)
        result=cur.fetchone()
        if result!=None:
            return "email alredy registered"
        else:
        #a="create table emp(name varchar(100),lastname varchar(100),email varchar(100),password varchar(100))"
            cur.execute("INSERT INTO emp('name', 'lastname', 'email', 'password') VALUES (?,?,?,?)",(name,lname,uemail,Password))
            con.commit()
            con.close()
            return render_template("login.html")
    return render_template("register.html")
 

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        uemail=request.form["email"]
        upassword=request.form["password"]
        print(uemail,upassword)
        import sqlite3
        con=sqlite3.connect("test1.db")
        cur=con.cursor()
        a=f"select * from emp where email='{uemail}' and password ='{upassword}'"
        cur.execute(a)
        result=cur.fetchone()
        print("database",result)
        sr=str(result[0])+" "+str(result[1])
        if result==None:
            return "enter valid details"
        else:
            return render_template("index.html",sr=sr)
    return render_template("login.html")

@app.route("/logout")
def logout():
    return redirect(url_for("main"))
    
@app.route("/home",methods=["POST","GET"])
def home():
	return render_template('home.html')

@app.route("/get")
def get_bot_response():
    userText = request.args.get('msg')
    time.sleep(1)
    return str(chat(userText))

if __name__ == "__main__":
        app.run()
 
