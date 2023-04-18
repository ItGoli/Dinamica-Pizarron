# En una aplicación Flask, no es posible limpiar el canvas que se utiliza en la URL /pizarra directamente desde la URL /moderador. Sin embargo, puedes utilizar una solución que involucre el uso de una variable global o el almacenamiento en caché para comunicar el estado de la pizarra entre ambas URL.

# Por ejemplo, puedes utilizar una variable global llamada "canvas" que se inicializa en la URL /pizarra y se actualiza a medida que el usuario dibuja en ella. Luego, en la URL /moderador, puedes acceder a esta variable global y actualizarla para borrar el contenido de la pizarra.

# A continuación se muestra un ejemplo de cómo podrías implementar esto en Flask:

# python
# Copy code
from flask import Flask, render_template, make_response

app = Flask(__name__)

# Inicializar la variable global del canvas
canvas = ""

@app.route('/pizarra')
def pizarra():
    return render_template('pizarra.html')

@app.route('/moderador')
def moderador():
    # Acceder a la variable global del canvas y limpiar su contenido
    global canvas
    canvas = ""
    return render_template('moderador.html')

@app.route('/actualizar-canvas', methods=['POST'])
def actualizar_canvas():
    # Actualizar la variable global del canvas con el nuevo contenido
    global canvas
    request = make_response
    canvas = request.form['canvas']
    return 'Canvas actualizado correctamente'

@app.route('/obtener-canvas')
def obtener_canvas():
    # Devolver el contenido actual del canvas como respuesta
    global canvas
    return canvas


# * Paginas SVG
# https://loading.io/pattern/
# https://loading.io/background/ 
# https://bgjar.com/
# https://www.svgbackgrounds.com/
# https://www.freepik.com/free-photos-vectors/svg-background

# https://www.vecteezy.com/free-vector/background-svg

# En este ejemplo, la URL /pizarra renderiza una plantilla HTML que contiene el canvas en el que el usuario puede dibujar. Cuando el usuario dibuja en el canvas, la acción se envía a la URL /actualizar-canvas a través de una petición POST. Esta URL actualiza la variable global del canvas con el contenido del canvas actual.

# La URL /obtener

# Aquí te dejo algunas ideas creativas para hacer más animaciones en CSS para mover imágenes:

# Animación de rebote: Haz que la imagen rebote en el lugar usando la propiedad transform: translateY(-50%) y la función cubic-bezier() para un efecto más suave.

# Rotación de la imagen: Haz que la imagen rote en el lugar usando la propiedad transform: rotate() y la función ease-in-out para un efecto más suave.

# Desvanecimiento de la imagen: Haz que la imagen se desvanezca mientras se mueve en el lugar usando la propiedad opacity y la función ease-out.

# Zoom de la imagen: Haz que la imagen se acerque y se aleje usando la propiedad transform: scale() y la función ease-in-out.

# Efecto de "perspectiva": Haz que la imagen se mueva en 3D usando la propiedad transform: perspective() y las funciones rotateX() y rotateY().

# Animación de oscilación: Haz que la imagen se mueva hacia adelante y hacia atrás como un péndulo usando la propiedad transform: translateX() y la función ease-in-out.

# Animación de rebote elástico: Haz que la imagen rebote varias veces como una pelota de goma usando la propiedad transform: scaleY() y la función cubic-bezier().

# Animación de escalada: Haz que la imagen se mueva hacia arriba y hacia abajo en el lugar usando la propiedad transform: translateY() y la función ease-in-out.

# Animación de cambio de tamaño: Haz que la imagen cambie de tamaño mientras se mueve en el lugar usando la propiedad transform: scale() y la función ease-out.

# Animación de movimiento continuo: Haz que la imagen se mueva en un patrón continuo usando la propiedad transform: translate() y la función linear.

# Puedes experimentar con estas ideas y crear tus propias animaciones personalizadas. ¡Diviértete!

