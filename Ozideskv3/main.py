# ----------- import statements  ------------
import sqlite3
from ast import Assign
from flask import Flask,flash, render_template, request, redirect, url_for
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
# from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

# ------------ app initialisation -------------------

app = Flask(__name__)


#-------------- Controllers ------------------------------
log= None
role=None
@app.route("/")
def index():
    return render_template('master.html')

@app.route("/contact", methods=["GET","POST"])
def contact():
    return render_template('contact.html')

@app.route("/contactsend", methods=["GET","POST"])
def contactsend():
    email = request.form['email']
    name = request.form['fname'] + " " + request.form['lname']
    reason = request.form['reason']
    message1 = request.form['message']
    sender_email = "dinnupatel100@gmail.com"
    sender_password = "yjjcmwdgwmvyotqw"

    # Receiver's email information
    receiver_email = email

    # Email content
    subject ="Query : " + name + " :  " + reason
    message = message1

    # Create a message object
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Add the message to the email body
    msg.attach(MIMEText(message, 'plain'))


    #Connect to the email server and send the email
    with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
        smtp.starttls()
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email, receiver_email, msg.as_string())

    return render_template('test.html')


@app.route("/about",methods=["GET","POST"])
def about():
    return render_template("about.html")

@app.route("/internships",methods=["GET","POST"])
def internships():
    return render_template("internships.html")

@app.route("/loginrender",methods=["GET","POST"])
def loginrender():
    return render_template('login.html')

@app.route("/hrmodule",methods=["GET","POST"])
def hrmodule():
    conn = sqlite3.connect('ozidesk.db')
    cursor = conn.cursor()
    cursor.execute("select * from login where status = 3 ")
    res = cursor.fetchall()
    print(res)
    roles = ['Apply','BA','DA','SO','RA']
    return render_template('hr.html',candidates=res, roles=roles)


@app.route("/login",methods=["GET","POST"])
def login():
    global log
    conn = sqlite3.connect('ozidesk.db')
    cursor = conn.cursor()
    email=request.form['email']
    password=request.form['password']
    cursor.execute("Select email, password from login")
    res = cursor.fetchall()
    #  f1=Login.query.all()
    for f in res:
    # f1=Login.query.all()
    # for f in f1:
        if f == (email , password ):
            cursor.execute("select login_id, role_id, status, type from login where email = '" + email + "'")
            res = cursor.fetchall()
            # print(res)
            type=res[0][3]
            print(type)
            if type==1:
                return redirect(url_for('hrmodule'))
            log = res[0][0]
            global role
            role = res[0][1]
            # conn.close()
            if res[0][2] == 0:
                return render_template('forapply.html')
            elif res[0][2] == 1:
                return redirect(url_for('form1'))
            elif res[0][2] == 2:
                return redirect(url_for('form2'))
            elif res[0][2] == 3:
                cursor.execute("select name from login where login_id ="+str(log))
                res=cursor.fetchall()
                name=res[0][0]
                return render_template('success.html',name=name)
            elif res[0][2] == 4:
                cursor.execute("select name from login where login_id ="+str(log))
                res=cursor.fetchall()
                name=res[0][0]
                return render_template('accept.html',name=name)
            else:
                cursor.execute("select name from login where login_id ="+str(log))
                res=cursor.fetchall()
                name=res[0][0]
                return render_template('reject.html',name=name)
    conn.close()
    return render_template('login_error.html')

@app.route("/registeration",methods=["GET","POST"])
def registration():
    return render_template('registration.html')

@app.route("/register",methods=["GET","POST"])
def register():
    conn = sqlite3.connect('ozidesk.db')
    cursor = conn.cursor()
    password = request.form['password']
    name = request.form['name']
    mobile = request.form['mobile']
    email = request.form['email']
    qualification = request.form['qualification']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    source = request.form['source']
    linkedin = request.form['linkedin']
    query = "insert into login (name, email, password, type, mobile, role_id) values('"+name +"','"+email+"','"+password+"',0,'"+mobile+"',0)"
    cursor.execute(query)
    conn.commit()
    cursor.execute("Select login_id from Login where email = '"+email+"'")
    res = cursor.fetchall()
    id = res[0]
    application = int(mobile[-4:])
    # query = "insert into intern_care values()"
    query = "insert into intern_care values ("+str(id[0])+","+str(application)+",'"+qualification+"','"+city+"','"+state+"','"+country+"','"+source+"','"+linkedin+"')"
    # print(query)
    cursor.execute(query)
    conn.commit()
    
    return render_template("login.html")

@app.route("/applypage",methods=["GET","POST"])
def applypage():
    return render_template("applypage.html")

