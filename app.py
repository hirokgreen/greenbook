from flask import Flask, render_template, request, redirect, flash, session, url_for, Session, Response, make_response
from functools import wraps
from pass_hash import Hssh
from form import LoginForm, Signupform, Addpost
from sqlalchemy import *
from models import *
import json
import  Cookie
import textwrap
from datetime import datetime, timedelta
import re
app = Flask(__name__)
app.secret_key='hirok'
#def connect_db():
 #   return sqlite3.connect(app.config['DATABASE'])

@app.route("/")
def home():
        return render_template('home.html')

def welcome():
    return render_template('welcome.html')

def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if request.cookies.get('cookie_name') is not None:
           flash('cookie success')
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first')
            return redirect('')
    return wrap    

@app.route("/hello/")
@login_required
def hello():
    form = Addpost()
    id = session['auth']
    table = Table(id, metadata, autoload=True)
    rs = table.select().order_by(table.c.id.desc()).execute()
    time = datetime.now()
    print '<h2>Hello Word! This is my first CGI program</h2>'
    return render_template('hello.html', posts = rs,form=form,time=time)

@app.route("/search/<q>",methods=['GET', 'POST','REQUEST'])
@login_required
def search(q):
    s = q
    jsn = [{ "url":"" , "display":"" }]
    table = Table('users', metadata, autoload=True)
    rs = select([table.c.id,table.c.uname],table.c.uname.like('%'+s+'%')).execute()
    for item in rs:
        id = '/hello/green'+str(item.id)+'/'
        jsn.append({"url":id,"display":item.uname})
    jsn.append({"url":"#","display":"see more"})
    text = json.dumps(jsn)

    return  text

@app.route("/chat")
@login_required
def chat():
    id = session['auth']
    table = Table('users', metadata, autoload=True)
    us = select([table.c.id,table.c.uname],table.c.uname!=session['name']).execute()
    return render_template('chat.html',user=us)

@app.context_processor
def utility_processor():
    def interval(t1, t2):
        s1 = int(t1.second)
        m1 = int(t1.minute)
        h1 = int(t1.hour)
        d1 = int(t1.day)
        s2 = int(t2.second)
        m2 = int(t2.minute)
        h2 = int(t2.hour)
        d2 = int(t2.day)

        if s2 > s1:
            m1 = m1 - 1
            s1 = s1 + 60
        seconds = s1 - s2
        if m2 > m1:
            h1 = h1 - 1
            m1 = m1 + 60
        minutes = m1 - m2
        if h2 > h1:
            d1 = d1 - 1
            h1 = h1 + 24
        hours = h1 - h2
        days = d1 - d2
        if days==0 and hours==0 and minutes==0:
            return 'just now'
        if days==0 and hours==0 and minutes!=0:
            return str(minutes) + ' mins'
        if days==0 and hours!=0:
            return str(hours) + ' hrs'
        else:
            if t2.month==1:
                mon = 'January'
            if t2.month==2:
                mon = 'February'
            if t2.month==3:
                mon = 'March'
            if t2.month==4:
                mon = 'April'
            if t2.month==5:
                mon = 'May'
            if t2.month==6:
                mon = 'June'
            if t2.month==7:
                mon = 'July'
            if t2.month==8:
                mon = 'August'
            if t2.month==9:
                mon = 'September'
            if t2.month==10:
                mon = 'October'
            if t2.month==11:
                mon = 'November'
            if t2.month==12:
                mon = 'December'
            if h2<=12:
                h2 = h2
                type = 'am'
            if h2>12:
                h2 = h2-12
                type = 'pm'

            return  mon + ' '+str(t2.day) + ', '+ str(t2.year)+' at '+str(h2)+':'+str(m2)+type
    return dict(interval=interval)

@app.context_processor
def utility_processor():
    def url(s):
        r = re.compile(r"(http[s]://[^ ]+)")
        rm = r.sub(r'<a href="\1">\1</a>', s)

        return rm
    return dict(url=url)