"""
<div id="last-image-espiral"></div>


#last-image-espiral {
  position: absolute;
}

.animacion-derecha {
  animation: spiral-image-derecha 3s linear infinite;
}

.animacion-izquierda {
  animation: spiral-image-izquierda 3s linear infinite;
}

@keyframes spiral-image-derecha {
  0% {
    transform: rotate(0deg) translateX(0px) translateY(0px);
  }

  50% {
    transform: rotate(1080deg) translateX(200px) translateY(200px);
  }

  100% {
    transform: rotate(0deg) translateX(0px) translateY(0px);
  }
}

@keyframes spiral-image-izquierda {
  0% {
    transform: rotate(0deg) translateX(0px) translateY(0px);
  }

  50% {
    transform: rotate(1080deg) translateX(-200px) translateY(-200px);
  }

  100% {
    transform: rotate(0deg) translateX(0px) translateY(0px);
  }
}


var elemento = document.getElementById("last-image-espiral");

if (elemento.getBoundingClientRect().left < window.innerWidth / 2) {
  elemento.classList.add("animacion-izquierda");
} else {
  elemento.classList.add("animacion-derecha");
}

https://cubenode.com/hosting-reseller

const canvas = document.createElement('canvas');
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
document.body.appendChild(canvas);

const ctx = canvas.getContext('2d');

// Dibujar el borde
ctx.lineWidth = 10;
ctx.strokeRect(300, 200, window.innerWidth - 600, window.innerHeight - 400);

<!-- <div> INTENTO AUTOMATIZACION
    {% set images_per_row = 14 %}
  {% set rows = image_names|batch(images_per_row)|list %}
  {% set last_image = last_image %}
  
  {% for row in rows %}
    <div {% if loop.index is even %}class="par"{% else %}class="impar"{% endif %}>
      {% for image_name in row %}
        {% if loop.last and loop.index < images_per_row-1 %}
          <img src="{{ url_for('static', filename='carpeta-img-1/' + image_name) }}" alt="{{ image }}" class="image">
          <img src="{{ url_for('static', filename='carpeta-img-1/' + last_image) }}" alt="{{ last_image }}" class="image last-image">
        {% else %}
          <img src="{{ url_for('static', filename='carpeta-img-1/' + image_name) }}" alt="{{ image }}" class="image">
        {% endif %}
      {% endfor %}
    </div>
  {% endfor %}
  </div> -->

  .par{
      display: flex;
      margin-left: 96px;
    }

    .impar{
      display: flex;
      margin-left: 32px;
    }

    <!DOCTYPE html>
<html>
  <head>
    <meta charset="UTF-8">
    <title>Enviar formulario automáticamente</title>
  </head>
  <body {% if len(imagenes) > 185 %}onload="document.getElementById('capturar_imagen_form').submit()" {% endif %}>
    <form id="capturar_imagen_form" action="/capturar_imagen" method="POST" enctype="multipart/form-data">
    </form>
  </body>
</html>


import smtplib
from email.mime.text import MIMEText

# Configura tus credenciales SMTP
smtp_server = "smtp.gmail.com"
smtp_port = 587
smtp_username = "tu_correo@gmail.com"
smtp_password = "tu_password"

# Lista de destinatarios (correo electrónico oculto)
destinatarios = ["usuario1@gmail.com", "usuario2@gmail.com", "usuario3@gmail.com"]

# Crea el mensaje de correo electrónico que enviarás
mensaje = MIMEText("Este es el contenido del correo.")

# Agrega los detalles del correo electrónico
mensaje["Subject"] = "Asunto del correo"
mensaje["From"] = "tu_correo@gmail.com"
mensaje["Bcc"] = ", ".join(destinatarios)

# Crea la conexión SMTP y autentica con las credenciales
smtp_conn = smtplib.SMTP(smtp_server, smtp_port)
smtp_conn.starttls()
smtp_conn.login(smtp_username, smtp_password)

# Envía el correo electrónico a todos los destinatarios
smtp_conn.sendmail(smtp_username, destinatarios, mensaje.as_string())

# Cierra la conexión SMTP
smtp_conn.quit()

"""