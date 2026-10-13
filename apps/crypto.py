import hashlib
from flask import Blueprint, request, jsonify

crypto_bp = Blueprint('crypto', __name__, url_prefix='/api/crypto')

@crypto_bp.route('/hash', methods=['POST'])
def generate_hash():
    payload = request.get_json() or {}
    text = payload.get('text', '')
    
    if not text:
        return jsonify({'error': 'El campo "text" es obligatorio.'}), 400
        
    encoded_text = text.encode('utf-8')
    
    return jsonify({
        'original': text,
        'hashes': {
            'md5': hashlib.md5(encoded_text).hexdigest(),
            'sha256': hashlib.sha256(encoded_text).hexdigest(),
            'sha512': hashlib.sha512(encoded_text).hexdigest()
        }
    })