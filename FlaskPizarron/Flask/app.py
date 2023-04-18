import ftplib
from flask import Flask, Response, flash, jsonify, redirect, render_template, request, send_file, url_for
from flask_uploads import UploadSet, configure_uploads, IMAGES
from ftplib import FTP
import base64
import hashlib
from PIL import Image, ImageGrab
import io
import os
from os.path import join, isfile
import numpy as np
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
import openpyxl
import cv2
from werkzeug.utils import secure_filename


app = Flask(__name__)

photos = UploadSet('photos', IMAGES)
app.config['UPLOADED_PHOTOS_DEST'] = 'Flask/static/img'
app.config['UPLOADED_MAPA_TXT'] = 'Flask/static/mapa-txt'
app.config['SECRET_KEY'] = 'tu clave secreta aquí'
app.config['ALLOWED_EXTENSIONS'] = {'txt'}



configure_uploads(app, photos)

contador_imagen = 0
contador_carpeta = 1

camara = cv2.VideoCapture(0)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    # mandarCorreos()
    return render_template('index.html')

@app.route('/galeria',  methods=['GET', 'PUT','DELETE'])
def galeria():
    dir_path = f'Flask/static/img'

    file_names = os.listdir(dir_path)

    return render_template('galeria.html', images=file_names)

# Ruta para modificar el nombre de una imagen
@app.route('/galeria/renombrar/<string:image>', methods=['PUT', 'GET'])
def rename(image):
    nuevo_nombre = request.args.get('nuevoNombre')
    os.rename(f'Flask/static/img/{image}', f'Flask/static/img/{nuevo_nombre}')
    return redirect(url_for('galeria'))



# Ruta para eliminar una imagen
@app.route('/galeria/borrar/<string:image>', methods=['DELETE', 'GET'])
def delete(image):
    os.remove(f'Flask/static/img/{image}')
    return redirect(url_for('galeria'))

@app.route('/pizarra')
def pizarra():
    return render_template('pizarra.html')


@app.route('/correo')
def correo():
    return render_template('correo.html')


@app.route('/despedida')
def despedida():
    return render_template('despedida.html')


@app.route('/prueba')
def prueba():
    return render_template('prueba.html')

@app.route('/composicion')
def composicion():

    return render_template("composicion.html")

