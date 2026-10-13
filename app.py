from flask import Flask, render_template_string
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

DASHBOARD_HTML = """
<<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Hub de Microaplicaciones Flask</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-900 text-slate-100 min-h-screen font-sans">
    <header class="border-b border-slate-800 bg-slate-950/50 backdrop-blur sticky top-0 z-50">
        <div class="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
            <div class="flex items-center space-x-3">
                <i class="fa-solid fa-cubes text-indigo-500 text-2xl"></i>
                <h1 class="text-xl font-bold tracking-tight">Portal MicroApps</h1>
            </div>
            <span class="bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 px-3 py-1 rounded-full text-xs font-mono">
                <i class="fa-solid fa-circle text-[8px] mr-1 animate-pulse"></i> Sistema Online
            </span>
        </div>
    </header>

    <main class="max-w-7xl mx-auto px-6 py-8">
        <section class="mb-8">
            <h2 class="text-3xl font-extrabold text-white">Consola Interactiva</h2>
            <p class="text-slate-400 mt-1">Prueba los endpoints directamente desde este panel sin necesidad de herramientas externas.</p>
        </section>

        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            
            <!-- Tarjeta 1: Generador de Contraseñas -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-amber-500/10 text-amber-400 rounded-md">Seguridad</span>
                        <span class="text-xs font-mono text-slate-400">GET</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-key mr-2 text-amber-400"></i>Generador de Passwords</h3>
                    <p class="text-slate-400 text-sm mb-4">Genera claves de alta entropía ajustando la longitud.</p>
                    
                    <div class="mb-4">
                        <label class="text-xs text-slate-400 block mb-1">Longitud (8-64):</label>
                        <input type="number" id="pass-length" value="16" min="8" max="64" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-1.5 text-sm text-white">
                    </div>
                </div>

                <div>
                    <button onclick="testPassword()" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">
                        Generar Password
                    </button>
                    <pre id="pass-output" class="text-xs font-mono bg-slate-950 p-3 rounded text-amber-300 overflow-x-auto min-h-[40px] flex items-center">Resultado aquí...</pre>
                </div>
            </div>

            <!-- Tarjeta 2: Generador de QR -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-amber-500/10 text-amber-400 rounded-md">Seguridad</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-qrcode mr-2 text-amber-400"></i>Generador de Código QR</h3>
                    <p class="text-slate-400 text-sm mb-4">Ingresa un texto o URL para compilar la imagen QR.</p>
                    
                    <div class="mb-4">
                        <input type="text" id="qr-text" placeholder="https://ejemplo.com" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-1.5 text-sm text-white">
                    </div>
                </div>

                <div>
                    <button onclick="testQR()" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">
                        Generar QR
                    </button>
                    <div id="qr-output" class="bg-slate-950 rounded p-2 flex justify-center items-center min-h-[120px]">
                        <span class="text-xs text-slate-500">Imagen QR se mostrará aquí</span>
                    </div>
                </div>
            </div>

            <!-- Tarjeta 3: Monitor de APIs -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-emerald-500/10 text-emerald-400 rounded-md">Red</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-satellite-dish mr-2 text-emerald-400"></i>Monitor de APIs</h3>
                    <p class="text-slate-400 text-sm mb-4">Verifica el tiempo de respuesta de una URL.</p>
                    
                    <div class="mb-4">
                        <input type="url" id="monitor-url" value="https://httpbin.org/get" class="w-full bg-slate-900 border border-slate-700 rounded px-3 py-1.5 text-sm text-white">
                    </div>
                </div>

                <div>
                    <button onclick="testMonitor()" class="w-full bg-emerald-600 hover:bg-emerald-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">
                        Consultar Estado
                    </button>
                    <pre id="monitor-output" class="text-xs font-mono bg-slate-950 p-3 rounded text-emerald-300 overflow-x-auto min-h-[40px] flex items-center">Esperando prueba...</pre>
                </div>
            </div>

            <!-- Tarjeta 4: JSON a CSV -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-indigo-500/10 text-indigo-400 rounded-md">Datos</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-file-csv mr-2 text-indigo-400"></i>JSON a CSV</h3>
                    <p class="text-slate-400 text-sm mb-4">Convierte una lista de objetos JSON a un archivo CSV descargable.</p>
                    
                    <div class="mb-4">
                        <textarea id="json-input" rows="3" class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-xs text-emerald-400 font-mono">[{"nombre":"Edward","rol":"Dev"}]</textarea>
                    </div>
                </div>

                <div>
                    <button onclick="testConverter()" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">
                        Convertir y Descargar CSV
                    </button>
                    <pre id="converter-output" class="text-xs font-mono bg-slate-950 p-2 rounded text-slate-400 min-h-[30px]">Estado: Listo</pre>
                </div>
            </div>

            <!-- Tarjeta 5: Formateador JSON -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-amber-500/10 text-amber-400 rounded-md">Dev Tools</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-code mr-2 text-amber-400"></i>Formateador JSON</h3>
                    <p class="text-slate-400 text-sm mb-4">Organiza y embellece estructuras JSON desordenadas.</p>
                    <textarea id="fmt-input" rows="3" class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-xs text-amber-300 font-mono mb-4" placeholder='{"a":1,"b":2}'></textarea>
                </div>
                <div>
                    <button onclick="testFormatter()" class="w-full bg-amber-600 hover:bg-amber-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">Formatear</button>
                    <pre id="fmt-output" class="text-xs font-mono bg-slate-950 p-2 rounded text-slate-400 min-h-[40px] overflow-x-auto">Estado: Esperando entrada...</pre>
                </div>
            </div>

            <!-- Tarjeta 6: Generador de Hashes -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-rose-500/10 text-rose-400 rounded-md">Cripto</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-key mr-2 text-rose-400"></i>Generador Hashes</h3>
                    <p class="text-slate-400 text-sm mb-4">Calcula firmas MD5, SHA-256 y SHA-512 de un texto.</p>
                    <input type="text" id="hash-input" value="portal_microapps" class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-xs text-white mb-4">
                </div>
                <div>
                    <button onclick="testCrypto()" class="w-full bg-rose-600 hover:bg-rose-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">Generar Hashes</button>
                    <pre id="hash-output" class="text-xs font-mono bg-slate-950 p-2 rounded text-slate-400 min-h-[40px] overflow-x-auto">Estado: Esperando entrada...</pre>
                </div>
            </div>

            <!-- Tarjeta 7: Analizador de Texto -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-teal-500/10 text-teal-400 rounded-md">Texto</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-font mr-2 text-teal-400"></i>Analizador Texto</h3>
                    <p class="text-slate-400 text-sm mb-4">Cuenta palabras, caracteres y tiempo de lectura.</p>
                    <textarea id="text-input" rows="3" class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-xs text-white mb-4" placeholder="Escribe tu texto aquí..."></textarea>
                </div>
                <div>
                    <button onclick="testTextAnalyzer()" class="w-full bg-teal-600 hover:bg-teal-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">Analizar</button>
                    <pre id="text-output" class="text-xs font-mono bg-slate-950 p-2 rounded text-slate-400 min-h-[40px] overflow-x-auto">Estado: Esperando entrada...</pre>
                </div>
            </div>

            <!-- Tarjeta 8: Decodificador JWT -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-purple-500/10 text-purple-400 rounded-md">Auth</span>
                        <span class="text-xs font-mono text-slate-400">POST</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-shield-halved mr-2 text-purple-400"></i>Decodificador JWT</h3>
                    <p class="text-slate-400 text-sm mb-4">Extrae el Header y Payload de un token JWT.</p>
                    <input type="text" id="jwt-input" placeholder="eyJhbGciOiJIUzI1Ni..." class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-xs text-white mb-4">
                </div>
                <div>
                    <button onclick="testJwt()" class="w-full bg-purple-600 hover:bg-purple-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">Decodificar</button>
                    <pre id="jwt-output" class="text-xs font-mono bg-slate-950 p-2 rounded text-slate-400 min-h-[40px] overflow-x-auto">Estado: Esperando entrada...</pre>
                </div>
            </div>

            <!-- Tarjeta 9: Conversor de Unidades -->
            <div class="bg-slate-800/50 border border-slate-700/50 rounded-xl p-6 flex flex-col justify-between">
                <div>
                    <div class="flex items-center justify-between mb-4">
                        <span class="text-xs font-semibold px-2.5 py-1 bg-sky-500/10 text-sky-400 rounded-md">Datos</span>
                        <span class="text-xs font-mono text-slate-400">GET</span>
                    </div>
                    <h3 class="text-lg font-bold text-white mb-2"><i class="fa-solid fa-hard-drive mr-2 text-sky-400"></i>Conversor Bytes</h3>
                    <p class="text-slate-400 text-sm mb-4">Convierte Bytes a KB, MB y GB en tiempo real.</p>
                    <input type="number" id="units-input" value="1048576" class="w-full bg-slate-900 border border-slate-700 rounded p-2 text-xs text-white mb-4">
                </div>
                <div>
                    <button onclick="testUnits()" class="w-full bg-sky-600 hover:bg-sky-500 text-white font-medium py-2 rounded-lg transition text-sm mb-3">Convertir</button>
                    <pre id="units-output" class="text-xs font-mono bg-slate-950 p-2 rounded text-slate-400 min-h-[40px] overflow-x-auto">Estado: Esperando entrada...</pre>
                </div>
            </div>

        </div>
    </main>

    <script>
        async function testPassword() {
            const length = document.getElementById('pass-length').value;
            const res = await fetch(`/api/security/generate-password?length=${length}`);
            const data = await res.json();
            document.getElementById('pass-output').innerText = data.password || data.error;
        }

        async function testQR() {
            const text = document.getElementById('qr-text').value;
            if (!text) return alert('Ingresa un texto para el QR');
            
            const res = await fetch('/api/security/generate-qr', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({text})
            });

            if (res.ok) {
                const blob = await res.blob();
                const url = URL.createObjectURL(blob);
                document.getElementById('qr-output').innerHTML = `<img src="${url}" class="h-28 w-28 rounded">`;
            } else {
                const err = await res.json();
                document.getElementById('qr-output').innerText = err.error;
            }
        }

        async function testMonitor() {
            const url = document.getElementById('monitor-url').value;
            const out = document.getElementById('monitor-output');
            out.innerText = 'Consultando...';

            const res = await fetch('/api/monitor/check', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url})
            });

            const data = await res.json();
            out.innerText = JSON.stringify(data, null, 2);
        }

        async function testConverter() {
            const rawJson = document.getElementById('json-input').value;
            const out = document.getElementById('converter-output');
            try {
                const parsed = JSON.parse(rawJson);
                const res = await fetch('/api/converter/json-to-csv', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify(parsed)
                });
                
                if (res.ok) {
                    const blob = await res.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = 'converted.csv';
                    a.click();
                    out.innerText = 'CSV descargado con éxito.';
                } else {
                    const err = await res.json();
                    out.innerText = err.error;
                }
            } catch(e) {
                out.innerText = 'JSON inválido';
            }
        }

        async function testFormatter() {
            const raw = document.getElementById('fmt-input').value;
            const out = document.getElementById('fmt-output');
            try {
                const res = await fetch('/api/formatter/format-json', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: raw
                });
                const data = await res.json();
                out.innerText = data.formatted || data.error;
            } catch(e) { out.innerText = 'JSON no válido'; }
        }

        async function testCrypto() {
            const text = document.getElementById('hash-input').value;
            const out = document.getElementById('hash-output');
            const res = await fetch('/api/crypto/hash', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            out.innerText = JSON.stringify(data.hashes, null, 2);
        }

        async function testTextAnalyzer() {
            const text = document.getElementById('text-input').value;
            const out = document.getElementById('text-output');
            const res = await fetch('/api/text/analyze', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ text })
            });
            const data = await res.json();
            out.innerText = JSON.stringify(data.metrics, null, 2);
        }

        async function testJwt() {
            const token = document.getElementById('jwt-input').value;
            const out = document.getElementById('jwt-output');
            const res = await fetch('/api/jwt/decode', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ token })
            });
            const data = await res.json();
            out.innerText = JSON.stringify(data, null, 2);
        }

        async function testUnits() {
            const bytes = document.getElementById('units-input').value;
            const out = document.getElementById('units-output');
            const res = await fetch(`/api/units/bytes?bytes=${bytes}`);
            const data = await res.json();
            out.innerText = JSON.stringify(data.conversions, null, 2);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

if __name__ == '__main__':
    app.run(debug=True)