@app.route("/add_post",methods=['GET', 'POST'])
@login_required
def add_post():
    form = Addpost()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Table(session['auth'], metadata, autoload=True)
            post.insert().execute({'description':form.body.data,'date_time':datetime.now()})
            return redirect('hello')

    return render_template('hello.html',form = form)

@app.route("/post_delete/<int:id>")
@login_required
def post_delete(id):
    table = Table(session['auth'], metadata, autoload=True)
    table.delete(table.c.id == id).execute()
    return redirect('hello')

@app.route("/post_update/<int:id>", methods=['GET', 'POST'])
@login_required
def post_update(id):
    table = Table(session['auth'], metadata, autoload=True)
    table.update(table.c.id == id , values=({'description':request.form['body']}) ).execute()
    return redirect('hello')


@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/logout")
def logout():
    session.pop('logged_in',None)
    session.pop('name',None)
    flash('You are logged out')
    return redirect('log')

@app.route("/register/",methods=['GET', 'POST'])
def register():
     form = Signupform()
     if request.method == 'POST':
         if form.validate_on_submit():
             obj = Hssh(form.password.data)
             password = obj.hashpassword()
             day = request.form['day']
             mon = request.form['mon']
             year = request.form['year']
             dob = day+'/'+mon+'/'+year
             user = Table('users', metadata, autoload=True)
             user.insert().execute({'uname':form.uname.data,'password':password,'fname':form.fname.data, 'lname':form.lname.data, 'email':form.email.data,
                                    'gender':request.form['gender'], 'address':form.address.data,'dob':dob})

             table = Table('users', metadata, autoload=True)
             rs = select([func.max(table.c.id)]).execute()
             for row in rs:
                 id = row[0]
             user_id = 'green'+str(id)
             #create post table
             post = PostTable()
             table = post.posttable(user_id)
             table.create()

             flash('successfully registered'+ user_id)
             return  redirect('')
         else:
             flash('please fill up the form correctly')

     return render_template('register.html', form=form)


@app.route("/log/",methods=['GET', 'POST'])
def log():
    form = LoginForm()
    name = None
    if request.method == 'POST':
        if form.validate_on_submit():
           obj = Hssh(form.password.data)
           table = Table('users', metadata, autoload=True)
           rs = select([table.c.id,table.c.uname,table.c.password],table.c.uname==form.username.data).execute()
           for row in rs:
              id = row[0]
              name = row[1]
              password = row[2]
           if name != None:
             if obj.chkpassword(password) is True:
                 session['logged_in'] = True
                 if request.form.get("remember")=='1':
                    rsp = Response()
                    rsp.set_cookie('cookie_name',value=name)

                 session['name'] = name
                 author = 'green'+str(id)
                 session['auth'] = author
                 flash('you are successfully logged in as '+ author)
                 return  redirect(url_for('hello'))
             else:
                 flash('username or password is incorrect')
                 return render_template('log.html',form=form)

           else:
               flash('username or password is incorrect')
               return render_template('log.html',form=form)

    return render_template('log.html', form=form)

@app.route("/hello/<fid>/")
@app.route("/hello/<fid>/<pid>")
@login_required
def frnd_specefic_posts(fid,pid='Anonymous'):
    if fid==session['auth']:
        return redirect('hello')

    id = fid.replace("green", "")
    frnd = Table('users', metadata, autoload=True)
    fr = select([frnd.c.uname],frnd.c.id==id).execute()
    for item in fr:
        fs = item.uname
    table = Table(fid, metadata, autoload=True)
    if pid!='Anonymous':
        rs = table.select(table.c.id==pid).execute()
    else:
        rs = table.select().order_by(table.c.id.desc()).execute()
    time = datetime.now()
    return render_template('frnd_post.html', posts=rs, time=time,fr_id=fs)

if __name__ == "__main__":
    app.run()