@app.route('/composicion/<tipo>')
def composicionTipo(tipo):
    global contador_carpeta
    if tipo not in ['ladrillo', 'mapa']:
        return redirect('/composicion')
    if tipo == 'ladrillo':
        # imagenes = os.listdir('Flask/static/carpeta-img-1')
        dir_path = f'Flask/static/carpeta-img-{contador_carpeta}'

    # lista de nombres de archivo de imágenes
        file_names = os.listdir(dir_path)

        for filename in file_names[:]:
            if filename.startswith('correo'):
                file_names.remove(filename)

        def get_image_number(filename):
            if filename.startswith('imagen'):
                return int(filename.split('-')[1].split('.')[0])

        imagenes = sorted(file_names, key=get_image_number)
        print(imagenes)
        # if len(imagenes) > 0:
        #     last_image = imagenes.pop()

        return render_template("ladrillo.html", image_names=imagenes
                            #    , last_image=last_image
                            )
    # if tipo == 'mapa':
    #     dir_path = f'Flask/static/carpeta-img-{contador_carpeta}'

    #     # lista de nombres de archivo de imágenes
    #     file_names = os.listdir(dir_path)

    #     for filename in file_names[:]:
    #         if filename.startswith('correo'):
    #             file_names.remove(filename)

    #     def get_image_number(filename):
    #         if filename.startswith('imagen'):
    #             return int(filename.split('-')[1].split('.')[0])

    #     imagenes = sorted(file_names, key=get_image_number)
    #     print(imagenes)
    #     posiciones = {
    #         'imagen-01.png': {'top': 0, 'left': 0},
    #         'imagen-02.png': {'top': 72, 'left': 0},
    #         'imagen-03.png': {'top': 72, 'left': 128},
    #         'imagen-04.png': {'top': 0, 'left': 128},
    #         'imagen-05.png': {'top': 144, 'left': 128},
    #         'imagen-06.png': {'top': 0, 'left': 256},
    #         'imagen-07.png': {'top': 144, 'left': 256},
    #         'imagen-08.png': {'top': 72, 'left': 256},
    #         'imagen-09.png': {'top': 144, 'left': 0},
    #         # 'imagen-10.png': {'top': 144, 'left': 128},
    #         # 'imagen-11.png': {'top': 144, 'left': 128},
    #         # 'imagen-12.png': {'top': 144, 'left': 128},
    #         # 'imagen-13.png': {'top': 144, 'left': 128},
    #         # 'imagen-14.png': {'top': 144, 'left': 128},
    #         # 'imagen-15.png': {'top': 144, 'left': 128},
    #         # 'imagen-16.png': {'top': 144, 'left': 128},
    #         # ... otros valores de posicion ...

    #         # * Reemplazar la variable posiciones por una que lea el txt y saque de ahí las posiciones.
    #         # * Esperar a que Leo diseñe para hacer las posiciones de 2*3, 2*2, 

    #     }
    #     def crear_diccionario_posiciones(imagenes, posiciones):
    #         posiciones_recortadas = {}
    #         for imagen in imagenes:
    #             if imagen in posiciones:
    #                 posiciones_recortadas[imagen] = posiciones[imagen]
    #         return posiciones_recortadas

    #     posiciones_recortadas = crear_diccionario_posiciones(imagenes, posiciones)

    #     return render_template("mapa.html", image_names=imagenes, posiciones=posiciones_recortadas)
    
@app.route('/composicion/mapeado', methods=['GET', 'POST'])
def mapa2():   
    # Obtener la lista de archivos de texto existentes
    txt_files = os.listdir(app.config['UPLOADED_MAPA_TXT'])
    img_files = os.listdir(app.config['UPLOADED_PHOTOS_DEST'])
    
    if request.method == 'POST':
        # Manejar la subida de archivos de texto
        file = request.files['txtInput']
        if file.filename == '':
            mensaje = 'No se ha seleccionado ningún archivo.'
            return render_template('mapeado.html', mensaje=mensaje, alerta='danger', files=txt_files, images=img_files)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_content = file.stream.read().decode('utf-8')
            txt_hash = hashlib.sha256(file_content.encode('utf-8')).hexdigest()
            for existing_file in os.listdir(app.config['UPLOADED_MAPA_TXT']):
                with open(os.path.join(app.config['UPLOADED_MAPA_TXT'], existing_file), 'rb') as f:
                    existing_hash = hashlib.sha256(f.read()).hexdigest()
                    if existing_hash == txt_hash:
                        mensaje = f'El archivo de texto "{filename}" ya existe con otro nombre, se llama "{existing_file}".'
                        return render_template('mapeado.html', mensaje=mensaje, alerta='warning', files=txt_files, images=img_files)
            file.stream.seek(0)
            file.save(os.path.join(app.config['UPLOADED_MAPA_TXT'], filename))
            mensaje = 'El archivo se ha subido correctamente.'
            return render_template('mapeado.html', mensaje=mensaje,alerta='success', files=txt_files, images=img_files)
        else:
            mensaje = 'El archivo seleccionado no es un archivo de texto permitido.'
            return render_template('mapeado.html', mensaje=mensaje, alerta='danger', files=txt_files, images=img_files)
    
    # Si se está haciendo una solicitud GET, simplemente renderizar el template
    return render_template('mapeado.html', files=txt_files, images=img_files)

