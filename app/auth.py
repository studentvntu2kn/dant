from flask import Blueprint, render_template, redirect, url_for, request, flash
import re
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint('auth', __name__)


@auth.route('/signup')
def signup():
    return render_template('auth/signup.html')

@auth.route('/login')
def login():
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/signup', methods=['POST'])
def signup_post():
    phone = request.form.get('phone')
    name = request.form.get('name')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')

    # Перевірка наявності користувача з таким телефоном
    user = User.query.filter_by(phone=phone).first()
    if user:  # Якщо користувач знайдений, то телефон вже зареєстрований
        flash('Користувач з таким номером вже зареєстрований')
        return redirect(url_for('auth.signup'))

    # Перевірка на правильність телефону (формат: +380XXXXXXXXX)
    # phone_regex = r'^\+380\d{9}$'
    # if not re.match(phone_regex, phone):
    #     flash('Невірний формат номера телефону')
    #     return redirect(url_for('auth.signup'))

    # Перевірка на наявність імені
    if not name or len(name) < 2:
        flash('Будь ласка, введіть ім\'я (мінімум 2 символи)')
        return redirect(url_for('auth.signup'))

    # Перевірка, чи паролі співпадають
    if password != confirm_password:
        flash('Паролі не співпадають')
        return redirect(url_for('auth.signup'))

    # Перевірка на складність пароля
    # if len(password) < 8:
    #     flash('Пароль повинен містити не менше 8 символів')
    #     return redirect(url_for('auth.signup'))
    # if not re.search(r'[A-Za-z]', password):  # Перевірка на наявність букв
    #     flash('Пароль повинен містити хоча б одну літеру')
    #     return redirect(url_for('auth.signup'))
    # if not re.search(r'\d', password):  # Перевірка на наявність цифри
    #     flash('Пароль повинен містити хоча б одну цифру')
    #     return redirect(url_for('auth.signup'))

    # Створення нового користувача та хешування паролю
    new_user = User(phone=phone, name=name, password=generate_password_hash(password, method='pbkdf2:sha256'))

    # Додавання нового користувача до бази даних
    db.session.add(new_user)
    db.session.commit()

    # Перенаправлення на сторінку входу після успішної реєстрації
    flash('Реєстрація успішна, будь ласка, увійдіть')
    return redirect(url_for('auth.login'))



@auth.route('/login', methods=['POST'])
def login_post():
    phone = request.form.get('phone')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.query.filter_by(phone=phone).first()

    # check if the user actually exists
    # take the user-supplied password, hash it, and compare it to the hashed password in the database
    if not user or not check_password_hash(user.password, password):
        flash('Неправильний логін або пароль')
        return redirect(url_for('auth.login')) # if the user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for('cabinet.home'))