@app.route("/form2",methods=["GET","POST"])
def form2():
    global log
   
    # answers = request.form['ozibook']
    roles = request.form['internship']
    # print(roles)
    global role
    
    conn = sqlite3.connect('ozidesk.db')
    cursor = conn.cursor()
    cursor.execute("select question_id,question from question where role__id=0")
    que = cursor.fetchall()
    cursor.execute("select role_id from role where role_name='"+roles+"'")
    res=cursor.fetchall()
    # print("Role",res)
    role=res[0][0]
    print(role)
    cursor.execute("update login set role_id = "+str(role)+" where login_id = "+str(log))
    # role=res[0][0]
    # query = "select application_id from intern_care where login_id = " + str(log)
    # # print(query)
    # cursor.execute(query)
    # res = cursor.fetchall()
    # appl = res[0][0]
    c=1
    for i in que:
        cursor.execute("insert into answer(login_id,question_id, answer) values("+str(log)+","+str(i[0])+",'"+request.form['ozibookf1q'+str(c)]+"')")
        c+=1
    # res=cursor.fetchall()
    conn.commit()
    cursor.execute("select * from question where role__id = "+str(role))
    res=cursor.fetchall()
    cursor.execute("update login set status = 2 where login_id = "+str(log))

    conn.close()
    # print(role)
    # print(res)
    return render_template("form2.html",questions=res)

@app.route("/success",methods=["GET","POST"])
def success():
    global log
   
    global role
    
    conn = sqlite3.connect('ozidesk.db')
    cursor = conn.cursor()
    cursor.execute("select question_id,question from question where role__id="+str(role))
    que = cursor.fetchall()
    dict_roles={1:'ba', 4:'ra'}
    code = dict_roles[role]
    c=1
    for i in que:
        cursor.execute("insert into answer(login_id,question_id, answer) values("+str(log)+","+str(i[0])+",'"+request.form['ozibook'+str(code)+'q'+str(c)]+"')")
        c+=1
    # res=cursor.fetchall()
    conn.commit()
    cursor.execute("update login set status = 3 where login_id = "+str(log))
    conn.commit()
    cursor.execute("select name from login where login_id = "+str(log))
    res = cursor.fetchall()
    name=res[0][0]
    conn.close()
    
    return render_template("success.html",name=name)

@app.route("/form1",methods=["GET","POST"])
def form1():
    global role
    conn = sqlite3.connect('ozidesk.db')
    cursor = conn.cursor()
    cursor.execute("select * from question where role__id = 0" )
    res=cursor.fetchall()
    cursor.execute("update login set status = 1 where login_id = "+str(log))
    # print(log)
    conn.commit()
    conn.close()
    # print(res)
    
    return render_template("form1.html",questions=res)


@app.route("/view",methods=["GET","POST"])
def view():
        id = request.args.get('id')
        conn = sqlite3.connect('ozidesk.db')
        cursor = conn.cursor()
        cursor.execute("select role_id from login where login_id = "+str(id))
        s = cursor.fetchall()
        rol = s[0][0]
        # cursor.execute("select * from question where role__id in (" + str(rol) + ", 0)" )
        ques = cursor.fetchall()
        cursor.execute("select * from answer where login_id="+str(id))
        ans = cursor.fetchall()
        items=[]
        for i in ans:
            a = i[1]
            q = i[2]
            cursor.execute("select question from question where question_id="+str(q))
            res = cursor.fetchall()
            items.append((res[0][0],a))
            # print(a)
            # for q in ques:
            #     print(q)
            #     if q[0] == a[2]:
            #         items.append((q[1],a))
                
        print(items)
        # print(ans)
        # print(ques)
        return render_template('view.html',items = items)
    
@app.route("/accept",methods=["GET","POST"])
def accept():
        id = request.args.get('id')
        conn = sqlite3.connect('ozidesk.db')
        cursor = conn.cursor()
        cursor.execute("update login set status=4 where login_id = "+ str(id))
        cursor.execute("select email from login where login_id = " + str(id))
        res = cursor.fetchall()
        email = res[0][0]

        conn.commit()
        conn.close()

        reason = "Ozibook"
        message1 = "HelloYou are Select, can join from 15th May"
        sender_email = "dinnupatel100@gmail.com"
        sender_password = "yjjcmwdgwmvyotqw"

        # Receiver's email information
        receiver_email = email

        # Email content
        subject =reason
        message = message1

        # Create a message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add the message to the email body
        msg.attach(MIMEText(message, 'plain'))


        #Connect to the email server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())

        return redirect(url_for('hrmodule'))

        
@app.route("/reject",methods=["GET","POST"])
def reject():
        id = request.args.get('id')
        conn = sqlite3.connect('ozidesk.db')
        cursor = conn.cursor()
        cursor.execute("update login set status=5 where login_id = "+ str(id))
        cursor.execute("select email from login where login_id = " + str(id))
        res = cursor.fetchall()
        email = res[0][0]
        conn.commit()
        conn.close()

        reason = "Ozibook"
        message1 = "Sorry, you are not selected"
        sender_email = "dinnupatel100@gmail.com"
        sender_password = "yjjcmwdgwmvyotqw"

        # Receiver's email information
        receiver_email = email

        # Email content
        subject =reason
        message = message1

        # Create a message object
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = receiver_email
        msg['Subject'] = subject

        # Add the message to the email body
        msg.attach(MIMEText(message, 'plain'))


        #Connect to the email server and send the email
        with smtplib.SMTP('smtp.gmail.com', 587) as smtp:
            smtp.starttls()
            smtp.login(sender_email, sender_password)
            smtp.sendmail(sender_email, receiver_email, msg.as_string())
        return redirect(url_for('hrmodule'))

    


#---------------- final application run ------------------

if __name__=="__main__":
    app.run(debug=True)
    # db.create_all()
    app.run(host='0.0.0.0',port=8080)    

