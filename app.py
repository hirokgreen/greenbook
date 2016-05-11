from flask import Flask, render_template, request, redirect, flash, session, url_for, Session, Response, make_response
from functools import wraps
from pass_hash import Hssh
from form import LoginForm, Signupform, Addpost
from models import *
import json
import  Cookie
from datetime import datetime, timedelta
import re
from werkzeug import secure_filename
import os
from sqlalchemy import *
from chat import *

UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

app = Flask(__name__)
app.secret_key='hirok'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route("/",methods=['GET', 'POST'])
def log():
    if 'logged_in' in session:
        return  redirect(url_for('hello'))
    if request.cookies.get('auth') is not None:
        session['logged_in']=True
        session['auth']=request.cookies.get('auth')
        return  redirect(url_for('hello'))
    else:
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
                     if request.form.get("remember")=='1':
                         rsp = make_response(redirect(url_for('hello')))
                         rsp.set_cookie('auth',session['auth'],expires=datetime.now()+timedelta(days=10))
                         return  rsp
                     flash('you are successfully logged in')
                     return redirect(url_for('hello'))

                 else:
                     flash('username or password is incorrect')
                     return render_template('log.html',form=form)

               else:
                   flash('username or password is incorrect')
                   return render_template('log.html',form=form)

        return render_template('log.html', form=form)



def login_required(test):
    @wraps(test)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return test(*args, **kwargs)
        if request.cookies.get('auth') is not None:
            session['logged_in']=True
            session['auth']=request.cookies.get('auth')
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
    c_id = int(id.replace("green", ""))
    table = Table('users', metadata, autoload=True)
    usr = select([table.c.uname],table.c.id==c_id).execute()
    for row in usr:
        session['name']=str(row[0])

    table = Table(id, metadata, autoload=True)
    rs = table.select().order_by(table.c.id.desc()).execute()
    time = datetime.now()



    return render_template('hello.html', posts = rs,form=form,time=time,chat=c_id)

@app.route("/main/")
@login_required
def main():
    return render_template('main.html')

@app.route("/add_post/",methods=['GET', 'POST'])
@login_required
def add_post():
    if request.method == 'POST':
        try:
            post = Table(session['auth'], metadata, autoload=True)
            post.insert().execute({'description':request.form['body'],'date_time':datetime.now()})
        except:
            flash('something goes wrong....')
    return redirect('hello')

@app.route("/add_pic/",methods=['GET', 'POST'])
@login_required
def add_pic():
    if request.method == 'POST' and 'file' in request.files:
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return redirect('hello')
@app.route("/post_delete/<int:id>")
@login_required
def post_delete(id):
    table = Table(session['auth'], metadata, autoload=True)
    lc_id = str(session['auth'])+'_'+str(id)
    like = Table('like', metadata, autoload=True)
    comment = Table('comment', metadata, autoload=True)
    like.delete(like.c.post_id==lc_id).execute()
    comment.delete(comment.c.post_id==lc_id).execute()
    table.delete(table.c.id == id).execute()
    return redirect('hello')

@app.route("/post_update/<int:id>", methods=['GET', 'POST'])
@login_required
def post_update(id):
    if request.form['body']!="":
        table = Table(session['auth'], metadata, autoload=True)
        table.update(table.c.id == id , values=({'description':request.form['body']}) ).execute()
    return redirect('hello')

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

@app.route("/chat/<con>/<con2>",methods=['GET', 'POST','REQUEST'])
@login_required
def chat(con,con2):
    jsn = [{ "frnd":"" , "self":"" }]
    id = int(session['auth'].replace("green", ""))
    table1 = Table(con, metadata, autoload=False)
    table2 = Table(con2, metadata, autoload=False)
    if not table1.exists() and not table2.exists():
            c = Chat(con)
            c.chat().create()
    if table1.exists():
        chat = Chat_view('t1',con,jsn)
        text = json.dumps(chat.view())
    else:
        chat = Chat_view('t2',con2,jsn)
        text = json.dumps(chat.view())
    return text

@app.route("/chat_add/<t>/<id>",methods=['GET', 'POST','REQUEST'])
@login_required
def chat_add(t,id):
    f = 'green'+str(id.replace("frndchat", ""))
    me = session['auth']
    con = me+'_'+f
    con2 = f+'_'+me
    jsn = [{ "frnd":"" , "self":"" }]
    chat = Chat_Add(t,con,con2,jsn)
    text = json.dumps(chat.add())

    return  text

@app.route("/like_add/<post_id>/")
@login_required
def like_add(post_id):
    like = Table('like', metadata, autoload=True)
    like.insert().execute({'post_id':post_id,'user_id':session['auth']})
    return redirect(url_for('like',post_id=post_id))

@app.route("/like_delete/<post_id>/")
@login_required
def like_delete(post_id):
    like = Table('like', metadata, autoload=True)
    s = select([like.c.id]).where(like.c.post_id==post_id).where(like.c.user_id==session['auth']).execute()
    for row in s:
        like.delete(like.c.id==row[0]).execute()
    return redirect(url_for('like',post_id=post_id))

