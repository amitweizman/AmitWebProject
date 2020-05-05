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
from AmitWebProject.Models.QueryFormStracture import QueryFormApplicationsStore


from flask_bootstrap import Bootstrap
bootstrap = Bootstrap(app)


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

@app.route('/plot_demo' , methods = ['GET' , 'POST'])
def plot_demo():
    df = pd.read_csv(path.join(path.dirname(__file__), 'static/data/time_series_2019-ncov-Confirmed.csv'))
    df = df.drop(['Lat' , 'Long' , 'Province/State'], 1)
    df = df.rename(columns={'Country/Region': 'Country'})
    df = df.groupby('Country').sum()
    df = df.loc[['Israel' , 'France' , 'Italy' , 'Spain' , 'United Kingdom']]
    df = df.transpose()
    df = df.reset_index()
    df = df.drop(['index'], 1)
    df = df.tail(30)

    fig = plt.figure()
    ax = fig.add_subplot(111)
    df.plot(ax = ax , kind = 'line')
    chart = plot_to_img(fig)
    
    return render_template(
        'plot_demo.html',
        img_under_construction = '/static/imgs/under_construction.png',
        chart = chart ,
        height = "300" ,
        width = "750"
    )

def remove_plus(str):
    if '+' in str:
        x=str.index('+')
        return(str[:x])
    else:
        return(str)

@app.route('/query' , methods = ['GET' , 'POST'])
def query():
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

    #chart = {}
    #height_case_1 = "100"
    #width_case_1 = "250"

    #df_trump = pd.read_csv(path.join(path.dirname(__file__), 'static/data/trump.csv'))
    #df_obama = pd.read_csv(path.join(path.dirname(__file__), 'static/data/obama.csv'))
    #df_bush = pd.read_csv(path.join(path.dirname(__file__), 'static/data/bush.csv'))
    #df_clinton = pd.read_csv(path.join(path.dirname(__file__), 'static/data/clinton.csv'))
    #presidents_dict = {'trump' : df_trump , 'obama' : df_obama , 'bush' : df_bush , 'clinton' : df_clinton }

 
    #    start_date = form1.start_date.data
    #    end_date = form1.end_date.data
    #    kind = form1.kind.data
    #    height_case_1 = "300"
    #    width_case_1 = "750"

    #    print(president)
    #    print(start_date)
    #    print(end_date)
    #    print(type(start_date)) 
    #    x = str(start_date)
    #    print(x)
    #    chart = plot_case_1(presidents_dict[president] , start_date , end_date , kind)

    
    return render_template(
        'query.html',
        #img_trump = '/static/imgs/trump.jpg',
        #img_obama = '/static/imgs/obama.jpg',
        #img_bush = '/static/imgs/bush.jpg',
        #img_clinton = '/static/imgs/clinton.jpg',
        #img_under_construction = '/static/imgs/under_construction.png',
        #form1 = form1,
        #src_case_1 = chart,
        #height_case_1 = height_case_1 ,
        #width_case_1 = width_case_1 ,
        #code_ex_1 = '/static/imgs/code_ex_1.PNG'
    )
