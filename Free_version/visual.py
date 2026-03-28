from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget,QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QInputDialog, QMessageBox, QGraphicsOpacityEffect, QPlainTextEdit, QFileDialog
from PyQt5.QtCore import Qt, QPropertyAnimation, QParallelAnimationGroup, QProcess, pyqtSignal, QTimer
from PyQt5.QtGui import QIcon, QPalette, QBrush, QPixmap
from chatter import *
import webbrowser
import requests
import pygame
import sys

def aplicar_fondo(widget, ruta):
    pixmap = QPixmap(ruta)

    pixmap = pixmap.scaled(
        widget.size(),
        Qt.IgnoreAspectRatio,
        Qt.SmoothTransformation
    )

    paleta = QPalette()
    paleta.setBrush(QPalette.Window, QBrush(pixmap))

    widget.setPalette(paleta)
    widget.setAutoFillBackground(True)

def cargar_anuncio(label):
    try:
        response = requests.get(AD_URL, timeout=5)
        data = response.json()
        ad = random.choice(data["ads"])

        image_url = ad["image"]
        link = ad["url"]

        img_response = requests.get(image_url, timeout=5)
        pixmap = QPixmap()
        pixmap.loadFromData(img_response.content)

        label.setPixmap(pixmap)
        label.setAlignment(Qt.AlignCenter)

        def abrir_link(event):
            webbrowser.open(link)

        label.mousePressEvent = abrir_link

    except Exception as e:
        print("Error cargando anuncio:", e)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

app = QApplication(sys.argv)
Title = " <.mandium "
AD_URL = "https://raw.githubusercontent.com/b1u3b1ur/comandium-ads/main/ad.json"

pygame.init()
pygame.mixer.music.load(resource_path('free.mp3'))
pygame.mixer.music.set_volume(0.3)
pygame.mixer.music.play(loops=-1)

FONDO_GLOBAL = 'fondo.jpg'

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        aplicar_fondo(self, FONDO_GLOBAL)
        
        self.setWindowTitle('<.mandium')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;")
        self.resize(850, 480)
        
        self.label = QLabel(Title)
        self.label.setStyleSheet(
            "font-size: 86px;"
            "font-weight: bold;"
            "font-family: Consolas;"
            # "border: 2px solid #FFFFFF;"
        )
        self.label.setFixedSize(500, 100)
        
        self.but = QPushButton("Chatear")
        self.but.setStyleSheet(
            "border-radius: 5px;"
            "border: 1px solid #FFFFFF;"
        )
        self.but.setFixedSize(100, 40)
        self.but_2 = QPushButton("Crear servidor")
        self.but_2.setStyleSheet(
            "border-radius: 5px;"
            "border: 1px solid #FFFFFF;"
        )
        self.but_2.setFixedSize(100, 40)
        self.but_C = QPushButton()
        self.but_C.setIcon(QIcon(resource_path('confi.png')))
        self.but_C.setIconSize(QtCore.QSize(32, 32))
        
        self.but.clicked.connect(self.open_chat)
        self.but_2.clicked.connect(self.open_server)
        self.but_C.clicked.connect(self.config)
        
        self.setWindowIcon(QIcon(resource_path('i am a game theorist.png')))
        
        self.label_opacity_effect = QGraphicsOpacityEffect(self.label)
        self.button_opacity_effect = QGraphicsOpacityEffect(self.but)
        self.button_opacity_effect_2 = QGraphicsOpacityEffect(self.but_2)
        self.button_opacity_effect_3 = QGraphicsOpacityEffect(self.but_C)
        
        self.label.setGraphicsEffect(self.label_opacity_effect)
        self.but.setGraphicsEffect(self.button_opacity_effect)
        self.but_2.setGraphicsEffect(self.button_opacity_effect)
        self.but_C.setGraphicsEffect(self.button_opacity_effect_3)

        self.label_opacity_effect.setOpacity(0)
        self.button_opacity_effect.setOpacity(0)
        self.button_opacity_effect_2.setOpacity(0)
        self.button_opacity_effect_3.setOpacity(0)
        
        self.anim = QPropertyAnimation(self.label_opacity_effect, b"opacity")
        self.anim.setDuration(800)
        self.anim.setStartValue(0)
        self.anim.setEndValue(1)
        
        self.anim_2 = QPropertyAnimation(self.button_opacity_effect, b"opacity")
        self.anim_2.setDuration(800)
        self.anim_2.setStartValue(0)
        self.anim_2.setEndValue(1)
        
        self.anim_3 = QPropertyAnimation(self.button_opacity_effect_2, b"opacity")
        self.anim_3.setDuration(800)
        self.anim_3.setStartValue(0)
        self.anim_3.setEndValue(1)
        
        self.anim_4 = QPropertyAnimation(self.button_opacity_effect_3, b"opacity")
        self.anim_4.setDuration(800)
        self.anim_4.setStartValue(0)
        self.anim_4.setEndValue(1)
        
        self.mult_anim = QParallelAnimationGroup(self)
        self.mult_anim.addAnimation(self.anim)
        self.mult_anim.addAnimation(self.anim_2)
        self.mult_anim.addAnimation(self.anim_3)
        self.mult_anim.addAnimation(self.anim_4)
        
        v_line = QVBoxLayout()
        v_line.addWidget(self.but_C, alignment=Qt.AlignRight)
        v_line.addStretch()
        v_line.addWidget(self.label, alignment=Qt.AlignHCenter)
        v_line.addSpacing(40)
        v_line.addWidget(self.but, alignment=Qt.AlignHCenter)
        v_line.addSpacing(20)
        v_line.addWidget(self.but_2, alignment=Qt.AlignHCenter)
        v_line.addStretch()

        self.setLayout(v_line)
        self.mult_anim.start()
        
    def open_chat(self):
        self.chat_window = Chat()
        self.chat_window.show()
        MyWindow.close(self)
    
    def open_server(self):
        self.server = Server()
        self.server.show()
        ventanas = QApplication.topLevelWidgets()

        especificas = [v for v in ventanas if isinstance(v, Server) and v.isVisible()]

        if len(especificas) > 1:
            for i in range(len(especificas) - 1):
                especificas[i].close()
    
    def config(self):
        self.confi_window = Confi()
        self.confi_window.show()
        ventanas = QApplication.topLevelWidgets()

        especificas = [v for v in ventanas if isinstance(v, Confi) and v.isVisible()]

        if len(especificas) > 1:
            for i in range(len(especificas) - 1):
                especificas[i].close()
        
