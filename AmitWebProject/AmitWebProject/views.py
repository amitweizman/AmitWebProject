"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template
from AmitWebProject import app
from AmitWebProject.Models.LocalDatabaseRoutines import create_LocalDatabaseServiceRoutines


from datetime import datetime
from flask import render_template, redirect, request

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

import json 
import requests

import io
import base64

from os import path

from flask   import Flask, render_template, flash, request
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from AmitWebProject.Models.QueryFormStracture import QueryFormStructure 
from AmitWebProject.Models.QueryFormStracture import LoginFormStructure
from AmitWebProject.Models.QueryFormStracture import UserRegistrationFormStructure 

##from RoyWebProject2_alternative.Models.LocalDatabaseRoutines import IsUserExist, IsLoginGood, AddNewUser

db_Functions = create_LocalDatabaseServiceRoutines() 

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )


@app.route('/register', methods=['GET', 'POST'])
def Register():
    form = UserRegistrationFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (not db_Functions.IsUserExist(form.username.data)):
            db_Functions.AddNewUser(form)
            db_table = ""

            flash('Thanks for registering new user - '+ form.FirstName.data + " " + form.LastName.data )
            # Here you should put what to do (or were to go) if registration was good
        else:
            flash('Error: User with this Username already exist ! - '+ form.username.data)
            form = UserRegistrationFormStructure(request.form)

    return render_template(
        'register.html', 
        form=form, 
        title='Register New User',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/login', methods=['GET', 'POST'])
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

@app.route('/data')
def data():
    """Renders the about page."""
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='My Data'
    )

df = pd.read_csv("C:\\Users\\royma\\source\\repos\\AmitWebProject\\AmitWebProject\\AmitWebProject\\static\\data\\dataset - apps on google play.csv")
@app.route  ('/dataSet')
def dataSet():
    """Renders the about page."""
    return render_template(
        'dataSet.html',
        title='dataSet',
        year=datetime.now().year,
        message='My Data Set', data = df.to_html(classes = "table table-hover")
    )