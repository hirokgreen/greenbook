from flask import Flask, render_template, request, redirect, flash, session, url_for
from functools import wraps
from pass_hash import Hssh
from form import LoginForm, Signupform, Addpost
from sqlalchemy import *
from models import *
import textwrap
#from db_create import *
from datetime import datetime, timedelta
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
        if 'logged_in' in session:
            return test(*args, **kwargs)
        else:
            flash('you need to login first')
            return redirect('log')
    return wrap    

@app.route("/hello")
@login_required
def hello():
    form = Addpost()
    id = session['auth']
    table = Table(id, metadata, autoload=True)
    rs = table.select().order_by(table.c.id.desc()).execute()
    time = datetime.now()
    return render_template('hello.html', posts = rs,id =id,form=form,time=time)


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

            return  mon + ' '+str(t2.day) + ', '+ str(t2.year)
    return dict(interval=interval)


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


@app.route("/about")
def about():
    return render_template('about.html')


@app.route("/logout")
def logout():
    session.pop('logged_in',None)
    session.pop('name',None)
    flash('You are logged out')
    return redirect('log')

@app.route("/register",methods=['GET', 'POST'])
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


@app.route("/log",methods=['GET', 'POST'])
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
                 session['name'] = name
                 author = 'green'+str(id)
                 session['auth'] = author
                 flash('you are successfully logged in as '+ name)
                 return  redirect(url_for('hello',member = author))    #send id to the 'hello'
             else:
                 flash('username or password is incorrect')
                 return render_template('log.html',form=form)

           else:
               flash('username or password is incorrect')
               return render_template('log.html',form=form)

    return render_template('log.html', form=form)

@app.route("/form")
def get():
    return render_template('form.html')

if __name__ == "__main__":
    app.run()

