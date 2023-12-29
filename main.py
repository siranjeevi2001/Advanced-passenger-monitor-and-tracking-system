from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for
from PersonCount import VideoCamera2
from camera import VideoCamera
from camera2 import VideoCamera3
from datetime import datetime
from datetime import date
import datetime
import random
from random import seed
from random import randint
import cv2
import numpy as np
import threading
import os
import time
import shutil
import imagehash
from flask_mail import Mail, Message
import PIL.Image
from PIL import Image
from PIL import ImageTk
import urllib.request
import urllib.parse
from urllib.request import urlopen
import webbrowser
import argparse
import mysql.connector

import qrcode


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="",
  charset="utf8",
  database="train_monitor"
)


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'
#####
##email
mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_USERNAME": "stegofaceidissuer@gmail.com",
    "MAIL_PASSWORD": "pwxzxzkmnyygrakr"
}

app.config.update(mail_settings)
mail = Mail(app)
#######
@app.route('/',methods=['POST','GET'])
def index():
    cnt=0
    act=""
    msg=""
    ff=open("note.txt",'w')
    ff.write('1')
    ff.close()
    
    ff=open("det.txt","w")
    ff.write("1")
    ff.close()

    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()

    ff11=open("img.txt","w")
    ff11.write("1")
    ff11.close()

    ff=open("person.txt","w")
    ff.write("")
    ff.close()

    ff=open("people.txt","w")
    ff.write("0")
    ff.close()
    
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('admin1')) 
        else:
            result="Your logged in fail!!!"
        

    return render_template('index.html',msg=msg,act=act)
@app.route('/login', methods=['POST','GET'])
def login():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s && utype='admin'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('admin')) 
        else:
            result="Your logged in fail!!!"
                
    
    return render_template('login.html',result=result)

@app.route('/login1', methods=['POST','GET'])
def login1():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s && utype='railway'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('home_rw')) 
        else:
            result="Your logged in fail!!!"
                
    
    return render_template('login1.html',result=result)

@app.route('/login2', methods=['POST','GET'])
def login2():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM admin where username=%s && password=%s && utype='ttr'",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('home_ttr')) 
        else:
            result="Your logged in fail!!!"
                
    
    return render_template('login2.html',result=result)

@app.route('/login_user', methods=['POST','GET'])
def login_user():
    result=""
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    if request.method == 'POST':
        username1 = request.form['uname']
        password1 = request.form['pass']
        mycursor = mydb.cursor()
        mycursor.execute("SELECT count(*) FROM user_details where uname=%s && pass=%s",(username1,password1))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            result=" Your Logged in sucessfully**"
            return redirect(url_for('userhome')) 
        else:
            result="Your logged in fail!!!"
                
    
    return render_template('login_user.html',result=result)


@app.route('/train_list', methods=['POST','GET'])
def train_list():
    result=""

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM train")
    data = mycursor.fetchall()
    
                
    
    return render_template('train_list.html',data=data)

@app.route('/booking', methods=['POST','GET'])
def booking():
    msg=""
    tid=request.args.get("tid")
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        
        
        mycursor.execute("SELECT count(*) FROM register where aadhar=%s",(aadhar,))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            
            return redirect(url_for('book_ticket',adr=aadhar,tid=tid)) 
        else:
            msg="fail"
                
    
    return render_template('booking.html',msg=msg)

@app.route('/view1', methods=['POST','GET'])
def view1():
    msg=""
    tid=request.args.get("tid")
    mycursor = mydb.cursor()
    
    if request.method == 'POST':
        aadhar = request.form['aadhar']
        
        
        mycursor.execute("SELECT count(*) FROM register where aadhar=%s",(aadhar,))
        myresult = mycursor.fetchone()[0]
        if myresult>0:
            mycursor.execute("SELECT * FROM register where aadhar=%s",(aadhar,))
            d1 = mycursor.fetchone()
            vid=d1[0]
            mycursor.execute("SELECT * FROM booking where aadhar=%s order by id desc limit 0,1",(aadhar,))
            d2 = mycursor.fetchone()
            tid=d2[2]
            rid=d2[0]
            return redirect(url_for('ticket',rid=rid,tid=tid,vid=vid)) 
        else:
            msg="fail"
                
    
    return render_template('view1.html',msg=msg)

