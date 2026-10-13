from flask import Blueprint, request, jsonify

text_bp = Blueprint('text', __name__, url_prefix='/api/text')

@text_bp.route('/analyze', methods=['POST'])
def analyze():
    payload = request.get_json() or {}
    content = payload.get('text', '')
    
    if not content:
        return jsonify({'error': 'No se ha proporcionado texto para analizar.'}), 400
    
    words = content.split()
    word_count = len(words)
    reading_time = round((word_count / 200) * 60, 2)
    
    return jsonify({
        'metrics': {
            'words': word_count,
            'characters_with_spaces': len(content),
            'characters_no_spaces': len(content.replace(' ', '').replace('\n', '').replace('\r', '')),
            'lines': len(content.splitlines()),
            'estimated_reading_time_seconds': reading_time
        }
    })