@app.route('/composicion/mapa/<imagenfondo>/<texto>')
def composicion_mapa(imagenfondo, texto):
    dir_path = f'Flask/static/img-mapa'

    # lista de nombres de archivo de imágenes
    file_names = os.listdir(dir_path)

    def get_image_number(filename):
        if filename.startswith('imagen'):
            return int(filename.split('-')[1].split('.')[0])

    imagenes = sorted(file_names, key=get_image_number)
    # procesar la imagen
    # ... procesar la imagen ...

    txt = app.config['UPLOADED_MAPA_TXT'] + '/' + texto

    # procesar el texto
    # ... procesar el texto ...
    with open(txt, 'r') as archivo:
        contenido = archivo.read()
        # print(contenido)
    posiciones = eval(contenido)
    print(posiciones)
    def crear_diccionario_posiciones(imagenes, posiciones):
        posiciones_recortadas = {}
        for imagen in imagenes:
            if imagen in posiciones:
                posiciones_recortadas[imagen] = posiciones[imagen]
        return posiciones_recortadas

    posiciones_recortadas = crear_diccionario_posiciones(imagenes, posiciones)
    return render_template("mapa.html", image_names=imagenes, posiciones=posiciones_recortadas,fondo=imagenfondo)

    # posiciones = {
    #         'imagen-01.png': {'top': 0, 'left': 0},
    #         'imagen-02.png': {'top': 72, 'left': 0},
    #         'imagen-03.png': {'top': 72, 'left': 128},
    #         'imagen-04.png': {'top': 0, 'left': 128},
    #         'imagen-05.png': {'top': 144, 'left': 128},
    #         'imagen-06.png': {'top': 0, 'left': 256},
    #         'imagen-07.png': {'top': 144, 'left': 256},
    #         'imagen-08.png': {'top': 72, 'left': 256},
    #         'imagen-09.png': {'top': 144, 'left': 0},
    #         # 'imagen-10.png': {'top': 144, 'left': 128},
    #         # 'imagen-11.png': {'top': 144, 'left': 128},
    #         # 'imagen-12.png': {'top': 144, 'left': 128},
    #         # 'imagen-13.png': {'top': 144, 'left': 128},
    #         # 'imagen-14.png': {'top': 144, 'left': 128},
    #         # 'imagen-15.png': {'top': 144, 'left': 128},
    #         # 'imagen-16.png': {'top': 144, 'left': 128},
    #         # ... otros valores de posicion ...

    #         # * Reemplazar la variable posiciones por una que lea el txt y saque de ahí las posiciones.
    #         # * Esperar a que Leo diseñe para hacer las posiciones de 2*3, 2*2, 

    #     }

    # construir el diccionario de posiciones
    # ... construir el diccionario ...

    # mostrar la composición
    # return render_template('mapa.html', image_names=img, posiciones=posiciones)


@app.route('/composicion/estructurada')
def composicionEstructura():
    
    return render_template('estructura.html')

@app.route('/composicion/estructurada/<columna>x<fila>')
def composicionEstructurada(columna,fila):
    
    return render_template('estructurada.html',columna=columna, fila=fila)

@app.route('/visualizador', methods=['GET', 'POST'])
def visualizador():
    if request.method == 'POST' and 'photo' in request.files:
        image = request.files['photo']
        image_hash = hashlib.sha256(image.read()).hexdigest()
        image.seek(0)
        for filename in os.listdir(app.config['UPLOADED_PHOTOS_DEST']):
            with open(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename), 'rb') as f:
                existing_hash = hashlib.sha256(f.read()).hexdigest()
                if existing_hash == image_hash:
                   return render_template('visualizador.html', mensaje=f'La imagen "{image.filename}" ya existe con otro nombre, se llama "{filename}".', alerta='warning')

        filename = photos.save(image)
        return redirect(url_for('cuadricula', filename=filename))
    if request.method == 'GET':
        return render_template('visualizador.html')


@app.route('/cuadricula/<filename>')
def cuadricula(filename):
    print(f'Filename: {filename}')
    return render_template('cuadricula.html', filename=filename)

@app.route('/cuadricula')
def cuadriculaIMG():
    return render_template('cuadricula.html')


