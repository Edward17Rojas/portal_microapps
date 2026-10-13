from flask import Blueprint, request, jsonify

webhook_bp = Blueprint('webhook', __name__, url_prefix='/api/webhook')

@webhook_bp.route('/echo', methods=['GET', 'POST', 'PUT', 'DELETE'])
def echo():
    return jsonify({
        'method': request.method,
        'headers': dict(request.headers),
        'args': request.args,
        'json': request.get_json(silent=True),
        'data': request.get_data(as_text=True)
    })