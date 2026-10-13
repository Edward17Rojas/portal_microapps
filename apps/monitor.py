import urllib.request
import urllib.error
import time
from flask import Blueprint, request, jsonify

monitor_bp = Blueprint('monitor', __name__, url_prefix='/api/monitor')

@monitor_bp.route('/check', methods=['POST'])
def check_status():
    payload = request.get_json() or {}
    url = payload.get('url')
    if not url:
        return jsonify({'error': 'La URL es requerida.'}), 400
    
    headers = {'User-Agent': 'Mozilla/5.0'}
    req = urllib.request.Request(url, headers=headers)
    start_time = time.time()
    
    try:
        # Timeout estricto de 3 segundos
        with urllib.request.urlopen(req, timeout=3) as response:
            elapsed_time = round((time.time() - start_time) * 1000, 2)
            return jsonify({
                'url': url,
                'status_code': response.getcode(),
                'response_time_ms': elapsed_time,
                'online': True
            })
    except urllib.error.HTTPError as e:
        elapsed_time = round((time.time() - start_time) * 1000, 2)
        return jsonify({
            'url': url,
            'status_code': e.code,
            'response_time_ms': elapsed_time,
            'online': False
        })
    except Exception as e:
        msg = 'Error o restricción de red (Allowlist PythonAnywhere)'
        return jsonify({'url': url, 'online': False, 'error': msg}), 500