@app.route('/book_ticket', methods=['POST','GET'])
def book_ticket():
    msg=""
    aadhar=request.args.get("adr")
    tid=request.args.get("tid")
    mycursor = mydb.cursor()
    rid=""
    mycursor.execute("SELECT * FROM register where aadhar=%s",(aadhar,))
    data = mycursor.fetchone()
    name=data[1]
    vid=str(data[0])
        
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']

        mycursor.execute("SELECT max(id)+1 FROM booking")
        maxid = mycursor.fetchone()[0]
        if maxid is None:
            maxid=1

        rid=str(maxid)

        now = date.today() #datetime.datetime.now()
        rdate=now.strftime("%d-%m-%Y")
        code="A"+str(maxid)+tid
        
        
        sql = "INSERT INTO booking(id,aadhar,tid,travel_date,mobile,email,code,name) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (maxid,aadhar,tid,rdate,mobile,email,code,name)
        print(sql)
        mycursor.execute(sql, val)
        mydb.commit()

        
        ##
        # output file name
        filename = "Q"+str(maxid)+".png"
        # generate qr code
        img = qrcode.make(code)
        # save img to a file
        img.save("static/upload/"+filename)

        ######
        ##send mail
        mess="Dear "+name+", Your are Ticket Booked, "
        with app.app_context():
            msgg = Message(subject="QR - Ticket Booking", sender=app.config.get("MAIL_USERNAME"),recipients=[email], body=mess)
            with app.open_resource("static/upload/"+filename) as fp:  
                msgg.attach("static/upload/"+filename, "images/png", fp.read())
            mail.send(msgg)

        #####
        msg="ok"
        #return redirect(url_for('add_photo1',aadhar=aadhar,tid=tid,vid=vid)) 
                
    
    return render_template('book_ticket.html',msg=msg,data=data,vid=vid,tid=tid,rid=rid)

@app.route('/add_photo1',methods=['POST','GET'])
def add_photo1():
    vid = request.args.get('vid')
    tid = request.args.get('tid')
    rid = request.args.get('rid')
    vface=""
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    #ff2=open("mask.txt","w")
    #ff2.write("face")
    #ff2.close()
    act = request.args.get('act')
    
    ff=open("user.txt","w")
    ff.write(str(vid))
    ff.close()

    cursor = mydb.cursor()
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"
        

        cursor.execute('delete from vt_face WHERE vid = %s', (vid, ))
        mydb.commit()

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1=vid+"_"+str(v1)+".jpg"
        i=2
        while i<vv:
            
            cursor.execute("SELECT max(id)+1 FROM vt_face")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface=vid+"_"+str(i)+".jpg"
            sql = "INSERT INTO vt_face(id, vid, vface) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            cursor.execute(sql,val)
            mydb.commit()
            i+=1

        cursor.execute("update booking set face_img=%s where id=%s",(vface,rid))
        mydb.commit()
        return redirect(url_for('ticket',vid=vid,rid=rid,act='success'))
        
    
    cursor.execute("SELECT * FROM register")
    data = cursor.fetchall()
    return render_template('add_photo1.html',data=data, vid=vid,rid=rid,tid=tid)

@app.route('/ticket', methods=['POST','GET'])
def ticket():
    vid = request.args.get('vid')
    
    rid = request.args.get('rid')

    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM register where id=%s",(vid,))
    data = mycursor.fetchone()

    mycursor.execute("SELECT * FROM booking where id=%s",(rid,))
    data3 = mycursor.fetchone()
    tid=data3[2]
    
    mycursor.execute("SELECT * FROM train where id=%s",(tid,))
    data2 = mycursor.fetchone()          
    
    return render_template('ticket.html',data=data, data2=data2, data3=data3)

