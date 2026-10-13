from flask import Flask, render_template
from apps.converter import converter_bp
from apps.security import security_bp
from apps.webhook import webhook_bp
from apps.monitor import monitor_bp
from apps.formatter import formatter_bp
from apps.crypto import crypto_bp
from apps.text_analyzer import text_bp
from apps.network_tools import jwt_bp
from apps.unit_converter import units_bp

app = Flask(__name__)

# Registro de módulos
app.register_blueprint(converter_bp)
app.register_blueprint(security_bp)
app.register_blueprint(webhook_bp)
app.register_blueprint(monitor_bp)
app.register_blueprint(formatter_bp)
app.register_blueprint(crypto_bp)
app.register_blueprint(text_bp)
app.register_blueprint(jwt_bp)
app.register_blueprint(units_bp)

@app.route('/')
def dashboard():
    return render_template(index.html)

if __name__ == '__main__':
    app.run(debug=True)