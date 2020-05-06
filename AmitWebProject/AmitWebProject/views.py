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


from flask   import Flask, render_template, flash, request,session
from wtforms import Form, BooleanField, StringField, PasswordField, validators
from wtforms import TextField, TextAreaField, SubmitField, SelectField, DateField
from wtforms import ValidationError

from AmitWebProject.Models.QueryFormStracture import QueryFormStructure 
from AmitWebProject.Models.QueryFormStracture import LoginFormStructure
from AmitWebProject.Models.QueryFormStracture import UserRegistrationFormStructure 
from AmitWebProject.Models.QueryFormStracture import QueryFormApplicationsStore


from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


db_Functions = create_LocalDatabaseServiceRoutines() 

#Home-Default page
@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )



#Registration Page
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
#Login View 
def Login():
    form = LoginFormStructure(request.form)

    if (request.method == 'POST' and form.validate()):
        if (db_Functions.IsLoginGood(form.username.data, form.password.data)):
            session['logged_in'] = True
            flash('Login approved!')
            #return redirect('<were to go if login is good!')
        else:
            session['logged_in'] = False
            flash('Error in - Username and/or password')
   
    return render_template(
        'login.html', 
        form=form, 
        title='Login to data analysis',
        year=datetime.now().year,
        repository_name='Pandas',
        )

#This is the about view
@app.route('/about')
def about():
    return render_template(
        'about.html',
        title='About the project',
        img_high= '/static/images/tichonet.png'
        )
#Contact View
@app.route('/contact')
def contact():
    return render_template(
        'contact.html',
        title='Contact the developer'
        )

#Data intro view
@app.route('/data')
def data():
    return render_template(
        'data.html',
        title='Data',
        year=datetime.now().year,
        message='My Data'
    )

df = pd.read_csv("C:\\Users\\User\Source\\Repos\\AmitWebProject\\AmitWebProject\\AmitWebProject\\static\\Data\\dataset - apps on google play.csv")

@app.route  ('/dataSet')
def dataSet():
    """Renders the about page."""
    return render_template(
        'dataSet.html',
        title='dataSet',
        year=datetime.now().year,
        message='My Data Set', data = df.to_html(classes = "table table-hover")
    )

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from AmitWebProject.Models.plot_service_functions import plot_to_img


#Remove the plus sign from the results of the database
def remove_plus(str):
    if '+' in str:
        x=str.index('+')
        return(str[:x])
    else:
        return(str)
#Query Page -Graph page
@app.route('/query' , methods = ['GET' , 'POST'])
def query():
    if (not 'logged_in' in session) or (session['logged_in'] == False):
        return redirect('/login')

    print("Query")
    df_app =  pd.read_csv(path.join(path.dirname(__file__), 'static/data/dataset - apps on google play.csv'))
    s_genres = df_app['Genres']
    l_genres = list(s_genres)
    l_genres = list(set(l_genres))
    m= list(zip(l_genres,l_genres))
    form1 = QueryFormApplicationsStore()
    form1.genres.choices = m
    chart = "/static/images/graph_temp.png"
    if request.method == 'POST':
        genres = form1.genres.data
        type = form1.types.data 
        df_app=df_app[['App', 'Rating', 'Installs', 'Genres', 'Type']]
        df_app =  df_app[df_app['Genres']==genres]
        df_app = df_app[df_app['Type']==type]
        df_app = df_app.drop('Genres',1)
        df_app = df_app.drop('Type',1)
        df_app['Rating']= df_app['Rating'].astype(float)
        df_app['Installs']=df_app['Installs'].apply(lambda x:remove_plus(x))
        df_app['Installs']=df_app['Installs'].apply(lambda x:x.replace(',',''))
        df_app['Installs']= df_app['Installs'].astype(int)
        df_app=df_app.sort_values('Installs',ascending=False)
        df_app=df_app.iloc[0:5]
        df_app=df_app.set_index('App')
        df_app['Installs']=df_app['Installs']/1000000
        fig = plt.figure()
        fig, ax = plt.subplots()
        df_app.plot('Rating', 'Installs', kind='scatter', ax=ax)
        for k, v in df_app.iterrows():
            ax.annotate(k, v)
        chart = plot_to_img(fig)

    return render_template(
      'query.html', 
      chart = chart,
     form1 = form1)
