from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget,QLineEdit, QLabel, QPushButton, QHBoxLayout, QVBoxLayout,QInputDialog, QMessageBox, QGraphicsOpacityEffect
from PyQt5.QtCore import Qt, QRect, QPropertyAnimation, QPoint, QParallelAnimationGroup
from PyQt5.QtGui import QFont, QIcon
from chatter import *
import subprocess
import sys

app = QApplication(sys.argv)

Title = " <.mandium "

class MyWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('<.mandium')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "font-family: Consolas;")
        self.resize(850, 480)
        
        self.label = QLabel(Title)
        self.label.setStyleSheet(
            "font-size: 86px;"
            "font-weight: bold;"
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
        self.but_C.setIcon(QIcon('confi.png'))
        self.but_C.setIconSize(QtCore.QSize(32, 32))
        
        self.but.clicked.connect(self.open_chat)
        self.but_2.clicked.connect(self.open_server)
        self.but_C.clicked.connect(self.close)
        
        self.setWindowIcon(QIcon('i am a game theorist.png'))
        
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
        subprocess.Popen([sys.executable, "server.py"])
    
    def config(self):
        self.confi_window = Confi()
        self.confi_window.show()
        MyWindow.close(self)
    
class Chat(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Chat Window')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "font-family: Consolas;")
        self.setWindowIcon(QIcon('i am a game theorist.png'))
        self.resize(850, 480)
        
        self.puerto = None
        
        self.label = QLabel("<.mandium [Alpha 0.1.2]\nSA.54 - Gracias por usar <.mandium")
        self.label.setStyleSheet("font-size: 13px")
        
        self.label_2 = QLabel(f">>")
        
        self.button = QPushButton()
        self.button.setIcon(QIcon('confi.png'))
        self.button.setIconSize(QtCore.QSize(32, 32))
        
        self.button_2 = QPushButton(">> puerto de acceso:")
        
        self.button_3 = QPushButton(">>")
        self.button_3.setStyleSheet(
            "border: 1px solid #FFFFFF;"
            "border-radius: 5px;")
        self.button_3.setFixedSize(850, 25)
        
        self.button.clicked.connect(self.close)
        self.button_2.clicked.connect(self.important)
        self.button_3.clicked.connect(self.chat)
        
        v_line = QVBoxLayout()
        h_line = QHBoxLayout()
        
        h_line.addWidget(self.label, alignment=Qt.AlignLeft)
        h_line.addWidget(self.button, alignment=Qt.AlignRight)
        
        v_line.addLayout(h_line)
        v_line.addSpacing(20)
        v_line.addWidget(self.button_2, alignment=Qt.AlignLeft)
        v_line.addSpacing(10)
        v_line.addWidget(self.label_2, alignment=Qt.AlignLeft)
        v_line.addStretch()
        v_line.addWidget(self.button_3, alignment=Qt.AlignLeft)

        self.setLayout(v_line)
    
    def important(self):
        im, ok = QInputDialog.getInt(self, "Puerto", "Ingresa el puerto del servidor:",value = self.puerto if self.puerto else 0)
        if ok:
            self.puerto = im
            self.button_2.setText(f">> puerto de acceso: {im}")
            port(im)
        else:
            QMessageBox.warning(self, "Cancelado", "Operación cancelada.")
    
    def chat(self):
        while True:
            ct, ok = QInputDialog.getText(self, "Mensaje", "Escribe tu mensaje (escribe 'q' para salir):")
            if ok:
                self.label_2.setText(f">>{"Usuario"}: {ct}")
                enviar(ct)
                if ct == 'quit' or ct == 'q':
                    QMessageBox.information(self, "Salir", "Saliendo del chat.")
                    break
            else:
                QMessageBox.warning(self, "Cancelado", "Operación cancelada.")
                break
            
class Confi(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('<.mandium configuración')
        self.setStyleSheet(
            "background-color: black;"
            "color: white;"
            "font-family: Consolas;")
        self.resize(850, 480)
        
        self.button = QPushButton("Nombre de usuario")
        
        

a = MyWindow()
a.show()
app.exec_()