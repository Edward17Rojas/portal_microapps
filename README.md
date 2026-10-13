# portal_microapps

Portal de microaplicaciones desarrollado con Flask para practicar casos reales de desarrollo web, despliegue y mantenimiento de pequeños servicios funcionales.

El proyecto consiste en una aplicación web que centraliza varias utilidades útiles para validación, conversión, seguridad, análisis y monitoreo. Cada funcionalidad está separada en un módulo independiente mediante blueprints de Flask, lo que facilita mantenimiento, extensión y reutilización.

## Objetivo

Crear un conjunto de microapps simples pero útiles para:

- practicar desarrollo con Flask
- aprender a estructurar aplicaciones modulares
- explorar APIs REST con validaciones básicas
- probar herramientas de seguridad, conversión y monitoreo web
- preparar el proyecto para despliegue en servicios como PythonAnywhere

## Características principales

La aplicación incluye estos módulos funcionales:

- Convertidor JSON a CSV
- Generador de contraseñas
- Generador de códigos QR
- Verificador de estado de una URL
- Formateador de JSON
- Generador de hashes MD5, SHA256 y SHA512
- Analizador de texto
- Decodificador de JWT
- Conversor de unidades de tamaño (bytes, KB, MB, GB)
- Endpoint para pruebas de webhook/echo

## Estructura del proyecto

```text
portal_microapps/
├── app.py
├── wsgi.py
├── requirements.txt
├── README.md
├── .gitignore
├── apps/
│   ├── __init__.py
│   ├── converter.py
│   ├── crypto.py
│   ├── formatter.py
│   ├── monitor.py
│   ├── network_tools.py
│   ├── security.py
│   ├── text_analyzer.py
│   ├── unit_converter.py
│   └── webhook.py
├── templates/
│   └── index.html
└── static/
    (si se agrega más contenido frontend o assets)
```

## Módulos y endpoints

### 1. Converter

Archivo: `apps/converter.py`

- `POST /api/converter/json-to-csv`
- Convierte una lista de objetos JSON en un archivo CSV descargable.
- Incluye validación para evitar payloads excesivamente grandes.

### 2. Security

Archivo: `apps/security.py`

- `GET /api/security/generate-password?length=16`
- Genera una contraseña aleatoria entre 8 y 64 caracteres.
- `POST /api/security/generate-qr`
- Genera un código QR a partir de un texto enviado en JSON.

### 3. Monitor

Archivo: `apps/monitor.py`

- `POST /api/monitor/check`
- Verifica si una URL responde correctamente y devuelve:
  - código HTTP
  - tiempo de respuesta
  - estado en línea/offline

### 4. Formatter

Archivo: `apps/formatter.py`

- `POST /api/formatter/format-json`
- Formatea JSON válido y responde con una versión indentada.
- Acepta JSON nativo o texto plano con contenido JSON.

### 5. Crypto

Archivo: `apps/crypto.py`

- `POST /api/crypto/hash`
- Genera hashes de un texto en:
  - MD5
  - SHA256
  - SHA512

### 6. Text Analyzer

Archivo: `apps/text_analyzer.py`

- `POST /api/text/analyze`
- Calcula métricas como:
  - cantidad de palabras
  - caracteres con espacios
  - caracteres sin espacios
  - líneas
  - tiempo estimado de lectura

### 7. JWT

Archivo: `apps/network_tools.py`

- `POST /api/jwt/decode`
- Decodifica la estructura de un JWT y devuelve header y payload.

### 8. Unit Converter

Archivo: `apps/unit_converter.py`

- `GET /api/units/bytes?bytes=1048576`
- Convierte bytes a:
  - KB
  - MB
  - GB

### 9. Webhook Echo

Archivo: `apps/webhook.py`

- `GET|POST|PUT|DELETE /api/webhook/echo`
- Permite probar cómo se reciben headers, parámetros, JSON y cuerpo de la petición.

## Aplicación principal

El archivo `app.py` inicia la aplicación Flask y registra todos los blueprints.

```python
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
    return render_template('index.html')
```

## Requisitos

El proyecto usa las siguientes dependencias:

```txt
Flask>=3.0.0
qrcode>=7.4.2
Pillow>=10.0.0
```

Se pueden instalar con:

```bash
pip install -r requirements.txt
```

## Ejecución local

```bash
python app.py
```

Luego abre en el navegador:

```text
http://127.0.0.1:5000/
```

## Despliegue

El proyecto incluye un archivo `wsgi.py` pensado para despliegues tipo WSGI, especialmente en servicios como PythonAnywhere.

```python
import sys
import os

path = '/home/tu_usuario/portal_microapps'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
```

Es necesario ajustar la ruta del proyecto al directorio real donde se encuentre alojado.

## Consideraciones de seguridad y uso

Este proyecto se diseñó como ejercicio práctico y no como una solución de producción completa. Algunas validaciones incluyen:

- límites de tamaño para evitar abuso de memoria
- validación de entrada en varios endpoints
- uso de control de tiempos en verificación de URLs
- manejo de errores con respuestas JSON claras

## Estado del proyecto

Proyecto en desarrollo/curso, orientado a prácticas de:

- Flask
- microservicios pequeños
- APIs REST
- despliegue web
- mantenimiento de aplicaciones simples
- organización modular del código

## Ideas de mejora futuras

- agregar autenticación y autorización
- separar frontend y backend en estructura más formal
- añadir tests automatizados
- crear más microapps especializadas
- integrar base de datos para persistencia
- desplegar con Docker
- añadir documentación de cada endpoint en Swagger/OpenAPI

## Autor

Edward Rojas
Proyecto desarrollado para practicar usos prácticos de Flask, despliegue y mantenimiento de microapps.


