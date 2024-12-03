from datetime import datetime

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User, Appointment
from flask import jsonify
from . import db

cabinet = Blueprint('cabinet', __name__)

#
# Route
#
@cabinet.route('/cabinet')
@login_required
def home():
    return render_template('cabinet/cabinet.html', name=current_user.name)


@cabinet.route('/cabinet/schedule')
@login_required
def schedule():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    current_time = datetime.now()

    current_time = current_time.replace(second=0, microsecond=0)
    for appointment in appointments:
        appointment.is_past = appointment.date < current_time

    return render_template('cabinet/schedule.html',
                           name=current_user.name,
                           phone=current_user.phone,
                           current_time=current_time,
                           appointments=appointments)


@cabinet.route('/cabinet/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        # Отримуємо дані з форми
        new_name = request.form.get('display-name')
        current_password = request.form.get('current-password')
        new_password = request.form.get('new-password')
        confirm_password = request.form.get('confirm-password')

        # Перевірка зміни імені
        if new_name and new_name != current_user.name:
            current_user.name = new_name
            db.session.commit()
            flash('Ім\'я успішно змінено.')

        # Якщо паролі заповнені, виконуємо зміну пароля
        if current_password or new_password or confirm_password:
            # Перевірка, чи введений старий пароль
            if not current_password:
                flash('Будь ласка, введіть ваш поточний пароль.')
                return redirect(url_for('cabinet.settings'))

            # Перевірка, чи введений новий пароль
            if not new_password or not confirm_password:
                flash('Будь ласка, введіть новий пароль і його підтвердження.')
                return redirect(url_for('cabinet.settings'))

            # Перевірка правильності старого паролю
            if not check_password_hash(current_user.password, current_password):
                flash('Неправильний старий пароль.')
                return redirect(url_for('cabinet.settings'))

            # Перевірка на співпадіння нового паролю та підтвердження
            if new_password != confirm_password:
                flash('Паролі не співпадають.')
                return redirect(url_for('cabinet.settings'))

            # Оновлення паролю в базі даних
            hashed_new_password = generate_password_hash(new_password, method='pbkdf2:sha256')
            current_user.password = hashed_new_password
            db.session.commit()
            flash('Пароль успішно змінено.')

        return redirect(url_for('cabinet.settings'))

    return render_template('cabinet/settings.html', name=current_user.name)

# Schedule
@cabinet.route('/cabinet/schedule', methods=['GET', 'POST'])
@login_required
def schedule_post():
    if request.method == 'POST':
        # Отримання даних із форми
        name = request.form.get('name')
        phone = request.form.get('phone')
        datetime_input = request.form.get('datetime')
        doctor = request.form.get('doctor')
        clinic = request.form.get('clinica')

        # Перевірка, чи всі поля заповнені
        if not all([name, phone, datetime_input, doctor, clinic]):
            flash('Будь ласка, заповніть усі поля.', 'error')
            return redirect(url_for('cabinet.schedule'))

        # Перевірка формату дати і часу
        try:
            datetime_obj = datetime.strptime(datetime_input, '%Y-%m-%dT%H:%M')
        except ValueError:
            flash('Некоректна дата і час.', 'error')
            return redirect(url_for('cabinet.schedule'))

        # Перевірка на минуле
        if datetime_obj < datetime.now():
            flash('Не можна вибрати дату або час у минулому.', 'error')
            return redirect(url_for('cabinet.schedule'))

        # Створення нового запису
        new_appointment = Appointment(
            phone=phone,
            name=name,
            date=datetime_obj,
            doctor_name=get_doctor_name(doctor),
            clinic_name=get_clinic_name(clinic),
            user_id=current_user.id
        )

        # Збереження у базі даних
        db.session.add(new_appointment)
        db.session.commit()

        flash('Запис успішно створено!', 'success')
        return redirect(url_for('cabinet.schedule'))

    # Завантаження форми та існуючих записів
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('cabinet/schedule.html', name=current_user.name, appointments=appointments)


# Функція для отримання імені лікаря за його ID
def get_doctor_name(doctor_id):
    doctors = {
        '1': 'Болюх Володимир',
        '2': 'Гаврилюк Владислав',
        '3': 'Коломієць Дімка'
    }
    return doctors.get(doctor_id, 'Невідомий лікар')

# Функція для отримання назви клініки за її ID
def get_clinic_name(clinic_id):
    clinics = {
        '1': 'ВНТУ Корпус 1',
        '2': 'ВНТУ Корпус 2',
        '3': 'ВНТУ Корпус 5'
    }
    return clinics.get(clinic_id, 'Невідома клініка')


# Notify
@cabinet.route('/cabinet/toggle-notification', methods=['POST'])
@login_required
def toggle_notification():
    data = request.get_json()
    notification_type = data.get('type')
    new_status = data.get('status')

    # Перевірка валідності типу та статусу
    if notification_type not in ['sms', 'viber']:
        return jsonify({'success': False, 'message': 'Невідомий тип оповіщення'})

    if new_status not in ['enabled', 'disabled']:
        return jsonify({'success': False, 'message': 'Невідомий статус'})

    # Зміна статусу у базі даних
    try:
        if notification_type == 'sms':
            current_user.sms_notifications = (new_status == 'enabled')
        elif notification_type == 'viber':
            current_user.viber_notifications = (new_status == 'enabled')

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)})