@app.route('/admin')
def admin():
    folder_path = f'Flask/static/carpeta-img-{contador_carpeta}'
    onlyfiles = [f for f in os.listdir(
        folder_path) if isfile(join(folder_path, f))]
    onlyfiles.pop(0)
    return render_template('admin.html', files=onlyfiles)


@app.route('/admin/delete/<filename>', methods=['POST'])
def delete_image(filename):
    folder_path = f'Flask/static/carpeta-img-{contador_carpeta}'
    file_path = os.path.join(folder_path, filename)
    os.remove(file_path)
    return redirect(url_for('admin'))


@app.route('/obtener_forma', methods=['POST'])
def obtener_forma():
    botones = request.get_json()
    print(botones)
    archivo = open("cuadricula.txt", "w")
    archivo.write(str(botones))
    archivo.close()
    return send_file("cuadricula.txt", as_attachment=True)


@app.route('/capturar_imagen', methods=['POST'])
def capturar_imagen():
    # Capturamos la imagen de la pantalla
    imagen = ImageGrab.grab()
    # Guardamos la imagen en la carpeta "capturas"
    ruta = os.path.join(os.getcwd(), 'capturas')
    if not os.path.isdir(ruta):
        os.mkdir(ruta)

    nombre_archivo = datetime.now().strftime("%Y%m%d_%H%M%S") + ".png"
    ruta_completa = os.path.join(ruta, nombre_archivo)
    imagen.save(ruta_completa, 'PNG')
    # Devolvemos una respuesta con un mensaje indicando que se ha capturado y guardado la imagen
    # return "La imagen se ha capturado y guardado con éxito en: " + ruta_completa
    return redirect(url_for('composicion'))

@app.route('/webcam')
def webcam():
    return render_template('webcam.html')

def obtener_frame_camara():
    ok, frame = camara.read()
    if not ok:
        return False, None
    # Codificar la imagen como JPG
    _, bufer = cv2.imencode(".jpg", frame)
    imagen = bufer.tobytes()
    return True, imagen


# Una función generadora para stremear la cámara
def generador_frames():
    while True:
        ok, imagen = obtener_frame_camara()
        if not ok:
            break
        else:
            # Regresar la imagen en modo de respuesta HTTP
            yield b"--frame\r\nContent-Type: image/jpeg\r\n\r\n" + imagen + b"\r\n"

# Más tarde...