@app.route('/verify1', methods=['POST','GET'])
def verify1():
    msg=""
    mycursor = mydb.cursor()
    data3=[]
    eid=""
    vid=""
    code=""
    cvv=""
    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
            
    if request.method=='POST':
        file=request.files['file']
        fname = file.filename
        ffn=fname.split(".")
        
        mycursor.execute("SELECT * FROM booking")
        cc = mycursor.fetchall()
        for c1 in cc:
            cv=str(c1[0])
            cvv="Q"+cv
            print(cvv)
            if ffn[0]==cvv:
                code=c1[6]
                break

        mycursor.execute("SELECT count(*) FROM booking where code=%s",(code,))
        cn = mycursor.fetchone()[0]
        if cn>0:
            mycursor.execute("SELECT * FROM booking where code=%s",(code,))
            data3 = mycursor.fetchone()
            rid=data3[0]
            aadhar=data3[1]
            tid=data3[2]

            mycursor.execute("SELECT * FROM register where aadhar=%s",(aadhar,))
            data2 = mycursor.fetchone()
            vid=data2[0]

            mycursor.execute("SELECT count(*) FROM store_entry where aadhar=%s && tid=%s && rdate=%s",(aadhar,tid,rdate))
            dd2 = mycursor.fetchone()[0]

            if dd2==0:
                mycursor.execute("SELECT max(id)+1 FROM store_entry")
                maxid = mycursor.fetchone()[0]
                if maxid is None:
                    maxid=1
                
                
                sql = "INSERT INTO store_entry(id,booking_id,tid,aadhar,rdate) VALUES (%s,%s,%s,%s,%s)"
                val = (maxid,rid,tid,aadhar,rdate)
                print(sql)
                mycursor.execute(sql, val)
                mydb.commit()
                eid=str(maxid)
                msg="ok"
            else:

                mycursor.execute("SELECT * FROM store_entry where aadhar=%s && tid=%s && rdate=%s",(aadhar,tid,rdate))
                dd3 = mycursor.fetchone()
                eid=dd3[0]
                msg="ok"
            return redirect(url_for('verify2',vid=vid,rid=rid,tid=tid,eid=eid))
            
        else:
            msg="fail"
            
    return render_template('verify1.html',msg=msg, data3=data3,eid=eid,vid=vid)

@app.route('/verify2',methods=['POST','GET'])
def verify2():
    msg=""
    ss=""
    uname=""
    act=""
    st=""
    ss=""
    eid = request.args.get('eid')
    vid = request.args.get('vid')
    tid = request.args.get('tid')
    rid = request.args.get('rid')
    
    act = request.args.get('act')
        
    ff3=open("img.txt","r")
    mcnt=ff3.read()
    ff3.close()

    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM register where id=%s',(vid,))
    rw = mycursor.fetchone()
    return render_template('verify2.html',msg=msg,vid=vid,st=st,tid=tid,rid=rid,eid=eid)

@app.route('/process1',methods=['POST','GET'])
def process1():
    msg=""
    ss=""
    uname=""
    act=""
    st=""
    ss=""
    eid = request.args.get('eid')
    vid = request.args.get('vid')
    tid = request.args.get('tid')
    rid = request.args.get('rid')
    
    act = request.args.get('act')
        
    
    mycursor = mydb.cursor()

    mycursor.execute('SELECT * FROM register where id=%s',(vid,))
    rw = mycursor.fetchone()                  
    return render_template('process1.html',msg=msg,vid=vid,tid=tid,rid=rid,eid=eid,st=st)
