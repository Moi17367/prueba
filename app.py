import socket
from flask import Flask, render_template, request, send_file
import qrcode
from io import BytesIO

app = Flask(__name__)

# Base de datos simulada (en memoria)
ESTUDIANTES = {
    "1": {"nombre": "Carlos", "apellido": "Pérez", "cedula": "12345678", "mencion": "Informática"},
    "2": {"nombre": "María", "apellido": "Gómez", "cedula": "87654321", "mencion": "Electrónica"},
    "3": {"nombre": "Ana", "apellido": "Rodríguez", "cedula": "11223344", "mencion": "Administración"}
}

def obtener_ip_local():
    """Obtiene la IP local de tu PC para que el QR funcione en el celular."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

@app.route('/')
def index():
    # Pasamos el diccionario de estudiantes a la vista principal
    return render_template('index.html', estudiantes=ESTUDIANTES)

@app.route('/estudiante/<id_estudiante>')
def perfil(id_estudiante):
    estudiante = ESTUDIANTES.get(id_estudiante)
    if not estudiante:
        return "Estudiante no encontrado", 404
    return render_template('perfil.html', estudiante=estudiante)

@app.route('/qr/<id_estudiante>')
def generar_qr(id_estudiante):
    estudiante = ESTUDIANTES.get(id_estudiante)
    if not estudiante:
        return "No encontrado", 404
    
    # Construimos la URL usando la IP local y el puerto 5000
    ip_local = obtener_ip_local()
    url_perfil = f"http://{ip_local}:5000/estudiante/{id_estudiante}"
    
    # Generar el código QR
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(url_perfil)
    qr.make(fit=True)
    
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Guardar la imagen en memoria para enviarla directamente al HTML
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == '__main__':
    # Importante: host='0.0.0.0' permite que otros dispositivos (como tu celular) se conecten
    app.run(host='0.0.0.0', port=5000, debug=True)