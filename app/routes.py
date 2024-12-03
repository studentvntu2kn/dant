import os
from . import db
from flask import Blueprint, render_template
from flask import send_from_directory

main = Blueprint('main', __name__)

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

@main.route('/doctors')
def doctors():
    return render_template('info/doctors.html')