@app.route('/process2',methods=['POST','GET'])
def process2():
    msg=""
    ss=""
    uname=""
    act=""
    st=""
    ss=""
    eid = request.args.get('eid')
    vid = request.args.get('vid')
    tid = request.args.get('tid')
    rid = request.args.get('rid')
    act = request.args.get('act') 
    ff3=open("img.txt","r")
    mcnt=ff3.read()
    ff3.close()
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM register where id=%s',(vid,))
    rw = mycursor.fetchone()                 
    try:
        cutoff=5
        act="1"
        mycursor.execute('SELECT * FROM vt_face where vid=%s',(vid,))
        dt = mycursor.fetchall()
        for rr in dt:
            hash0 = imagehash.average_hash(Image.open("static/frame/"+rr[2])) 
            hash1 = imagehash.average_hash(Image.open("faces/f1.jpg"))
            cc1=hash0 - hash1
            print("cc="+str(cc1))
            if cc1<=cutoff:
                vid=rr[1]
                ss="yes"
                msg="ok"
                mycursor.execute("update store_entry set face_st=1 where id=%s",(eid,))
                mydb.commit()
                break
        if ss=="yes":
            msg="ok"
        else:
            msg="fail"
    except:
        print("try")

    return render_template('process2.html',msg=msg,vid=vid,tid=tid,rid=rid,eid=eid,st=st)
@app.route('/monitor',methods=['POST','GET'])
def monitor():
    ff=open("sms.txt","w")
    ff.write("1")
    ff.close()
    return render_template('monitor.html')
@app.route('/process3',methods=['POST','GET'])
def process3():
    msg=""
    st=""
    mess=""
    mobile=""
    sms_st=""
    ff=open("people.txt","r")
    pc=ff.read()
    ff.close()

    ff=open("sms.txt","r")
    sms1=ff.read()
    ff.close()
    sms=int(sms1)
    num=int(pc)
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM booking order by id desc limit 0,1")
    rw = mycursor.fetchone()
    tid=rw[2]
    now = date.today() #datetime.datetime.now()
    rdate=now.strftime("%d-%m-%Y")
    mycursor.execute("SELECT * FROM admin where utype='ttr'")
    dd2 = mycursor.fetchone()
    mobile=dd2[3]
    mycursor.execute("SELECT count(*) FROM store_entry where face_st=1 && rdate=%s && tid=%s",(rdate,tid))
    cnt = mycursor.fetchone()[0]
    ucnt=str(cnt)
    if num>cnt:
        st="1"
        sm=sms+1
        if sms<=3:
            sms_st="1"
            mess="Passenger limit over"
        ff=open("sms.txt","w")
        ff.write(str(sm))
        ff.close()
            
        
                                    
            
    return render_template('process3.html',pc=pc,ucnt=ucnt,st=st,sms_st=sms_st,mess=mess,mobile=mobile)
    
@app.route('/page1',methods=['POST','GET'])
def page1():

    return render_template('page1.html')




