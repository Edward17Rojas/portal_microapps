import io
import string
import secrets
import qrcode
from flask import Blueprint, request, jsonify, send_file

security_bp = Blueprint('security', __name__, url_prefix='/api/security')

@security_bp.route('/generate-password', methods=['GET'])
def generate_password():
    length = int(request.args.get('length', 16))
    length = min(max(length, 8), 64)  # Restricción entre 8 y 64 caracteres
    chars = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(chars) for _ in range(length))
    return jsonify({'password': password, 'length': length})

@security_bp.route('/generate-qr', methods=['POST'])
def generate_qr():
    data = request.json.get('text', '') if request.json else ''
    if not data:
        return jsonify({'error': 'El campo text es requerido.'}), 400
    
    if len(data) > 500:
        msg = 'El texto excede el límite permitido de 500 caracteres.'
        return jsonify({'error': msg}), 400

    img = qrcode.make(data)
    buf = io.BytesIO()
    img.save(buf, 'PNG')
    buf.seek(0)
    return send_file(buf, mimetype='image/png')