#
@cabinet.route('/cabinet/delete-appointment/<int:appointment_id>', methods=['POST'])
@login_required
def delete_appointment(appointment_id):
    # Шукаємо запис за його ID
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        flash('Запис не знайдено.', 'error')
        return redirect(url_for('cabinet.schedule'))

    # Перевіряємо, чи запис належить поточному користувачу
    if appointment.user_id != current_user.id:
        flash('Ви не можете видалити цей запис.', 'error')
        return redirect(url_for('cabinet.schedule'))

    # Видаляємо запис
    db.session.delete(appointment)
    db.session.commit()

    flash('Запис успішно видалено.', 'success')
    return redirect(url_for('cabinet.schedule'))


@cabinet.route('/cabinet/edit-appointment/<int:appointment_id>', methods=['POST'])
@login_required
def edit_appointment(appointment_id):
    # Знаходимо запис у базі даних
    appointment = Appointment.query.get(appointment_id)

    if not appointment:
        return jsonify({'success': False, 'message': 'Запис не знайдено.'}), 404

    # Перевіряємо, чи запис належить поточному користувачу
    if appointment.user_id != current_user.id:
        return jsonify({'success': False, 'message': 'У вас немає прав редагувати цей запис.'}), 403

    # Отримуємо дані з JSON-запиту
    data = request.get_json()
    new_date = data.get('date')
    new_doctor_id = data.get('doctor')
    new_clinic_id = data.get('clinic')

    # Перевірка наявності дати
    if not new_date:
        return jsonify({'success': False, 'message': 'Дата не може бути порожньою.'}), 400

    try:
        new_date_obj = datetime.strptime(new_date, '%Y-%m-%dT%H:%M')
        if new_date_obj < datetime.now():
            return jsonify({'success': False, 'message': 'Дата не може бути в минулому.'}), 400
    except ValueError:
        return jsonify({'success': False, 'message': 'Некоректна дата.'}), 400

    # Перевірка лікаря та клініки
    new_doctor_name = get_doctor_name(new_doctor_id)
    new_clinic_name = get_clinic_name(new_clinic_id)

    if not new_doctor_name or not new_clinic_name:
        return jsonify({'success': False, 'message': 'Невірні дані лікаря або клініки.'}), 400

    # Оновлюємо запис
    try:
        appointment.date = new_date_obj
        appointment.doctor_name = new_doctor_name
        appointment.clinic_name = new_clinic_name

        db.session.commit()
        return jsonify({
            'success': True,
            'message': 'Запис успішно оновлено.',
            'data': {
                'id': appointment.id,
                'date': appointment.date.strftime('%Y-%m-%dT%H:%M'),
                'doctor': appointment.doctor_name,
                'clinic': appointment.clinic_name
            }
        }), 200

    except Exception as e:
        return jsonify({'success': False, 'message': f'Помилка сервера: {str(e)}'}), 500
