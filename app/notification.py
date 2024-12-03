# app/notification.py
import threading
import time

from datetime import datetime, timedelta


class NotificationManager:
    def __init__(self, app, db):
        self.app = app  # Передаємо додаток
        self.db = db
        self.notification_intervals = {
            '3 hours': timedelta(hours=3),
            '8 hours': timedelta(hours=8),
            '1 day': timedelta(days=1),
        }

    def check_and_send_notifications(self):
        with self.app.app_context():  # Активуємо контекст додатка
            from app.models import Appointment  # Імпортуємо всередині контексту
            now = datetime.now()
            appointments = Appointment.query.all()

            for appointment in appointments:
                time_until_appointment = appointment.date - now

                if appointment.user.viber_notifications:
                    self._send_viber_notification(appointment, time_until_appointment)

                if appointment.user.sms_notifications:
                    self._send_sms_notification(appointment, time_until_appointment)

    def _send_viber_notification(self, appointment, time_until_appointment):
        # Перевірка часу для сповіщення
        for label, interval in self.notification_intervals.items():
            if timedelta(0) < time_until_appointment <= interval:
                print(f"Viber notification sent for appointment {appointment.id} ({label})")

    def _send_sms_notification(self, appointment, time_until_appointment):
        # Перевірка часу для сповіщення
        for label, interval in self.notification_intervals.items():
            if timedelta(0) < time_until_appointment <= interval:
                print(f"SMS notification sent for appointment {appointment.id} ({label})")

    def scheduler(self):
        while True:
            self.check_and_send_notifications()
            time.sleep(60)  # Перевірка кожну хвилину

    def start_scheduler(self):
        thread = threading.Thread(target=self.scheduler, daemon=True)
        thread.start()
