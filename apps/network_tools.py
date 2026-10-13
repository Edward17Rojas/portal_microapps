import base64
import json
from flask import Blueprint, request, jsonify

jwt_bp = Blueprint('jwt', __name__, url_prefix='/api/jwt')

@jwt_bp.route('/decode', methods=['POST'])
def decode_jwt():
    payload = request.get_json() or {}
    token = payload.get('token', '').strip()
    
    if not token:
        return jsonify({'error': 'El campo "token" es requerido.'}), 400
        
    parts = token.split('.')
    if len(parts) != 3:
        return jsonify({'error': 'Estructura JWT no válida. Debe contener tres partes separadas por puntos.'}), 400
        
    try:
        def decode_base64_part(data):
            padded = data + '=' * (-len(data) % 4)
            decoded_bytes = base64.urlsafe_b64decode(padded)
            return json.loads(decoded_bytes.decode('utf-8'))

        header = decode_base64_part(parts[0])
        body = decode_base64_part(parts[1])

        return jsonify({
            'status': 'valid_structure',
            'header': header,
            'payload': body,
            'signature_present': bool(parts[2])
        })
    except Exception as e:
        return jsonify({'error': f'Falló la decodificación del token: {str(e)}'}), 400