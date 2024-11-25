from flask import Blueprint, render_template

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


@main.route('/register')
def register():
    return render_template('auth/register.html')

@main.route('/login')
def login():
    return render_template('auth/login.html')
