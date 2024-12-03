from flask import Blueprint, jsonify
from app.models import Clinic

clinic_bp = Blueprint('clinic', __name__)

@clinic_bp.route('/get-clinics', methods=['GET'])
def get_clinics():
    """Повертає список клінік у форматі JSON."""
    clinics = Clinic.query.all()
    return jsonify([
        {
            "id": clinic.id,
            "name": clinic.name
        }
        for clinic in clinics
    ])