# Cuando visiten la ruta
@app.route("/streaming_camara")
def streaming_camara():
    return Response(generador_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/correogoli')
def mandarCorreos2():
    global contador_carpeta
    correo_from = 'joseantonio.golineuro@gmail.com'
    password = 'lrtjlfkwvdothfeg'
    correo_to = 'joseantonio.golineuro@gmail.com'
    correo_cc = 'joseantoniocastanedapavon@gmail.com'
    img_a_enviar = f'Flask/static/carpeta-img-{contador_carpeta}/imagen-0.png'
    nombre_img_enviada = 'GoliNeuroIMG.png'

    html = """\
<!DOCTYPE html>
<html lang="es">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link
        href="https://fonts.googleapis.com/css2?family=Comfortaa&family=Open+Sans&family=Roboto:wght@100;300&display=swap"
        rel="stylesheet">
    <link href="https://fonts.cdnfonts.com/css/helvetica-255" rel="stylesheet">
    <title>Firma</title>
</head>

<body>
    <table width="800px" height="200" border="0" cellspacing="0" cellpadding="0" 
        style="
        background-image:url(https://i.ibb.co/F4FxSRv/Fondo.png);
        background-size:800px 550px;
        background-repeat: none;
        color:white; 
        margin:5px;">
        <tr>
            <td width="380px">
                <div style="margin-bottom: 34px;">
                    <p style="margin-left:32px; white-space: nowrap; margin-top: 0%;margin-bottom: 0%;
                    font-size:21px; font-family: 'Comfortaa', 'Helvetica', 'Open Sans', sans-serif">
                        JOSÉ ANTONIO CASTAÑEDA</p>
                    <p href="" style="margin-left:32px; margin-top: 10px; 
                    color:#c585c2;text-decoration: none;
                    font-size:14.5px; font-family: 'Roboto', 'Helvetica', 'Open Sans', sans-serif;">
                        Desarrollador IT</p>
                </div>
            </td>
            <td width="250px">
                <div>
                    <div style="display: flex; align-items: center; margin-bottom:10px;">
                        <a href="mailto:jacastaneda@golineuro.es">
                            <!-- Icono Correo -->
                            <img src="https://i.ibb.co/fd2CwdZ/Icono-Correo.png" width="19" height="14" style="margin-right: 10px;"">
                            <!-- Icono Correo -->
                        </a>

                        <a style="text-decoration: none; color:white;margin-bottom:2px; 
                        font-size: 18px; font-family:'Roboto', 'Helvetica', 'Open Sans', sans-serif;"
                            href="mailto:jacastaneda@golineuro.es">jacastaneda@golineuro.es</a>
                    </div>

                    <div style="display: flex; align-items: center; margin-bottom:10px;">
                        <a href="tel:+34951089354">
                            <!-- Icono Teléfono -->
                            <img src="https://i.ibb.co/BGmTBLb/Icono-Tel-fono.png" width="18" height="18" style="margin-right: 10px;">
                            <!-- Icono Teléfono -->
                        </a>
                        <a style="text-decoration: none;color:white;margin-bottom:2px; 
                        font-size: 18px; font-family:'Roboto', 'Helvetica', 'Open Sans', sans-serif;"
                            href="tel:+34951089354">+34 951 08 93 54</a>
                    </div>

                    <div style="display: flex; align-items: center; ">
                        <a href="https://golineuro.es/" target="_blank">
                            <!-- Icono Web -->
                            <img src="https://i.ibb.co/JvNrVkY/Icono-Web.png" width="19.5" height="14.5" style="margin-right: 10px;">
                            <!-- Icono Web -->
                        </a>
                        <a style="text-decoration: none;color:white;margin-bottom:2px; 
                        font-size: 18px; font-family:'Roboto', 'Helvetica', 'Open Sans', sans-serif;"
                        href="https://golineuro.es/" target="_blank">golineuro.es</a>
                    </div>
                </div>
            </td>
            <td width="170px">
                <div style="margin-top: 15px; margin-bottom:20px;">
                    <a href="https://golineuro.es/" target="_blank">
                        <!-- Goli -->
                        <img src="https://i.ibb.co/2hXqkLS/Imagen-Goli.png" width="122" height="70" style="margin-bottom:50px;">
                        <!-- Goli -->
                    </a>
                </div>
            </td>
        </tr>
    </table>
</body>

</html>
            """

    image_email = MIMEMultipart()
    image_email['From'] = correo_from
    image_email['To'] = correo_to
    dia = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'
    image_email['Subject'] = f'Imagen conjunta Goli Neuromarketing de fecha: {dia}'

    text = MIMEText(
        """
Desde el equipo de Goli te hacemos entrega de este collage de imágenes en el que participaste.

Tu imagen es la que se encuentra adjunta en este correo.

    """
    )
    image_email.attach(text)

    image_email.attach(MIMEText(html, 'html', 'utf-8'))

    with open(img_a_enviar, 'rb') as f:
        img = MIMEImage(f.read(), name=nombre_img_enviada)
        image_email.attach(img)

    smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
    smtp_server.starttls()
    smtp_server.login(correo_from, password)
    smtp_server.sendmail(image_email['From'], [
                         image_email['To']], image_email.as_string())
    smtp_server.quit()

    def envioTermCond():
        msg = MIMEMultipart()
        msg['From'] = correo_from
        msg['To'] = correo_to
        msg['CC'] = correo_cc
        msg['Subject'] = 'Confirma los terminos de uso y servicios'
        msg.attach(MIMEText(
            'Por favor, confirma los términos de condiciones de uso con el siguiente elnace: https://golineuro.es/'))
        msg.attach(MIMEText(
            """

Los terminos de condiciones de uso son los siguientes: 
...
...
...

"""
        ))
        msg.attach(MIMEText(html, 'html', 'utf-8'))

        smtp_server = smtplib.SMTP('smtp.gmail.com', 587)
        smtp_server.starttls()
        smtp_server.login(correo_from, password)

        smtp_server.sendmail(
            msg['From'], [msg['To'], msg['CC']], msg.as_string())

        smtp_server.quit()

    # envioTermCond()
        # Espera de 1 hora
        # time.sleep(3600)

    return ('Correo mandado')


# TODO: encadenar toda la maquinaría, cuando se realice el proceso de crear la imagen y luego de verificación de correo, al pasar a la pantalla de despedida que
# TODO: se trate la imágen para optimizarla, y al terminar llame a otra función que mande la imagen a una lista de imagenes, se recargue la pantalla de composición con las imágenes
# TODO: y la última que realice una animación y se quede fija en su sítio.

@app.route("/composicion", methods=["POST"])
def refresh_composicion():
    # Lógica para actualizar la composición
    # ...

    return jsonify({"success": True}), 200


@app.route('/ultimo_archivo')
def ultimoArchivo():
    global contador_carpeta
    carpeta = f'Flask/static/carpeta-img-{contador_carpeta}'
    contenido = os.listdir(carpeta)
    archivo = contenido[len(contenido)-1]
    # archivo = contenido[2]
    print(f"El ultimo archivo subido en la carpeta {carpeta} es {archivo}")
    return archivo


def borrarArchivoEspera(archivo):
    try:
        os.remove(archivo)

    except FileNotFoundError:
        mensaje = 'El archivo de imagen no existe pero la imagen se ha tratado'
        print(mensaje)


@app.route('/borrar-archivo-espera')
def borrarArchivoEspera():
    try:
        global contador_imagen
        archivo = (f'Flask/static/images/imagen-{contador_imagen}.png')
        os.remove(archivo)
        mensaje = 'Imagen borrada con exito'

    except FileNotFoundError:
        mensaje = 'El archivo de imagen no existe pero la imagen se ha tratado'
        print(mensaje)
        return render_template('moderador.html', mensaje=mensaje)

    return render_template('moderador.html', mensaje=mensaje)


@app.route('/borrar_imagen', methods=['POST'])
def borrar_imagen():
    data_uri = request.form['data']
    print(data_uri)
    # filename = request.form['filename']
    # filepath = os.path.join('static', f'carpeta-img-{contador_carpeta}', data_uri)
    # print()
    filepath = f'Flask/static/carpeta-img-{contador_carpeta}/{data_uri}'
    os.remove(filepath)
    return jsonify({'mensaje': 'Imagen borrada correctamente.'})


@app.route('/tratar-imagen')
def tratarImagen():

    try:
        global contador_imagen, contador_carpeta
        archivo_inicio = (f'Flask/static/images/imagen-{contador_imagen}.png')
        archivo_final = (
            f'Flask/static/carpeta-img-{contador_carpeta}/imagen-{contador_imagen}.png')

        # Cargar la imagen y convertirla en una matriz numpy
        img = Image.open(archivo_inicio).convert('RGBA')
        arr = np.array(img)

        # Crear una máscara para identificar la línea
        mask = np.all(arr[:, :, :3] == (255, 255, 255), axis=2)

        # Crear una copia de la imagen original y reemplazar los píxeles de la línea con el nuevo color

        new_arr = np.copy(arr)
        # cambiar la linea roja por verde
        new_arr[:, :, :3][mask] = (255, 35, 60)

        # Crear una matriz con un fondo de color azul y del mismo tamaño que la imagen original
        background = np.zeros_like(new_arr)
        background[:] = (200, 200, 55, 255)

        # Combinar la imagen modificada con el fondo azul utilizando la máscara de transparencia de la imagen
        background[mask] = new_arr[mask]

        # Guardar la imagen resultante
        new_img = Image.fromarray(background, mode='RGBA')
        # new_img = Image.fromarray(new_arr, mode='RGBA')
        # new_img.thumbnail((128, 72), Image.Resampling.LANCZOS)

        # quality_val = 100

        new_img.save(archivo_final)

        borrarArchivoEspera()

        contador_imagen += 1

        mensaje = 'Imagen guardada'

        return render_template('moderador.html', mensaje=mensaje)

    except FileNotFoundError:
        mensaje = 'El archivo de imagen no existe'
    except Exception as e:
        mensaje = 'Se produjo un error al tratar la imagen: ' + str(e)

    return render_template('moderador.html', mensaje=mensaje)


@app.route('/guardar_imagen', methods=['POST'])
def guardar_imagen():
    global contador_imagen
    # print(os.listdir())
    data_uri = request.form['data']
    image_data = base64.b64decode(data_uri.split(',')[1])
    image = Image.open(io.BytesIO(image_data))
    image.save(
        f'Flask/static/carpeta-img-{contador_carpeta}/imagen-{contador_imagen}.png')
    contador_imagen += 1

    return 'Imagen guardada correctamente!'


@app.route('/correo-usuario', methods=['POST'])
def correoUsuario():
    global contador_carpeta
    archivo_txt = (f'Flask/static/carpeta-img-{contador_carpeta}/correos.txt')
    correo = request.form['correo']
    print(correo)
    with open(archivo_txt, "a+") as archivo:
        archivo.write(correo+"\n")

    print("El correo ha sido guardado en el archivo.")

    # Guardar el correo en la base de datos o hacer lo que sea necesario
    return 'OK'


@app.route('/latest-image')
def latest_image():

    archivo = ultimoArchivo()
    print(archivo)
    return jsonify({'url': f'{archivo}'})


def login():
    servidor = "ftp.golineuro.es"
    contraseña = "6fPizarra$$"
    usuario = "totemboard@golineuro.es"

    try:
        ftp = FTP(servidor, usuario, contraseña)
        print("Conexión establecida")
        return ftp

    except ftplib.all_errors as e:
        print(f'Error al conectarse a {servidor}: {e}')
        return None


def refrescarFtp(ftp):
    contenido = []
    ftp.retrlines('LIST', contenido.append)
    ftp.dir = contenido
    last = len(contenido) - 1
    primer_archivo = contenido[2].split(' ')[-1]
    print(primer_archivo)
    ultimo_archivo = contenido[last].split(' ')[-1]
    print(ultimo_archivo)
    # b = a.split(' ')[-1]
    return ultimo_archivo


def mostrarArchivos(ftp, carpeta):
    ftp.cwd(carpeta)
    archivos = ftp.nlst()  # obtiene una lista de los nombres de los archivos en la carpeta

    for archivo in archivos:
        if archivo.startswith('imagen-'):
            print(archivo)


def conexionYDescargaFTP():

    try:
        ftp = login()
        print("Conexión realizada")
        print("Estamos en la carpeta " + ftp.pwd())
        ftp.dir()
        with open('Flask/static/prueba.xlsx', 'wb') as archivo_local:
            ftp.retrbinary('RETR prueba.xlsx', archivo_local.write)
        # ftp.cwd('Imagenes')
        # ftp.dir()
        # files = ftp.nlst()

        # if len(files) > 0:
        #     first_file = files[0]
        #     print("El nombre del primer archivo en la carpeta '{}' es '{}'.".format('Imagenes', first_file))
        # else:
        #     print("La carpeta '{}' está vacía.".format('Imagenes'))
    except:
        ...
        # Sorpresa      #f25855 rgb(242,88,85)
        # Entusiasmo    #ef903d rgb(239,144,61)
        # Admiracion    #f4de6d rgb(244,222,109)
        # Calma         #397371 rgb(57,115,113)
        # Relax         #55bfac rgb(85,191,172)
        # Gozo          #168ee1 rgb(22,142,225)
        # Bienestar     #4d47eb rgb(77,71,235)
        # Armonia       #7e4de8 rgb(126,77,232)
        # Alegria       #9241e7 rgb(146,65,231)
        # Diversion     #ef7998 rgb(239,121,152)


def excel():
    workbook = openpyxl.load_workbook(f'Flask/static/prueba.xlsx')
    hoja = workbook.active

    def colores(numero):
        colores = [(242, 88, 85), (239, 144, 61), (244, 222, 109), (57, 115, 113), (85, 191, 172), (22, 142, 225),
                   (77, 71, 235), (126, 77, 232), (146, 65, 231), (239, 121, 152)]

        return colores[numero % len(colores)]

    for fila in hoja.iter_rows(min_row=1, max_row=1):
        for celda in fila:
            if celda.value is None:
                continue
            try:
                valor = int(celda.value)
            except ValueError:
                valor = 0
            print(f"{valor} {colores(valor)}", end=" ")
        print()


def leerCorreos():
    # Abre el archivo de texto y lee los correos electrónicos en cada línea
    with open('Flask/static/carpeta-img-1/correos.txt', 'r') as archivo:
        lineas = archivo.readlines()

    # Crea un arreglo para almacenar los correos electrónicos
    correos = []

    # Agrega cada correo electrónico a la lista
    for linea in lineas:
        # Elimina cualquier espacio en blanco al inicio o al final de la línea
        correos.append(linea.strip())

    # Imprime la lista de correos electrónicos
    return correos


def mandarCorreos():
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "joseantonio.golineuro@gmail.com"
    smtp_password = "lrtjlfkwvdothfeg"

    # Lista de destinatarios (correo electrónico oculto)
    destinatarios = leerCorreos()

    # Agrega los detalles del correo electrónico
    mensaje = MIMEMultipart()
    dia = f'{datetime.now().day}/{datetime.now().month}/{datetime.now().year}'
    mensaje["Subject"] = f'Imagen conjunta Goli Neuromarketing de fecha: {dia}'
    mensaje["From"] = "joseantonio.golineuro@gmail.com"
    mensaje["Bcc"] = ", ".join(destinatarios)

    # Carga la imagen en memoria
    with open('Flask/static/firma.png', 'rb') as file:
        imagen_data = file.read()

    # Agrega la imagen al mensaje con la etiqueta 'cid'
    imagen = MIMEImage(imagen_data, name='firma.png')
    imagen.add_header('Content-ID', '<firma>')
    mensaje.attach(imagen)

    # Crea el mensaje de correo electrónico que enviarás
    cuerpo = MIMEText("""
    <html>
        <body>
            <p>Desde el equipo de Goli te hacemos entrega de este collage de imágenes en el que participaste.</p>
            <p>Muchas gracias por participar.</p>
            <img src="cid:firma" alt="firma" width="800px" height="200">
        </body>
    </html>
    """, 'html', 'utf-8')

    mensaje.attach(cuerpo)

    with open('capturas/collage1.png', 'rb') as file:
        imagen_firma = MIMEImage(file.read())
        imagen_firma.add_header('Content-Disposition',
                                'attachment', filename='collage.png')
        mensaje.attach(imagen_firma)

    # Crea la conexión SMTP y autentica con las credenciales
    smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
    smtp_conn.starttls()
    smtp_conn.login(smtp_username, smtp_password)

    # Envía el correo electrónico a todos los destinatarios
    smtp_conn.sendmail(smtp_username, destinatarios, mensaje.as_string())

    # Cierra la conexión SMTP
    smtp_conn.quit()

    print('Mandado')


if __name__ == '__main__':
    app.run(debug=True)