class Chat(QWidget):
    def __init__(self):
        super().__init__()
        aplicar_fondo(self, FONDO_GLOBAL)
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_chat)
        self.timer.start(100) 
        
        self.setWindowTitle('Chat Window')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;")
        self.setWindowIcon(QIcon(resource_path('i am a game theorist.png')))
        self.resize(850, 480)
        
        self.puerto = None
        self.indice_mensajes = 0
        
        self.label = QLabel("<.mandium [Alpha 2.2.1]\nSA.54 - Gracias por usar <.mandium")
        self.label.setStyleSheet("font-size: 13px")
        
        self.label_2 = QLabel(f" >> {Username}")
        
        self.button = QPushButton()
        self.button.setIcon(QIcon(resource_path('confi.png')))
        self.button.setIconSize(QtCore.QSize(32, 32))
        
        self.button_2 = QPushButton(">> puerto de acceso:")
        
        self.cmd_output = QPlainTextEdit()
        self.cmd_output.setReadOnly(True)
        self.cmd_output.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: 1px solid white;"
            "padding: 5px;"
        )

        self.cmd_input = QLineEdit()
        self.cmd_input.setPlaceholderText("Escribe tu mensaje (escribe 'q' para salir):")
        self.cmd_input.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "border: 1px solid white;"
            "padding: 5px;"
        )
        
        self.cmd_output.appendPlainText("Chat iniciado...\n")
        
        self.button.clicked.connect(self.config)
        self.button_2.clicked.connect(self.important)
        self.cmd_input.returnPressed.connect(self.chat)
        
        v_line = QVBoxLayout()
        h_line = QHBoxLayout()
        
        h_line.addWidget(self.label, alignment=Qt.AlignLeft)
        h_line.addWidget(self.button, alignment=Qt.AlignRight)
        
        v_line.addLayout(h_line)
        v_line.addSpacing(20)
        v_line.addWidget(self.button_2, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.label_2, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.cmd_output)
        v_line.addWidget(self.cmd_input)
        v_line.addStretch()

        self.setLayout(v_line)
    
    def important(self):
        im, ok = QInputDialog.getText(self, "Puerto", "Ingresa la ip del servidor:")
        k_im, ok = QInputDialog.getText(self, "Clave", "Ingresa la clave del servidor:")
        if ok:
            self.button_2.setText(f">> puerto de acceso: En linea")
            self.cmd_output.insertPlainText(f'> {im} \n')
            self.cmd_output.insertPlainText(f'> {k_im} \n')
            self.cmd_input.clear()
            port(im, k_im)
        else:
            QMessageBox.warning(self, "Cancelado", "Operación cancelada.")
    
    def chat(self):

        cm = self.cmd_input.text().strip()
        sm = str(cm)
        self.cmd_input.clear()
        
        if not cm:
            return
        
        if sm == "/file":
            ruta , _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar archivo",
            "",
            "Todos los archivos (*)")
            sm = f"/file {ruta}"
        
        if sm == "/carpet":
            ruta_c = QFileDialog.getExistingDirectory(
            self,
            "Seleccionar carpeta",
            "")
            sm = f"/carpet {ruta_c}"
        
        if cm.lower() == "cls":
            self.cmd_output.clear()
            self.cmd_input.clear()
            return
        
        if cm == 'quit' or cm == 'q':
            QMessageBox.information(self, "Salir", "Saliendo del chat.")
            self.cmd_output.appendPlainText(f"> Saliendo del chat")
            self.button_2.setText(">> puerto de acceso: Off line")
            self.cmd_output.clear()
        
        enviar(sm)

    def actualizar_chat(self):
        while not out_msg.empty():
            texto = out_msg.get()
            self.cmd_output.appendPlainText(texto)

    def config(self):
        self.confi_window = Confi()
        self.confi_window.username_changed.connect(self.update_username)
        self.confi_window.show()
        
    def update_username(self, name):
        global Username
        Username = name
        self.label_2.setText(f">> {name}")
    
    def showEvent(self, event):
        aplicar_fondo(self, FONDO_GLOBAL)
        super().showEvent(event)

