from flask import Flask
from flask import Flask, render_template, Response, redirect, request, session, abort, url_for


app = Flask(__name__)
##session key
app.secret_key = 'abcdef'


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


if __name__ == "__main__":
    app.run(debug=True)
