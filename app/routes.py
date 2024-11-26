import os
from . import db
from flask import Blueprint, render_template
from flask import send_from_directory

main = Blueprint('main', __name__)

@main.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(main.root_path, 'app/static'),
                               'favicon.ico', mimetype='img/favicon.ico')

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/home')
def home2():
    return render_template('index.html')

@main.route('/about')
def about():
    return render_template('info/about.html')

@main.route('/review')
def review():
    return render_template('info/review.html')

@main.route('/services')
def services():
    return render_template('info/services.html')

@main.route('/contact')
def contact():
    return render_template('info/contact.html')

