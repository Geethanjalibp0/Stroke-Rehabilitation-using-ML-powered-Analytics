from flask import Flask, render_template, request, flash, redirect,session,url_for
import sqlite3
import pickle
import numpy as np
from datetime import datetime

# Get current date and time
import google.generativeai as genai
genai.configure(api_key='***************************************')
gemini_model = genai.GenerativeModel('*************')
chat = gemini_model.start_chat(history=[])

chat_history = []


app = Flask(__name__)
app.secret_key="*************"

import pickle
knn=pickle.load(open("model/model.pkl","rb"))
import telepot

connection = sqlite3.connect('table_name.db')
cursor = connection.cursor()


command = """CREATE TABLE IF NOT EXISTS history(id INTEGER PRIMARY KEY AUTOINCREMENT, Pid TEXT, date TEXT , hb TEXT,temp TEXT,ecg TEXT, prediciton TEXT, recommendation TEXT)"""
cursor.execute(command)

command = """CREATE TABLE IF NOT EXISTS user(id INTEGER PRIMARY KEY AUTOINCREMENT,  name TEXT, password TEXT, mobile TEXT, email TEXT)"""
cursor.execute(command)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/userlog', methods=['GET', 'POST'])
def userlog():
    if request.method == 'POST':

        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']

        query = "SELECT * FROM user WHERE name = '"+name+"' AND password= '"+password+"'"
        cursor.execute(query)

        result = cursor.fetchone()

        if result:
            session['id'] = result[0]
            session['name'] = name
            import requests
            import pandas as pd
            data=requests.get("https://api.thingspeak.com/******/*******/*******************************************")
            hb=data.json()['feeds'][-1]['field1']
            temp=data.json()['feeds'][-1]['field2']
            ecg=data.json()['feeds'][-1]['field3']
            print(f"heart beat : {hb} \n temperature : {temp} \n ECG : {ecg}")


            return render_template('fetal.html',hb=hb,temp=temp,ecg=ecg,name=name)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/adminlog', methods=['GET', 'POST'])
def adminlog():
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        connection = sqlite3.connect('table_name.db')
        cursor = connection.cursor()
        if name == "admin" and password == "admin123":
            query = "SELECT * FROM user"
            cursor.execute(query)
            result = cursor.fetchall()
            return render_template('adminlog.html', result=result)
        else:
            return render_template('index.html', msg='Sorry, Incorrect Credentials Provided,  Try Again')

    return render_template('index.html')


