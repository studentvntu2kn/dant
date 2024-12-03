from flask import Blueprint, jsonify
from app.models import Doctor

doctor_bp = Blueprint('doctor', __name__)

@doctor_bp.route('/get-doctors', methods=['GET'])
def get_doctors():
    """Повертає список лікарів у форматі JSON."""
    doctors = Doctor.query.all()
    return jsonify([
        {
            "id": doctor.id,
            "full_name": doctor.full_name,
            "specialty": doctor.specialty
        }
        for doctor in doctors
    ])
