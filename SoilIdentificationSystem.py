from tkinter import *
from tkinter import filedialog
import requests
import os 
from datetime import datetime
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox
from PIL import Image, ImageTk
import mysql.connector as a
import matplotlib.image as img
import pandas as pd
import cv2 
root = Tk()
img_path = "hi"
final_ph="hello"

#frames
name=Label(root,text="SOIL IDENTIFICATION SYSTEM",fg="black",font="roboto 25 bold")
name.pack()
f1 = LabelFrame(root,text="testing section",padx=25,pady=5)
f1.pack(side=LEFT,padx=50,pady=50 )
#f2 = LabelFrame(root,borderwidth=6,bg="white",width=250,height=200,text="cropped image")
#f2.pack(side=LEFT ,pady=70,padx=20,anchor='sw')
f4 =Frame(root,borderwidth=6)
f4.pack(side=BOTTOM,anchor='sw',padx=100,pady=50)
f3 =Frame(root,borderwidth=6)
f3.pack(side=RIGHT,padx=30,anchor='se')
main_image= Frame(root,borderwidth=6,bg="white",width=200,height=200)
main_image.pack(side=BOTTOM )

def Image_open():
    fln = filedialog.askopenfilename(initialdir = os.getcwd(), title="Select Tmage file", filetypes=(("JPEG File",".jpeg"),("JPG File",".jpg"),("PNG file", ".png"),("All Files",".")))# fln stores image location
    global img_path
    
    img_path = fln
    img = Image.open(fln)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image = img)
    lbl_label.image = img
    

def Predict_Ph():
    global img_path
    global final_ph
    image=img.imread(img_path)
#print(image.shape)
    r,g,b=[],[],[]
    for row in image:
        for pixel in row:
            temp_r,temp_g,temp_b=pixel
            r.append(temp_r)
            g.append(temp_g)
            b.append(temp_b)       
    R=(sum(r)//len(r)) % 256
    G=(sum(g)//len(g)) % 256
    B=(sum(b)//len(b)) % 256
    #print(R,G,B)
    avg= G/B
    ph= avg/R
    mydb=a.connect(host="localhost",user="root",password="soil@123",database="soilDB")
    mycursor=mydb.cursor()
    mycursor.execute(f"""select actualpH from soilpH where {ph}  between min and max""")
    myres=mycursor.fetchone()
    tup=myres[0]
    final_ph=tup
    rvalue.set(R)
    gvalue.set(G)
    bvalue.set(B)
    phvalue_2.set(ph)
    phvalue.set(final_ph)
    
    
    
    
def Crop_Recommendation():
    global pop
    global e
    pop = Toplevel(root)
    pop.title("           Location")
    pop.geometry("250x200")
    
    pop_label =Label( pop, text="Enter the City Name")
    pop_label.pack(pady=10)
    
    my_Farme = Frame(pop)
    my_Farme.pack(pady=3)
   
    e = Entry(pop, width = 20, borderwidth = 2)
    e.pack()
    City = Button(pop, text = "Done", command = Recommend)
    City.pack(pady=5)

    
def Recommend():
    global final_ph
    complete_api_link = r"https://api.openweathermap.org/data/2.5/weather?q="+e.get()+"&appid=c79d4432bfdce79321a7fe9a0e3482ae"
    api_link = requests.get(complete_api_link)
    api_data = api_link.json()

    if  api_data['cod'] == '404':
        messagebox.showerror("Location Error"," Invalid City: "+e.get()+", \n Please Check your city name")
    else:
        temp_city = int((api_data['main']['temp'] - 273.15))
        hmdt = api_data['main']['humidity']
        print(hmdt,temp_city,e.get())
        mydb=a.connect(host="localhost",user="root",password="soil@123",database="soilDB")
        mycursor=mydb.cursor()
        mycursor.execute(f"""select crop from croprec where  ({final_ph}  between minpH and maxpH) and 
        ({temp_city} between mintemp and maxtemp) and ({hmdt} between minhum and maxhum)""")
        myres=mycursor.fetchall()
        r = ' '.join(map(str, myres))
        j= r.replace("('","")
        z=j.replace("',)",", ")
        messagebox.showinfo("Crop Recommended",z)
    
def Upload_image():
    global img_path
    img=cv2.imread(img_path,cv2.IMREAD_GRAYSCALE)
#cv2.imshow('Img',img) 
    laplacian_var=cv2.Laplacian(img, cv2.CV_64F).var()
    if laplacian_var < 350:
        messagebox.showerror("Image Error:Blur image","Please select another image")
        #text = Label(text= "Please input correct image", bg='white', fg='blue', padx=655, pady=435)# used to write text
        #text.pack()
    else:
        messagebox.showinfo("Image upload","Image uploaded successfully")
        


lbl = Label(main_image,width=300,height=300)
lbl.pack()


#lable and textfield for frame 3
l1=Label(f3,text="FEATURE EXTRACTION SECTION",fg="black",font="roboto 12 bold")
rindex=Label(f3,text="R INDEX ",fg="black",font="roboto 9 bold")
gindex=Label(f3,text="G INDEX ",fg="black",font="roboto 9 bold")
bindex=Label(f3,text="B INDEX ",fg="black",font="roboto 9 bold")
l1.grid(row=0,column=1,pady=30)
rindex.grid(row=1,column=0,pady=10)
gindex.grid(row=2,column=0,pady=10)
bindex.grid(row=3,column=0,pady=10)

rvalue=StringVar()
gvalue=StringVar()
bvalue=StringVar()

rentry=Entry(f3,textvariable=rvalue)
gentry=Entry(f3,textvariable=gvalue)
bentry=Entry(f3,textvariable=bvalue)
rentry.grid(row=1,column=1,pady=10)
gentry.grid(row=2,column=1,pady=10)
bentry.grid(row=3,column=1,pady=10)

#frame4 entries(final Ph)
l2=Label(f4,text="Color Based Results",fg="black",font="roboto 15 bold")
l2.grid(row=0,column=0,pady=30)
l3=Label(f4,text="FINAL OUTPUT (Ph)",fg="black",font="roboto 11 bold")
l3.grid(row=1,column=0,pady=10)
phvalue=StringVar()
phentry=Entry(f4,textvariable=phvalue)
phentry.grid(row=2,column=0,pady=10)
l4=Label(f4,text="Soil pH index",fg="black",font="roboto 15 bold")
l4.grid(row=0,column=2,pady=30)
l5=Label(f4,text="FINAL OUTPUT (Ph)",fg="black",font="roboto 11 bold")
l5.grid(row=1,column=2,pady=10)
phvalue_2=StringVar()
phentry_2=Entry(f4,textvariable=phvalue_2)
phentry_2.grid(row=2,column=2,pady=10)


#BUTTONS
Browse = Button(f1,text="Browse Test Image", padx=45,pady=10, command = Image_open, fg="black" )#padx,y to change button size
Ph = Button(f1,text="Predict PH", padx=65,pady=10, command = Predict_Ph, fg="black")
Crop = Button(f1,text="Exit",command=root.destroy, padx=85,pady=10 , fg="black")
upload = Button(f1,text="upload",command=Upload_image, padx=75,pady=10,  fg="black")
find=Button(f4,text="Find Suitable Crops",command = Crop_Recommendation,padx=15,pady=10)

Browse.pack(pady=20)
Ph.pack(pady=20)
upload.pack(pady=20)
Crop.pack(pady=20)
find.grid(row=4,column=1,pady=10)

root.title("SOIL RECOMMENDATION SYSTEM")
root.geometry("300x350")
root.mainloop()