@app.route('/update', methods=['GET', 'POST'])
def update():
    if request.method == 'POST':

        connection = sqlite3.connect('table_name.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        cursor.execute("update user set name = '"+name+"', password = '"+password+"', mobile = '"+mobile+"', email = '"+email+"' where id = '"+str(session['id'])+"'")
        connection.commit()

        return render_template('index.html', msg='Successfully Updated')
    
    return render_template('index.html')

@app.route('/userreg', methods=['GET', 'POST'])
def userreg():
    if request.method == 'POST':

        connection = sqlite3.connect('table_name.db')
        cursor = connection.cursor()

        name = request.form['name']
        password = request.form['password']
        mobile = request.form['phone']
        email = request.form['email']
        
        print(name, mobile, email, password)

        cursor.execute("INSERT INTO user VALUES (NULL, '"+name+"', '"+password+"', '"+mobile+"', '"+email+"')")
        connection.commit()

        return render_template('index.html', msg='Successfully Registered')
    
    return render_template('index.html')

@app.route('/ahome')
def ahome():
    connection = sqlite3.connect('user_data.db')
    cursor = connection.cursor()
    query = "SELECT * FROM user"
    cursor.execute(query)
    result = cursor.fetchall()
    return render_template('adminlog.html', result=result)

@app.route('/view/<Id>')
def view(Id):
    print(Id)
    connection = sqlite3.connect('table_name.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user where id=?", [Id])
    row = cursor.fetchone()

    cursor.execute("SELECT * FROM history where Pid=?", [Id])
    results = cursor.fetchall()

    return render_template('userhistory.html', results=results, row=row)

@app.route('/delete/<Id>')
def delete(Id):
    print(Id)
    connection = sqlite3.connect('table_name.db')
    cursor = connection.cursor()
    cursor.execute("delete FROM history where id=?", [Id])
    connection.commit()

    return redirect(url_for('ahome'))

@app.route('/history')
def history():
    Id = session['id']
    print(Id)
    connection = sqlite3.connect('table_name.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM history where Pid=?", [Id])
    results = cursor.fetchall()
    return render_template('history.html', results=results)

@app.route('/logout')
def logout():
    return render_template('index.html')

@app.route('/profile')
def profile():
    connection = sqlite3.connect('table_name.db')
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM user where id=?", [session['id']])
    row = cursor.fetchone()
    print(row)
    return render_template('profile.html', row=row)

@app.route("/fetalPage", methods=['GET', 'POST'])
def fetalPage():
    import requests
    import pandas as pd
    data=requests.get("https://api.thingspeak.com/*************/************/*******************************************")
    hb=data.json()['feeds'][-1]['field1']
    temp=data.json()['feeds'][-1]['field2']
    ecg=data.json()['feeds'][-1]['field3']
    print(hb, temp, ecg)
    return render_template('fetal.html',hb=hb,temp=temp,ecg=ecg, name=session['name'])

@app.route("/predict", methods = ['POST', 'GET'])
def predictPage():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        Gender = request.form['Gender']
        height = request.form['height']
        Weight = request.form['Weight']
        ECG = request.form['ECG']
        his = int(request.form['his'])
        if his == 1:
            history="Stroke Occured in History"
        elif his == 0:
            history="No  Stroke Occured in History"
        
        Heart_Rate = request.form['Heart_Rate']
       
        Temperature = request.form['Temperature']
        
        data = np.array([[age, Gender, height, Weight, ECG, Heart_Rate, Temperature]])
        my_prediction = knn.predict(data)
        probabilities = knn.predict_proba(data)
        print(f"\n\n\n{probabilities[0][0]}\n\n\n")
        class_labels = knn.classes_
        for i, probs in enumerate(probabilities):
            print(f"Sample {i+1}:")
            for label, prob in zip(class_labels, probs):
                print(f"  Class {label}: {prob:.4f}")
        result = my_prediction[0]
        var=0
        if result == 1 :
            res='Normal'
            acc=f"{(1-probabilities[0][0])* 100:.2f}%"
        else:
            res='Stroke'
            acc=f"{ probabilities[0][0] * 100:.2f}%"
        
        # print(res)
        prompt=f"in Stroke prediciton  diagnosis using heartbeat ({Heart_Rate}) , ECG ({ECG}) , Tempearture ({Temperature})  and got result as {res} this is the  prediction i got so  you need to provide the '1) drug with dosage recommendatoin ,2) atleast 4 to 5 diet plan fr veg and non veg seperate seperately,3) write some do's and dont's,4) Exercise Suitable based on my Heartbeat {Heart_Rate}, Temperature {Temperature},ECG {ECG} in table  '(give in exact html format) "
        gemini_response = chat.send_message(prompt)
        recommendatoin = gemini_response.text
        recommendatoin = recommendatoin.replace("```html", "")
        recommendatoin = recommendatoin.replace("```", "")
        print("Output  is {}".format(res))
        msg = recommendatoin.replace("**", "\n")
        msg = msg.replace("*", "\n")


        now = datetime.now()
        timee=now.strftime("%Y-%m-%d %H:%M:%S")
        print(f"\n\n\n {timee} \n\n\n")
        connection = sqlite3.connect('user_data.db')
        cursor = connection.cursor()

        # Pid TEXT, date TEXT, , hb TEXT,temp TEXT,ecg TEXT, prediciton TEXT, recommendation TEXT
        cursor.execute("INSERT INTO history VALUES (NULL,?,?,?,?,?,?,?)", [session['id'], timee, Heart_Rate, Temperature, ECG, res, msg])
        connection.commit()

        return render_template('predict.html',name=name, pred = result,status=res,recommendation=msg,acc=acc)

    return render_template('predict.html')

if __name__ == '__main__':
	app.run(debug = True)
