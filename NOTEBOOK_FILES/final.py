import pandas as pd
from tkinter import *
from tkinter import ttk
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import random
from PIL import ImageTk, Image  

root = Tk()
root.title("Welcome")
img =Image.open('aa.webp')
img=img.resize((1500,750))
bg = ImageTk.PhotoImage(img)

##root.geometry("550x450")

# Add image
label = Label(root, image=bg)
label.place(x = 0,y = 0)

root.geometry("1500x750")

# Add image
label = Label(root, image=bg)
label.place(x = 0,y = 0)

import pickle
rf=pickle.load(open("rf.pkl","rb"))
label_1 = ttk.Label(root, text ='EPILEPTIC PREDICTION ',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_1.place(x = 500,y = 25)


label_1 = ttk.Label(root, text ='Age',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_1.place(x = 100,y = 200)
    
Entry_1= Entry(root,font=("Helvetica", 24))
Entry_1.place(x = 300,y = 200)


label_2 = ttk.Label(root, text ='Sex',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_2.place(x = 100,y = 250)

options = StringVar(root)
options.set("select option") # default value

om1 = OptionMenu(root, options, "Male","Female")
om1.place(x = 300,y = 250)


    
label_3 = ttk.Label(root, text ='Height',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_3.place(x = 100,y = 300)
    
Entry_3 = Entry(root,font=("Helvetica", 24))
Entry_3.place(x = 300,y = 300)

label_31 = ttk.Label(root, text ='in cms',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_31.place(x = 750,y = 300)




label_4 = ttk.Label(root, text ='Weight',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_4.place(x = 100,y = 350)
    
Entry_4 = Entry(root,font=("Helvetica", 24))
Entry_4.place(x = 300,y = 350)



label_5 = ttk.Label(root, text ='ECG Rate',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_5.place(x = 100,y = 400)
    
Entry_5 = Entry(root,font=("Helvetica", 24))
Entry_5.place(x = 300,y = 400)


label_6 = ttk.Label(root, text ='Heart Rate',background="#14161a",foreground="#ffffff",font=("Helvetica", 24))
label_6.place(x = 100,y = 450)
    
Entry_6 = Entry(root,font=("Helvetica", 24))
Entry_6.place(x = 300,y = 450)


label_6 = ttk.Label(root, text ='Temp',font=("Helvetica", 24),background="#14161a",foreground="#ffffff")
label_6.place(x = 100,y = 500)
    
Entry_7 = Entry(root,font=("Helvetica", 24))
Entry_7.place(x = 300,y = 500)


def predict():
   
    age = Entry_1.get()
    sex = options.get()
    print(sex)
    if sex == "Male":
        sex = 0
    else:
        sex = 1
    height = Entry_3.get()
    weight = Entry_4.get()
    ecg = Entry_5.get()
    hb = Entry_6.get()
    temp = Entry_7.get()
    out = rf.predict([[float(age),float(sex),float(height),float(ecg),float(hb),float(temp)]])
    print(out)
    if out[0] == 0 :
        res="Normal"
    else: 
        res='Epileptic Seizure'
    output.configure(text=res)
b1 = Button(root, text = 'predict',font=("Helvetica", 18),background="#14161a",command = predict,foreground="#ffffff")
b1.place(x = 80,y = 550)
    
output = Label(root,font=("Helvetica", 18,"bold"))
output.place(x = 280,y = 550)
root.mainloop()
