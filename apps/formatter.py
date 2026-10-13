import json
from flask import Blueprint, request, jsonify

formatter_bp = Blueprint('formatter', __name__, url_prefix='/api/formatter')

@formatter_bp.route('/format-json', methods=['POST'])
def format_json():
    try:
        # 1. Manejo seguro de entrada (soporta JSON nativo y texto plano pegado)
        data = request.get_json(silent=True)
        
        if data is None:
            raw_text = request.get_data(as_text=True)
            if not raw_text or not raw_text.strip():
                return jsonify({'error': 'El cuerpo de la petición está vacío.'}), 400
            try:
                data = json.loads(raw_text)
            except json.JSONDecodeError as decode_err:
                return jsonify({
                    'error': f'Estructura JSON inválida: {decode_err.msg} (Línea {decode_err.lineno}, columna {decode_err.colno}).'
                }), 400

        # 2. Control de carga de memoria (Optimizado para el límite de RAM de PythonAnywhere)
        # Evita procesar payloads gigantescos que puedan causar un Out-Of-Memory (OOM) / error 502
        raw_bytes = request.content_length
        if raw_bytes and raw_bytes > 2 * 1024 * 1024:  # Límite preventivo de 2 MB
            return jsonify({'error': 'El archivo/payload JSON supera el límite permitido de 2 MB.'}), 413

        # 3. Formateo limpio del JSON
        formatted = json.dumps(
            data, 
            indent=4, 
            ensure_ascii=False, 
            sort_keys=False  # Mantiene la estructura original del usuario
        )

        return jsonify({
            'status': 'success',
            'formatted': formatted
        }), 200

    except Exception as e:
        return jsonify({'error': f'Error interno al procesar el JSON: {str(e)}'}), 500