class Confi(QWidget):
    username_changed = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        aplicar_fondo(self, FONDO_GLOBAL)
        
        self.setWindowTitle('<.mandium configuración')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;")
        self.resize(850, 480)
        
        self.setWindowIcon(QIcon('i am a game theorist.png'))
        
        self.music_label = QLabel("placeholder.mp3")
        self.music_state = QLabel("Estado: ")
        
        self.nm = QLabel("<--- Nombre --->")
        self.msc = QLabel("<--- Musica --->")
        self.start = QLabel("<--- Pantalla de Inicio --->")
        self.manual = QLabel("<--- Manual de Usuario --->")
        
        self.button = QPushButton("Nombre de usuario:")
        self.button.setStyleSheet("border: 1px solid #FFFFFF;")
        
        self.button_pause=QPushButton('Pausa')
        self.button_pause.setStyleSheet("border: 1px solid #FFFFFF;")
        self.button_resume=QPushButton('Resume')
        self.button_resume.setStyleSheet("border: 1px solid #FFFFFF;")
        self.button_restore=QPushButton('Restore')
        self.button_restore.setStyleSheet("border: 1px solid #FFFFFF;")
        
        self.button_user_manual = QPushButton('Manual')
        self.button_user_manual.setStyleSheet("border: 1px solid #FFFFFF;")
        
        self.button_screen = QPushButton('Pantalla Principal')
        self.button_screen.setStyleSheet("border: 1px solid #FFFFFF;")
        self.button_server = QPushButton("Servidor")
        self.button_server.setStyleSheet("border: 1px solid #FFFFFF;")
        
        self.button.clicked.connect(self.name_config)
        self.button_resume.clicked.connect(self.resume)
        self.button_pause.clicked.connect(self.pause)
        self.button_user_manual.clicked.connect(self.ur_manual)
        self.button_screen.clicked.connect(self.comd)
        self.button_server.clicked.connect(self.server)
        
        v_line = QVBoxLayout()
        h_line = QHBoxLayout()
        c_line = QHBoxLayout()
        
        h_line.addWidget(self.music_label, alignment=Qt.AlignLeft)
        h_line.addSpacing(10)
        h_line.addWidget(self.button_pause,alignment=Qt.AlignLeft)
        h_line.addSpacing(10)
        h_line.addWidget(self.button_resume,alignment=Qt.AlignLeft)
        h_line.addSpacing(10)
        h_line.addWidget(self.button_restore,alignment=Qt.AlignLeft)
        h_line.addStretch()
        
        c_line.addWidget(self.button_screen)
        c_line.addSpacing(10)
        c_line.addWidget(self.button_server)
        c_line.addStretch()
        
        v_line.addStretch()
        v_line.addWidget(self.nm, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.button, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.msc, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addLayout(h_line)
        v_line.addSpacing(10)
        v_line.addWidget(self.music_state, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.start, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addLayout(c_line)
        v_line.addSpacing(10)
        v_line.addWidget(self.manual, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.button_user_manual, alignment=Qt.AlignLeft)
        v_line.addStretch()
        
        self.setLayout(v_line)
            
    def name_config(self):
        name, ok = QInputDialog.getText(self, "Nombre de usuario", "Ingresa tu nombre de usuario:")
        if ok and name:
            self.button.setText(f"Nombre de usuario: {name}")
            self.username_changed.emit(name)
            user(name)
        else:
            QMessageBox.warning(self, "Cancelado", "Operación cancelada.")
    
    def pause(self):
        pygame.mixer.music.pause()
        self.music_state.setText(f"Estado: Song paused")

    def resume(self):
        pygame.mixer.music.unpause()
        self.music_state.setText("Estado: Song RESUMED")
    
    def comd(self):
        self.c = MyWindow()
        self.c.show()
        ventanas = QApplication.topLevelWidgets()

        especificas = [v for v in ventanas if isinstance(v, MyWindow) and v.isVisible()]

        if len(especificas) > 1:
            for i in range(len(especificas) - 1):
                especificas[i].close()
    
    def server(self):
        self.servr = Server()
        self.servr.show()
        ventanas = QApplication.topLevelWidgets()

        especificas = [v for v in ventanas if isinstance(v, Server) and v.isVisible()]

        if len(especificas) > 1:
            for i in range(len(especificas) - 1):
                especificas[i].close()
    
    def ur_manual(self):
        self.mnl = UserManual()
        self.mnl.show()

class Server(QWidget):
    def __init__(self):
        super().__init__()
        aplicar_fondo(self, FONDO_GLOBAL)
        
        self.setWindowTitle('<.mandium server')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;")
        self.resize(425, 240)
        
        self.setWindowIcon(QIcon('i am a game theorist.png'))
        
        self.salida = QPlainTextEdit()
        self.salida.setReadOnly(True)

        self.entrada = QLineEdit()
        self.entrada.setPlaceholderText("Escribe un comando o acepta los usuarios")

        layout = QVBoxLayout()
        layout.addWidget(self.salida)
        layout.addWidget(self.entrada)
        self.setLayout(layout)

        self.proceso = QProcess(self)
        self.proceso.readyReadStandardOutput.connect(self.leer_stdout)
        self.proceso.readyReadStandardError.connect(self.leer_stderr)

        ruta_absoluta = resource_path("server.py")
        self.proceso.start("python", [ruta_absoluta])
        self.salida.appendPlainText("CMD iniciado...\n")
        self.entrada.returnPressed.connect(self.enviar_comando)

    def enviar_comando(self):
        comando = self.entrada.text()
        if not comando:
            return
        
        if comando == '/limpiar':
            self.salida.clear()
            self.entrada.clear()
            pass
        
        self.salida.insertPlainText('>' + comando + "\n")
        self.proceso.write((comando + "\n").encode("utf-8"))
        self.entrada.clear()

    def leer_stdout(self):
        data = self.proceso.readAllStandardOutput().data().decode(errors="ignore")
        self.salida.appendPlainText(data)

    def leer_stderr(self):
        data = self.proceso.readAllStandardError().data().decode(errors="ignore")
        self.salida.appendPlainText(data)

class UserManual(QWidget):
    def __init__(self):
        super().__init__()
        
        EULA = """ACUERDO DE LICENCIA DE USUARIO FINAL (EULA)

Última actualización: [FECHA]

Este Acuerdo de Licencia de Usuario Final ("Acuerdo") es un contrato legal entre usted ("Usuario") y el desarrollador ("Licenciante") de la aplicación Comandium ("Aplicación").

Al instalar, copiar, acceder o utilizar la Aplicación, usted acepta estar sujeto a los términos y condiciones de este Acuerdo. Si no está de acuerdo con estos términos, no instale ni utilice la Aplicación.

1. CONCESIÓN DE LICENCIA

El Licenciante otorga al Usuario una licencia ilimitada, no exclusiva, transferible e irrevocable para instalar y utilizar la Aplicación.

Esta licencia no implica la venta de la Aplicación ni de los derechos de propiedad intelectual asociados a la misma.

2. DESCRIPCIÓN DEL SOFTWARE

La Aplicación es un sistema de comunicación cliente-servidor que permite:

Mensajería entre usuarios conectados.

Envío y recepción de archivos.

Gestión de conexiones de red.

Configuración dinámica de parámetros.

Las funciones pueden ser modificadas, actualizadas o eliminadas en cualquier momento; sin embargo, siempre se notificará previamente cualquier cambio que vaya a realizarse.

3. RESTRICCIONES

Al tratarse de la versión de paga, no se imponen restricciones base sobre la personalización o modificación interna de la copia adquirida por el Usuario. El Usuario podrá editar su copia de la Aplicación según sus necesidades.

No obstante, esta libertad no implica la transferencia de los derechos de autor originales sobre el software.

4. PROPIEDAD INTELECTUAL

La Aplicación, incluyendo su código fuente, estructura, diseño, algoritmos y documentación, es propiedad exclusiva del Licenciante y está protegida por las leyes de propiedad intelectual aplicables.

El presente Acuerdo concede al Usuario derecho de propiedad sobre su copia adquirida de la Aplicación, mas no sobre la autoría original del software.

El Creador no se hace responsable por el uso que los usuarios den a su copia de la Aplicación.

5. ACTUALIZACIONES Y MODIFICACIONES

El Licenciante podrá proporcionar actualizaciones, mejoras o modificaciones en cualquier momento. Dichas actualizaciones estarán sujetas a los términos del presente Acuerdo.

6. RESPONSABILIDAD DEL USUARIO

El Usuario es el único responsable del uso que haga de la Aplicación y del contenido que transmita o reciba a través de ella.

El Licenciante no supervisa ni controla el contenido intercambiado entre usuarios.

7. LIMITACIÓN DE RESPONSABILIDAD

La Aplicación se proporciona "TAL CUAL" y "SEGÚN DISPONIBILIDAD", sin garantías de ningún tipo, expresas o implícitas.

El Licenciante no será responsable por:

Pérdida de datos.

Fallos en la conexión de red.

Daños directos, indirectos o incidentales.

Uso indebido por parte del Usuario.

Archivos dañados o infectados transmitidos por terceros.

El uso de la Aplicación es bajo su propio riesgo.

8. SEGURIDAD Y DATOS

La Aplicación puede manejar datos como:

Nombre de usuario.

Dirección IP.

Archivos enviados o recibidos.

El Licenciante no garantiza almacenamiento seguro ni protección contra accesos no autorizados, salvo que se indique expresamente.

Se recomienda no transmitir información confidencial o sensible sin medidas de seguridad adicionales.

9. FEEDBACK

Se agradece la entrega de feedback por parte de los usuarios. La Aplicación fue desarrollada inicialmente en un entorno ideal y puede contener errores o fallos.

Cualquier bug, por mínimo que sea, se agradecerá que sea reportado.

Esta Aplicación, aunque lleva tiempo en desarrollo, fue creada originalmente por un programador en sus inicios profesionales. El software continúa en evolución y puede mejorar con el apoyo y la colaboración del público.

10. TERMINACIÓN

Este Acuerdo estará vigente hasta que sea terminado.

El Licenciante podrá rescindir esta licencia (mas no invalidar la copia legítimamente adquirida por el Usuario) si se descubre que el Usuario realiza actividades indebidas relacionadas con la propiedad intelectual original del software.

En caso de que el usuario desee terminar su licencia puede borrar los archios directamente del sistema.

En caso de terminación, el Usuario deberá eliminar cualquier copia obtenida de forma no autorizada.

11. LEY APLICABLE

Este Acuerdo se regirá e interpretará conforme a las leyes de Venezuela, sin tener en cuenta sus normas sobre conflicto de leyes.

12. ACEPTACIÓN

Al instalar o utilizar la Aplicación, el Usuario confirma que ha leído, entendido y aceptado los términos de este Acuerdo."""
        
        self.setWindowTitle('<.mandium configuración')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;")
        self.resize(850, 480)
        
        self.setWindowIcon(QIcon('i am a game theorist.png'))
        
        self.label = QLabel("""Buenas 
Muchas gracias por usar comandium no soy muy bueno en es esto asi que aqui aparte de un manual para saber como funciona toda la aplicacion
va a estar el acuerdo de licencia del usuario para el que lo quiera leer lo pueda hacer tranquilamente
Esta aplicacion requiere la descarga de python 3.12 la puedes descargar en la microsoft store""")
        #Poner labels
        self.label_imagen = QLabel("arroz")
        imagen_1 = QPixmap("Tutorial/image_1")
        self.label_imagen.setPixmap(imagen_1)
        self.label_imagen.setFixedSize(500, 500)
        self.label_imagen.setScaledContents(True)
        #Poner imagenes
        v_line = QVBoxLayout()
        h_line = QHBoxLayout()
        
        v_line.addStretch()
        v_line.addWidget(self.label, alignment=Qt.AlignLeft)
        v_line.addSpacing(20)
        v_line.addWidget(self.label_imagen, alignment=Qt.AlignLeft)
        v_line.addStretch()
        
        self.setLayout(v_line)

a = MyWindow()
a.show()
app.exec_()