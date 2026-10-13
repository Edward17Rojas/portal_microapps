from flask import Blueprint, request, jsonify

units_bp = Blueprint('units', __name__, url_prefix='/api/units')

@units_bp.route('/bytes', methods=['GET'])
def convert_bytes():
    raw_bytes = request.args.get('bytes')
    
    if raw_bytes is None:
        return jsonify({'error': 'El parámetro "bytes" es obligatorio en la URL.'}), 400
        
    try:
        size_bytes = float(raw_bytes)
        if size_bytes < 0:
            return jsonify({'error': 'El valor de bytes no puede ser negativo.'}), 400
            
        return jsonify({
            'input_bytes': size_bytes,
            'conversions': {
                'kilobytes': round(size_bytes / 1024, 2),
                'megabytes': round(size_bytes / (1024**2), 4),
                'gigabytes': round(size_bytes / (1024**3), 6)
            }
        })
    except ValueError:
        return jsonify({'error': 'El parámetro "bytes" debe ser un número válido.'}), 400