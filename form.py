from flask_wtf import Form
from wtforms import TextField, PasswordField, validators, TextAreaField
from wtforms.validators import DataRequired, Length, ValidationError,email, equal_to
from flask import request

class LoginForm(Form):
    PUBLIC_KEY = '6Ld90hMTAAAAAHMuWMHuxFV6OQJp224JtCgoXoyB'
    SECRET_KEY = '6Ld90hMTAAAAAG8MptdY7u9hnZYACLY4Jhz5n3nZ'

    username = TextField("username",  [validators.Required("Please enter your name.")])
    password = PasswordField("Password", [validators.Required("Please enter password.")])



class Signupform(Form):
    fname = TextField("fname",  [validators.Required("name required"),Length(min=4,max=20)])
    lname = TextField("lname",  [validators.Required("name required"),Length(min=2,max=20)])
    uname = TextField("uname",  [validators.Required("Please enter username."),Length(min=5,max=20)])
    email = TextField("email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField("password", [validators.Required("Please enter password."),Length(min=6)])
    repassword = PasswordField("repassword", [validators.Required("Please enter password."),validators.EqualTo('password','password must match')])
    address = TextAreaField("address", [validators.Required("Please enter your address.")])

class Addpost(Form):
    body = TextAreaField("body", [validators.Required("post must not empty")])