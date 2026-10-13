import io
import csv
from flask import Blueprint, request, jsonify, Response

converter_bp = Blueprint('converter', __name__, url_prefix='/api/converter')

@converter_bp.route('/json-to-csv', methods=['POST'])
def json_to_csv():
    try:
        data = request.get_json()
        if not data or not isinstance(data, list):
            msg = 'El cuerpo de la petición debe ser una lista JSON de objetos.'
            return jsonify({'error': msg}), 400
        
        # Validación de seguridad para no sobrecargar RAM
        if len(data) > 500:
            msg = 'Límite excedido. Máximo 500 registros por petición.'
            return jsonify({'error': msg}), 400

        output = io.StringIO()
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
        
        return Response(
            output.getvalue(),
            mimetype='text/csv',
            headers={
                'Content-Disposition': 'attachment;filename=converted.csv'
            }
        )
    except Exception as e:
        return jsonify({'error': str(e)}), 500