@app.route("/like/<post_id>/")
@login_required
def like(post_id):
    table = Table('like', metadata, autoload=True)
    liker = Table('users', metadata, autoload=True)
    rs = select([table.c.user_id],table.c.post_id==post_id).order_by(table.c.id.desc()).execute()
    r = []
    type = 'unliked'
    you = ''
    comma=''
    is_like=''
    for i in rs:
        if i[0]==session['auth']:
            type = 'like'
        id = int(i[0].replace("green", ""))
        name = select([liker.c.id],liker.c.id==id).execute()
        for n in name:
            r.append(n[0])
    if type=="like":
        you='you'
    c = len(r)
    if c>=2:
        comma = 'true'
    if c>=1:
        is_like = 'true'

    current_id = int(session['auth'].replace("green", ""))

    return render_template('like.html',user=r,user_id=rs,type=type,post_id=post_id,you=you,c_i=current_id,comma=comma,is_like=is_like)

@app.route("/comment/<post_id>/")
def comment(post_id):
    time = datetime.now()
    table = Table('comment', metadata, autoload=True)
    rs = table.select(table.c.post_id==post_id).order_by(table.c.id.asc()).execute()

    return render_template('comment.html',rs=rs,post_id=post_id,time=time)


@app.route("/add_comment",methods=['GET', 'POST'])
@login_required
def add_comment():
    if request.method == 'POST':
        try:
            p_id = request.form['p_id']
            table = Table('comment', metadata, autoload=True)
            table.insert().execute({'post_id':p_id,'comment':request.form['body'],'user_id':session['auth'],'date_time':datetime.now()})
        except:
            flash('kk')
    p_id = request.form['p_id']
    return redirect(url_for('comment',post_id=p_id))

@app.route("/comment_delete/<c_id>/<post_id>")
@login_required
def comment_delete(c_id,post_id):
    comment = Table('comment', metadata, autoload=True)
    comment.delete(comment.c.id==c_id).execute()
    return redirect(url_for('comment',post_id=post_id))


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
    def offlinetime(t1, t2):
        s1 = int(t1.second)
        m1 = int(t1.minute)
        h1 = int(t1.hour)
        d1 = int(t1.day)
        mo1 = int(t1.month)
        s2 = int(t2.second)
        m2 = int(t2.minute)
        h2 = int(t2.hour)
        d2 = int(t2.day)
        mo2 = int(t2.month)

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
        if d2 > d1:
            mo1 = mo1 - 1
            d1 = d1 + 30
        days = d1 - d2
        if days==0 and hours==0 and minutes==0:
            return '1m'
        if days==0 and hours==0 and minutes!=0:
            return str(minutes) + 'm'
        if days==0 and hours!=0:
            return str(hours) + 'h'
        if days!=0:
            return str(days) + 'd'
        else:
            return ''
    def name(id):
        user = Table('users', metadata, autoload=True)
        name = select([user.c.uname],user.c.id==id).execute()
        for row in name:
            liker = row[0]
        return liker
    def commenter(id):
        uid = id.replace("green", "")
        user = Table('users', metadata, autoload=True)
        name = select([user.c.uname],user.c.id==uid).execute()
        for row in name:
            commenter = row[0]
        return commenter
    def ajax(t1,t2):
        return t1
    def status(id,type):
        uid = int(session['auth'].replace("green", ""))
        table = Table('users', metadata, autoload=True)
        if type=='on':
            us = table.select(table.c.time_last_active >= (datetime.now() - timedelta(seconds=6))).execute()

        if type=='off':
            us = table.select(table.c.time_last_active <= (datetime.now() - timedelta(seconds=6))).execute()

        return us
    def online(id):
        uid = id.replace("green", "")
        table = Table('users', metadata, autoload=True)
        table.update(table.c.id == uid , values=({'time_last_active':datetime.now()}) ).execute()

    def getid():
        id  = session['auth'].replace("green", "")

        return id

    return dict(interval=interval,name=name,commenter=commenter,ajax=ajax,status=status,online=online,getid=getid,offlinetime=offlinetime)

@app.context_processor
def utility_processor():
    def url(s):
        r = re.compile(r"(http[s]://[^ ]+)")
        rm = r.sub(r'<a href="\1">\1</a>', s)

        return rm
    return dict(url=url)





@app.route("/about/")
def about():
    return render_template('about.html')


@app.route("/logout")
def logout():
    session.pop('logged_in',None)
    id = session['auth'].replace("green", "")
    #session.pop('name',None)
    rsp = make_response(redirect(''))
    rsp.delete_cookie('auth')
    flash('You are successfully logged out')
    return  rsp


    #return redirect('')

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

             flash('you have successfully registered as  '+ form.uname.data)
             return  redirect('')
         else:
             flash('please fill up the form correctly')

     return render_template('register.html', form=form)



@app.route("/hello/<fid>/")
@app.route("/hello/<fid>/<pid>")
@login_required
def frnd_specefic_posts(fid,pid='Anonymous'):
    if fid==session['auth']:
        return redirect('hello')

    id = fid.replace("green", "")
    c_id = session['auth'].replace("green", "")
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
    return render_template('frnd_post.html', posts=rs, time=time,fr_id=fs,fid=fid,pid=pid,chat=c_id)

if __name__ == "__main__":
    app.run(debug=True)
