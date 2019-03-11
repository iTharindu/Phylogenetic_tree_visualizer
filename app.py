from IPython.core.display import HTML
from flask import Flask, render_template, request, redirect, url_for, session,flash, logging
from flask_mysqldb import MySQL
from wtforms import Form, StringField, TextAreaField, PasswordField,validators
from passlib.hash import sha256_crypt



from werkzeug.utils import secure_filename
import numpy as np

from Bio import Phylo
from Bio.Phylo.TreeConstruction import DistanceCalculator
from Bio.Phylo.TreeConstruction import ParsimonyTreeConstructor
from Bio.Phylo.TreeConstruction import DistanceTreeConstructor
from Bio.Phylo.TreeConstruction import ParsimonyScorer
from Bio import AlignIO

import plot
import plotly
import plotly.graph_objs as go
import ipywidgets as ipw
import plotly.plotly as py
from plotly.offline import iplot, init_notebook_mode
import plotly.graph_objs as go
import plotly.io as pio
from IPython.display import Image

import gene_analyzer

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_DB'] = 'db_phygraph'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/upload')
def upload_file():
   return render_template('upload.html')


@app.route('/uploader', methods=['GET', 'POST'])
def uploader_file():
    if request.method == 'POST':
        f = request.files['file']
        f.save(secure_filename(f.filename))
        plot.create_circular_tree()
        gene_analyzer.create_tree(f.filename) 
    return render_template('uploader.html')


@app.route('/uploaded')
def uploaded_file():
    return render_template('uploaded.html')

class RegisterForm(Form):
    user_name = StringField('User Name', [validators.Length(min=1, max=50)])
    email = StringField('Email', [validators.Length(min = 6, max =100)])
    password = PasswordField('Password',[
        validators.DataRequired(),
        validators.EqualTo('confirm', message = 'Passwords do not match')
    ])
    confirm = PasswordField('Confirm Password')

@app.route('/register', methods = ['GET','POST'])
def register():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user_name = form.user_name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))
        
        cur = mysql.connection.cursor()

        cur.execute("Insert into Users(user_name,user_email,password) values(%s, %s, %s)", (user_name,email,password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registerd..', 'success')

        return redirect(url_for('upload_file'))
        
    return render_template('register.html', form = form)


@app.route('/register_test', methods=['GET', 'POST'])
def register_test():
    form = RegisterForm(request.form)
    if request.method == 'POST' and form.validate():
        user_name = form.user_name.data
        email = form.email.data
        password = sha256_crypt.encrypt(str(form.password.data))

        cur = mysql.connection.cursor()

        cur.execute("Insert into Users(user_name,user_email,password) values(%s, %s, %s)",
                    (user_name, email, password))

        mysql.connection.commit()

        cur.close()

        flash('You are now registerd..', 'success')

        return redirect(url_for('upload_file'))

    return render_template('register_test.html', form=form)



@app.route('/login')
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.secret_key = 'secret'
    app.run(debug=True)

