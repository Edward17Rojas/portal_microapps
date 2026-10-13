from flask import Flask, render_template_string
from apps.converter import converter_bp
from apps.security import security_bp
from apps.webhook import webhook_bp
from apps.monitor import monitor_bp

app = Flask(__name__)

# Registro de módulos
app.register_blueprint(converter_bp)
app.register_blueprint(security_bp)
app.register_blueprint(webhook_bp)
app.register_blueprint(monitor_bp)

DASHBOARD_HTML = """
<!DOCTYPE html>
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
            
            <!-- Targeta 1: Generador de Contraseñas -->
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

            <!-- Targeta 2: Generador de QR -->
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

            <!-- Targeta 3: Monitor de APIs -->
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
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

if __name__ == '__main__':
    app.run(debug=True)