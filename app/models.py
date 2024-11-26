from datetime import datetime
from flask_login import UserMixin
from app import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    phone = db.Column(db.String(15), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    name = db.Column(db.String(50), nullable=False)

    # Булеві поля для відслідковування налаштувань оповіщень
    viber_notifications = db.Column(db.Boolean, default=False)  # Включене Вайбер оповіщення
    sms_notifications = db.Column(db.Boolean, default=False)  # Включене СМС оповіщення

    # Зв'язок один-до-багатьох з Appointment
    appointments = db.relationship('Appointment', backref='user', lazy=True)

    def __repr__(self):
        return f'<User {self.id}, {self.name}>'


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор запису
    phone = db.Column(db.String(15), nullable=False)  # Номер телефону
    name = db.Column(db.String(50), nullable=False)  # Ім'я користувача
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    doctor_name = db.Column(db.String(50), nullable=False)  # Ім'я лікаря
    clinic_name = db.Column(db.String(100), nullable=False)  # Назва клініки

    # Зовнішній ключ, що зв'язує запис з користувачем
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Appointment {self.id}, {self.name}, {self.date}>'
