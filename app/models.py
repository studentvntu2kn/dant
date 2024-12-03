import json
from datetime import datetime
from flask_login import UserMixin
from app.extensions import db

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

class Doctor(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор лікаря
    full_name = db.Column(db.String(100), nullable=False)  # Ім'я та прізвище лікаря
    specialty = db.Column(db.String(100), nullable=False)  # Спеціальність лікаря

    def __repr__(self):
        return f'<Doctor {self.id}, {self.full_name}, {self.specialty}>'

    @staticmethod
    def load_doctors_from_json(file_path, app):
        import json
        from sqlalchemy.exc import IntegrityError

        with app.app_context():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for doctor_data in data['doctors']:
                    # Перевіряємо, чи лікар із таким ID вже існує
                    existing_doctor = Doctor.query.filter_by(id=doctor_data['id']).first()
                    if existing_doctor:
                        # Оновлюємо існуючий запис
                        existing_doctor.full_name = doctor_data['full_name']
                        existing_doctor.specialty = doctor_data['specialty']
                    else:
                        # Додаємо нового лікаря
                        doctor = Doctor(
                            id=doctor_data['id'],
                            full_name=doctor_data['full_name'],
                            specialty=doctor_data['specialty']
                        )
                        db.session.add(doctor)

                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Помилка завантаження лікарів із JSON: {e}")
            except Exception as e:
                print(f"Інша помилка: {e}")


class Clinic(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Унікальний ідентифікатор лікаря
    name = db.Column(db.String(100), nullable=False)  # Ім'я та прізвище лікаря

    def __repr__(self):
        return f'<Clinic {self.id}, {self.name}>'

    @staticmethod
    def load_clinics_from_json(file_path, app):
        import json
        from sqlalchemy.exc import IntegrityError

        with app.app_context():
            try:
                with open(file_path, 'r', encoding='utf-8') as file:
                    data = json.load(file)

                for clinic_data in data['clinics']:
                    # Перевіряємо, чи лікар із таким ID вже існує
                    existing_clinic = Clinic.query.filter_by(id=clinic_data['id']).first()
                    if existing_clinic:
                        # Оновлюємо існуючий запис
                        existing_clinic.name = clinic_data['name']
                    else:
                        # Додаємо нового лікаря
                        clinic = Clinic(
                            id=clinic_data['id'],
                            name=clinic_data['name']
                        )
                        db.session.add(clinic)

                db.session.commit()
            except IntegrityError as e:
                db.session.rollback()
                print(f"Помилка завантаження клінік із JSON: {e}")
            except Exception as e:
                print(f"Інша помилка: {e}")