@app.route('/admin',methods=['POST','GET'])
def admin():
    msg=""
    act=request.args.get("act")
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    mycursor = mydb.cursor()
    if request.method=='POST':
        
        name=request.form['name']
        gender=request.form['gender']
        dob=request.form['dob']
        mobile=request.form['mobile']
        email=request.form['email']
        address=request.form['address']
        city=request.form['city']
        aadhar=request.form['aadhar']
        
        mycursor.execute("SELECT count(*) FROM register where aadhar=%s",(aadhar,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
            mycursor.execute("SELECT max(id)+1 FROM register")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            
            sql = "INSERT INTO register(id,name,gender,dob,mobile,email,address,city,aadhar,rdate) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,name,gender,dob,mobile,email,address,city,aadhar,rdate)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()
            
            return redirect(url_for('add_photo',vid=maxid))
        else:
            msg="fail"
        
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from vt_face where vid=%s",(did,))
        mydb.commit()
        mycursor.execute("delete from register where id=%s",(did,))
        mydb.commit()
        return redirect(url_for('admin'))
        
        
    mycursor.execute("SELECT * FROM register")
    data = mycursor.fetchall()
    
    return render_template('admin.html',msg=msg,data=data)

@app.route('/home_rw',methods=['POST','GET'])
def home_rw():
    msg=""
    act=request.args.get("act")

    mycursor = mydb.cursor()
    if request.method=='POST':
        
        train=request.form['train']
        train_no=request.form['train_no']
        splace=request.form['splace']
        dplace=request.form['dplace']
        route=request.form['route']
        arrival=request.form['arrival']
        departure=request.form['departure']
        cost=request.form['cost']
        
        mycursor.execute("SELECT count(*) FROM train where train_no=%s",(train_no,))
        myresult = mycursor.fetchone()[0]

        if myresult==0:
            mycursor.execute("SELECT max(id)+1 FROM train")
            maxid = mycursor.fetchone()[0]
            if maxid is None:
                maxid=1

            now = date.today() #datetime.datetime.now()
            rdate=now.strftime("%d-%m-%Y")
            
            
            sql = "INSERT INTO train(id,train,train_no,splace,dplace,route,arrival,departure,cost) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            val = (maxid,train,train_no,splace,dplace,route,arrival,departure,cost)
            print(sql)
            mycursor.execute(sql, val)
            mydb.commit()
            msg="success"
        else:
            msg="fail"
        
    if act=="del":
        did=request.args.get("did")
        mycursor.execute("delete from train where id=%s",(did,))
        mydb.commit()

        return redirect(url_for('home_rw'))
        
        
    mycursor.execute("SELECT * FROM train")
    data = mycursor.fetchall()
    
    return render_template('home_rw.html',msg=msg,data=data,act=act)




@app.route('/add_photo',methods=['POST','GET'])
def add_photo():
    vid=""
    ff1=open("photo.txt","w")
    ff1.write("2")
    ff1.close()

    #ff2=open("mask.txt","w")
    #ff2.write("face")
    #ff2.close()
    act = request.args.get('act')
    
    if request.method=='GET':
        vid = request.args.get('vid')
        ff=open("user.txt","w")
        ff.write(str(vid))
        ff.close()

    cursor = mydb.cursor()
    
    if request.method=='POST':
        vid=request.form['vid']
        fimg="v"+vid+".jpg"
        

        cursor.execute('delete from vt_face WHERE vid = %s', (vid, ))
        mydb.commit()

        ff=open("det.txt","r")
        v=ff.read()
        ff.close()
        vv=int(v)
        v1=vv-1
        vface1=vid+"_"+str(v1)+".jpg"
        i=2
        while i<vv:
            
            cursor.execute("SELECT max(id)+1 FROM vt_face")
            maxid = cursor.fetchone()[0]
            if maxid is None:
                maxid=1
            vface=vid+"_"+str(i)+".jpg"
            sql = "INSERT INTO vt_face(id, vid, vface) VALUES (%s, %s, %s)"
            val = (maxid, vid, vface)
            print(val)
            cursor.execute(sql,val)
            mydb.commit()
            i+=1

        
        return redirect(url_for('view_photo',vid=vid,act='success'))
        
    
    cursor.execute("SELECT * FROM register")
    data = cursor.fetchall()
    return render_template('add_photo.html',data=data, vid=vid)




def kmeans_color_quantization(image, clusters=8, rounds=1):
    h, w = image.shape[:2]
    samples = np.zeros([h*w,3], dtype=np.float32)
    count = 0

    for x in range(h):
        for y in range(w):
            samples[count] = image[x][y]
            count += 1

    compactness, labels, centers = cv2.kmeans(samples,
            clusters, 
            None,
            (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10000, 0.0001), 
            rounds, 
            cv2.KMEANS_RANDOM_CENTERS)

    centers = np.uint8(centers)
    res = centers[labels.flatten()]
    return res.reshape((image.shape))


###Preprocessing
@app.route('/view_photo',methods=['POST','GET'])
def view_photo():
    ff1=open("photo.txt","w")
    ff1.write("1")
    ff1.close()
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()

    if request.method=='POST':
        print("Training")
        vid=request.form['vid']
        cursor = mydb.cursor()
        cursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        dt = cursor.fetchall()
        for rs in dt:
            ##Preprocess
            path="static/frame/"+rs[2]
            path2="static/process1/"+rs[2]
            mm2 = PIL.Image.open(path).convert('L')
            rz = mm2.resize((200,200), PIL.Image.ANTIALIAS)
            rz.save(path2)
            
            '''img = cv2.imread(path2) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            path3="static/process2/"+rs[2]
            cv2.imwrite(path3, dst)'''
            #noice
            img = cv2.imread('static/process1/'+rs[2]) 
            dst = cv2.fastNlMeansDenoisingColored(img, None, 10, 10, 7, 15)
            fname2='ns_'+rs[2]
            cv2.imwrite("static/process1/"+fname2, dst)
            ######
            ##bin
            image = cv2.imread('static/process1/'+rs[2])
            original = image.copy()
            kmeans = kmeans_color_quantization(image, clusters=4)

            # Convert to grayscale, Gaussian blur, adaptive threshold
            gray = cv2.cvtColor(kmeans, cv2.COLOR_BGR2GRAY)
            blur = cv2.GaussianBlur(gray, (3,3), 0)
            thresh = cv2.adaptiveThreshold(blur,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV,21,2)

            # Draw largest enclosing circle onto a mask
            mask = np.zeros(original.shape[:2], dtype=np.uint8)
            cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = cnts[0] if len(cnts) == 2 else cnts[1]
            cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
            for c in cnts:
                ((x, y), r) = cv2.minEnclosingCircle(c)
                cv2.circle(image, (int(x), int(y)), int(r), (36, 255, 12), 2)
                cv2.circle(mask, (int(x), int(y)), int(r), 255, -1)
                break
            
            # Bitwise-and for result
            result = cv2.bitwise_and(original, original, mask=mask)
            result[mask==0] = (0,0,0)

            
            ###cv2.imshow('thresh', thresh)
            ###cv2.imshow('result', result)
            ###cv2.imshow('mask', mask)
            ###cv2.imshow('kmeans', kmeans)
            ###cv2.imshow('image', image)
            ###cv2.waitKey()

            cv2.imwrite("static/process1/bin_"+rs[2], thresh)
            

            ###RPN - Segment
            img = cv2.imread('static/process1/'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            ####
            img = cv2.imread('static/process2/fg_'+rs[2])
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/fg_"+rs[2]
            segment.save(path3)
            '''
            img = cv2.imread(path2)
            gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
            ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

            # noise removal
            kernel = np.ones((3,3),np.uint8)
            opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)

            # sure background area
            sure_bg = cv2.dilate(opening,kernel,iterations=3)

            # Finding sure foreground area
            dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
            ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)

            # Finding unknown region
            sure_fg = np.uint8(sure_fg)
            segment = cv2.subtract(sure_bg,sure_fg)
            img = Image.fromarray(img)
            segment = Image.fromarray(segment)
            path3="static/process2/"+rs[2]
            segment.save(path3)
            '''
            #####
            image = cv2.imread(path2)
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            edged = cv2.Canny(gray, 50, 100)
            image = Image.fromarray(image)
            edged = Image.fromarray(edged)
            path4="static/process3/"+rs[2]
            edged.save(path4)
            ##
            #shutil.copy('static/assets/images/11.png', 'static/process4/'+rs[2])
       
        return redirect(url_for('view_photo1',vid=vid))
        
    return render_template('view_photo.html', result=value,vid=vid)

###
def crfrnn_segmenter(model_def_file, model_file, gpu_device, inputs):
    
    assert os.path.isfile(model_def_file), "File {} is missing".format(model_def_file)
    assert os.path.isfile(model_file), ("File {} is missing. Please download it using "
                                        "./download_trained_model.sh").format(model_file)

    if gpu_device >= 0:
        caffe.set_device(gpu_device)
        caffe.set_mode_gpu()
    else:
        caffe.set_mode_cpu()

    net = caffe.Net(model_def_file, model_file, caffe.TEST)

    num_images = len(inputs)
    num_channels = inputs[0].shape[2]
    assert num_channels == 3, "Unexpected channel count. A 3-channel RGB image is exptected."
    
    caffe_in = np.zeros((num_images, num_channels, _MAX_DIM, _MAX_DIM), dtype=np.float32)
    for ix, in_ in enumerate(inputs):
        caffe_in[ix] = in_.transpose((2, 0, 1))

    start_time = time.time()
    out = net.forward_all(**{net.inputs[0]: caffe_in})
    end_time = time.time()

    print("Time taken to run the network: {:.4f} seconds".format(end_time - start_time))
    predictions = out[net.outputs[0]]

    return predictions[0].argmax(axis=0).astype(np.uint8)


def run_crfrnn(input_file, output_file, gpu_device):
    """ Runs the CRF-RNN segmentation on the given RGB image and saves the segmentation mask.
    Args:
        input_file: Input RGB image file (e.g. in JPEG format)
        output_file: Path to save the resulting segmentation in PNG format
        gpu_device: ID of the GPU device. If using the CPU, set this to -1
    """

    input_image = 255 * caffe.io.load_image(input_file)
    input_image = resize_image(input_image)

    image = PILImage.fromarray(np.uint8(input_image))
    image = np.array(image)

    palette = get_palette(256)
    #PIL reads image in the form of RGB, while cv2 reads image in the form of BGR, mean_vec = [R,G,B] 
    mean_vec = np.array([123.68, 116.779, 103.939], dtype=np.float32)
    mean_vec = mean_vec.reshape(1, 1, 3)

    # Rearrange channels to form BGR
    im = image[:, :, ::-1]
    # Subtract mean
    im = im - mean_vec

    # Pad as necessary
    cur_h, cur_w, cur_c = im.shape
    pad_h = _MAX_DIM - cur_h
    pad_w = _MAX_DIM - cur_w
    im = np.pad(im, pad_width=((0, pad_h), (0, pad_w), (0, 0)), mode='constant', constant_values=0)

    # Get predictions
    segmentation = crfrnn_segmenter(_MODEL_DEF_FILE, _MODEL_FILE, gpu_device, [im])
    segmentation = segmentation[0:cur_h, 0:cur_w]

    output_im = PILImage.fromarray(segmentation)
    output_im.putpalette(palette)
    output_im.save(output_file)
###CNN Classification
def CNN(self):
        
        train_data_preprocess = ImageDataGenerator(
                rescale = 1./255,
                shear_range = 0.2,
                zoom_range = 0.2,
                horizontal_flip = True)

        test_data_preprocess = (1./255)

        train = train_data_preprocess.flow_from_directory(
                'dataset/training',
                target_size = (128,128),
                batch_size = 32,
                class_mode = 'binary')

        test = train_data_preprocess.flow_from_directory(
                'dataset/test',
                target_size = (128,128),
                batch_size = 32,
                class_mode = 'binary')

        ## Initialize the Convolutional Neural Net

        # Initialising the CNN
        cnn = Sequential()

        # Step 1 - Convolution
        # Step 2 - Pooling
        cnn.add(Conv2D(32, (3, 3), input_shape = (128, 128, 3), activation = 'relu'))
        cnn.add(MaxPooling2D(pool_size = (2, 2)))

        # Adding a second convolutional layer
        cnn.add(Conv2D(32, (3, 3), activation = 'relu'))
        cnn.add(MaxPooling2D(pool_size = (2, 2)))

        # Step 3 - Flattening
        cnn.add(Flatten())

        # Step 4 - Full connection
        cnn.add(Dense(units = 128, activation = 'relu'))
        cnn.add(Dense(units = 1, activation = 'sigmoid'))

        # Compiling the CNN
        cnn.compile(optimizer = 'adam', loss = 'binary_crossentropy', metrics = ['accuracy'])

        history = cnn.fit_generator(train,
                                 steps_per_epoch = 250,
                                 epochs = 25,
                                 validation_data = test,
                                 validation_steps = 2000)

        plt.plot(history.history['acc'])
        plt.plot(history.history['val_acc'])
        plt.title('Model Accuracy')
        plt.ylabel('accuracy')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        plt.plot(history.history['loss'])
        plt.plot(history.history['val_loss'])
        plt.title('Model Loss')
        plt.ylabel('loss')
        plt.xlabel('epoch')
        plt.legend(['train', 'test'], loc='upper left')
        plt.show()

        test_image = image.load_img('\\dataset\\', target_size=(128,128))
        test_image = image.img_to_array(test_image)
        test_image = np.expand_dims(test_image, axis=0)
        result = cnn.predict(test_image)
        print(result)

        if result[0][0] == 1:
                print('feature extracted and classified')
        else:
                print('none')
                
@app.route('/view_photo1',methods=['POST','GET'])
def view_photo1():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo1.html', result=value,vid=vid)

@app.route('/view_photo11',methods=['POST','GET'])
def view_photo11():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo11.html', result=value,vid=vid)

@app.route('/view_photo2',methods=['POST','GET'])
def view_photo2():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo2.html', result=value,vid=vid)    

@app.route('/view_photo3',methods=['POST','GET'])
def view_photo3():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo3.html', result=value,vid=vid)

@app.route('/view_photo4',methods=['POST','GET'])
def view_photo4():
    vid=""
    value=[]
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT * FROM vt_face where vid=%s",(vid, ))
        value = mycursor.fetchall()
    return render_template('view_photo4.html', result=value,vid=vid)

@app.route('/message',methods=['POST','GET'])
def message():
    vid=""
    name=""
    if request.method=='GET':
        vid = request.args.get('vid')
        mycursor = mydb.cursor()
        mycursor.execute("SELECT name FROM register where id=%s",(vid, ))
        name = mycursor.fetchone()[0]
    return render_template('message.html',vid=vid,name=name)


@app.route('/home_ttr',methods=['POST','GET'])
def home_ttr():
    msg=""
    act=request.args.get("act")
    mycursor = mydb.cursor()
   
        
        
    mycursor.execute("SELECT * FROM train")
    data = mycursor.fetchall()
    
    return render_template('home_ttr.html',msg=msg,data=data,act=act)

@app.route('/view_book1',methods=['POST','GET'])
def view_book1():
    msg=""
    act=request.args.get("act")
    tid=request.args.get("tid")
    mycursor = mydb.cursor()
   
        
        
    mycursor.execute("SELECT * FROM booking where tid=%s",(tid,))
    data = mycursor.fetchall()
    
    return render_template('view_book1.html',msg=msg,data=data,act=act)

@app.route('/view_book',methods=['POST','GET'])
def view_book():
    msg=""
    act=request.args.get("act")
    tid=request.args.get("tid")
    mycursor = mydb.cursor()
   
        
        
    mycursor.execute("SELECT * FROM booking where tid=%s",(tid,))
    data = mycursor.fetchall()
    
    return render_template('view_book.html',msg=msg,data=data,act=act)



@app.route('/logout')
def logout():
    # remove the username from the session if it is there
    #session.pop('username', None)
    return redirect(url_for('index'))
#########################
def gen2(PersonCount):
    while True:
        frame = PersonCount.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/video_feed2')
def video_feed2():
    return Response(gen2(VideoCamera2()), mimetype='multipart/x-mixed-replace; boundary=frame')
########################
def gen3(camera2):
    while True:
        frame = camera2.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/video_feed3')
def video_feed3():
    return Response(gen3(VideoCamera3()), mimetype='multipart/x-mixed-replace; boundary=frame')



#########################
def gen(camera):
    
    while True:
        frame = camera.get_frame()
        
        
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
################
@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
