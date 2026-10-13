import json
from flask import Blueprint, request, jsonify

formatter_bp = Blueprint('formatter', __name__, url_prefix='/api/formatter')

@formatter_bp.route('/format-json', methods=['POST'])
def format_json():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'El cuerpo de la petición no contiene un JSON válido o está vacío.'}), 400
        
        formatted = json.dumps(data, indent=4, ensure_ascii=False)
        return jsonify({
            'status': 'success',
            'formatted': formatted
        })
    except Exception as e:
        return jsonify({'error': f'Error al procesar la estructura JSON: {str(e)}'}), 500