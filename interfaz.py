import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QSpinBox
from PyQt6.QtWidgets import QColorDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt

from app import AppConfig

from PyQt6.QtWidgets import (
    QFormLayout,
    QStackedWidget,
)

from PyQt6.QtGui import QColor, QPixmap


# VENTANA DE SETTINGS
class VentanaSettings(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Settings")
        self.setMinimumSize(800, 550)

        # 1. Cargar la configuración actual desde app.py
        self.config_actual = AppConfig.cargar_configuracion()
        self.ruta_foto_seleccionada = self.config_actual.get("foto_perfil", "")

        self.crear_interfaz()
        self.aplicar_estilo()

        # 2. Rellenar los campos con los valores cargados
        self.cargar_datos_en_interfaz()

    # INTERFAZ

    def crear_interfaz(self):

        layout_principal = QHBoxLayout()
        self.setLayout(layout_principal)

        # 1. Panel Lateral Izquierdo
        panel_lateral = QWidget()
        panel_lateral.setFixedWidth(200)

        layout_lateral = QVBoxLayout()
        panel_lateral.setLayout(layout_lateral)

        titulo = QLabel("⚙  Settings")
        titulo.setObjectName("tituloSettings")

        layout_lateral.addWidget(titulo)

        # Botones de navegación
        self.btn_general = QPushButton("⚙   General")
        self.btn_apariencia = QPushButton("◈   Apariencia")
        self.btn_colores = QPushButton("●   Colores")
        self.btn_cuenta = QPushButton("♙   Cuenta")

        self.btn_general.setObjectName("botonActivo")

        layout_lateral.addWidget(self.btn_general)
        layout_lateral.addWidget(self.btn_apariencia)
        layout_lateral.addWidget(self.btn_colores)
        layout_lateral.addWidget(self.btn_cuenta)

        layout_lateral.addStretch()

        layout_principal.addWidget(panel_lateral)

        # CONTENIDO
        self.paginas = QStackedWidget()

        self.crear_pagina_general()
        self.crear_pagina_apariencia()
        self.crear_pagina_colores()
        self.crear_pagina_cuenta()

        layout_principal.addWidget(self.paginas)

        # Conectar botones de navegación
        self.btn_general.clicked.connect(
            lambda: self.paginas.setCurrentIndex(0)
        )

        self.btn_apariencia.clicked.connect(
            lambda: self.paginas.setCurrentIndex(1)
        )

        self.btn_colores.clicked.connect(
            lambda: self.paginas.setCurrentIndex(2)
        )

        self.btn_cuenta.clicked.connect(
            lambda: self.paginas.setCurrentIndex(3)
        )

    # MÉTODO AUXILIAR PARA CREAR LA BOTONERA DE GUARDAR/CANCELAR EN CADA PÁGINA
    def crear_botonera_inferior(self, layout_pagina):
        botones = QHBoxLayout()
        botones.addStretch()

        btn_cancelar = QPushButton("Cancelar")
        btn_guardar = QPushButton("💾  Guardar cambios")
        btn_guardar.setObjectName("botonGuardar")

        botones.addWidget(btn_cancelar)
        botones.addWidget(btn_guardar)

        layout_pagina.addLayout(botones)

        # Conectar eventos
        btn_cancelar.clicked.connect(self.reject)
        btn_guardar.clicked.connect(self.guardar_cambios)

    # PÁGINA GENERAL

    def crear_pagina_general(self):

        pagina = QWidget()
        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel("Configuración General")
        titulo.setObjectName("tituloPrincipal")

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Configura los datos principales de tu aplicación."
        )

        descripcion.setObjectName("descripcion")

        layout.addWidget(descripcion)

        formulario = QFormLayout()

        # Nombre de usuario
        self.nombre_usuario = QLineEdit()
        self.nombre_usuario.setPlaceholderText(
            "Ingrese su nombre de usuario"
        )

        formulario.addRow(
            "Nombre de usuario:",
            self.nombre_usuario
        )

        # Idioma
        self.idioma = QComboBox()

        self.idioma.addItems([
            "es-ES",
            "en-US"
        ])

        formulario.addRow(
            "Idioma:",
            self.idioma
        )

        # Tamaño
        self.tamano_fuente = QSpinBox()

        self.tamano_fuente.setMinimum(8)
        self.tamano_fuente.setMaximum(40)
        self.tamano_fuente.setValue(12)

        formulario.addRow(
            "Tamaño de fuente:",
            self.tamano_fuente
        )

        layout.addLayout(formulario)
        layout.addStretch()

        # Añadir botones de Guardar/Cancelar
        self.crear_botonera_inferior(layout)

        self.paginas.addWidget(pagina)

    # PÁGINA APARIENCIA

    def crear_pagina_apariencia(self):

        pagina = QWidget()
        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel("Apariencia")
        titulo.setObjectName("tituloPrincipal")

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Selecciona el tema que deseas utilizar."
        )

        descripcion.setObjectName("descripcion")

        layout.addWidget(descripcion)

        formulario = QFormLayout()

        # Tema
        self.tema = QComboBox()

        self.tema.addItems([
            "claro",
            "oscuro"
        ])

        formulario.addRow(
            "Tema de interfaz:",
            self.tema
        )

        layout.addLayout(formulario)

        # Vista previa
        titulo_preview = QLabel("Vista previa")
        titulo_preview.setObjectName("subtitulo")

        layout.addWidget(titulo_preview)

        preview = QWidget()
        preview.setObjectName("preview")

        preview_layout = QVBoxLayout()
        preview.setLayout(preview_layout)

        texto_preview = QLabel(
            "Así se verá tu interfaz"
        )

        texto_preview.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        preview_layout.addWidget(
            texto_preview
        )

        boton_preview = QPushButton(
            "Botón de ejemplo"
        )

        preview_layout.addWidget(
            boton_preview
        )

        layout.addWidget(preview)
        layout.addStretch()

        # Añadir botones de Guardar/Cancelar
        self.crear_botonera_inferior(layout)

        self.paginas.addWidget(pagina)

    # PÁGINA COLORES

    def crear_pagina_colores(self):

        pagina = QWidget()
        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel("Colores")
        titulo.setObjectName("tituloPrincipal")

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Personaliza los colores utilizados por la aplicación."
        )

        descripcion.setObjectName("descripcion")

        layout.addWidget(descripcion)

        formulario = QFormLayout()

        # COLOR DEL MENÚ

        self.color_menu = "#d9d9d9"

        self.btn_color_menu = QPushButton(
            self.color_menu
        )

        self.btn_color_menu.clicked.connect(
            self.seleccionar_color_menu
        )

        formulario.addRow(
            "Color de la barra de menú:",
            self.btn_color_menu
        )

        # COLOR DE LETRA

        self.color_letra = "#000000"

        self.btn_color_letra = QPushButton(
            self.color_letra
        )

        self.btn_color_letra.clicked.connect(
            self.seleccionar_color_letra
        )

        formulario.addRow(
            "Color de letra:",
            self.btn_color_letra
        )

        layout.addLayout(formulario)
        layout.addStretch()

        # Añadir botones de Guardar/Cancelar
        self.crear_botonera_inferior(layout)

        self.paginas.addWidget(pagina)

    # PÁGINA CUENTA

    def crear_pagina_cuenta(self):

        pagina = QWidget()
        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel("Cuenta")
        titulo.setObjectName("tituloPrincipal")

        layout.addWidget(titulo)

        descripcion = QLabel(
            "Personaliza tu información de perfil."
        )

        descripcion.setObjectName("descripcion")

        layout.addWidget(descripcion)

        # FOTO
        self.foto_perfil = QLabel("👤")

        self.foto_perfil.setObjectName(
            "fotoPerfil"
        )

        self.foto_perfil.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.foto_perfil.setFixedSize(
            120,
            120
        )

        layout.addWidget(
            self.foto_perfil,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.btn_cambiar_foto = QPushButton(
            "Cambiar foto"
        )

        self.btn_cambiar_foto.clicked.connect(
            self.seleccionar_foto
        )

        layout.addWidget(
            self.btn_cambiar_foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        # Añadir botones de Guardar/Cancelar
        self.crear_botonera_inferior(layout)

        self.paginas.addWidget(pagina)

    # Selector Color Menú

    def seleccionar_color_menu(self):

        color = QColorDialog.getColor(
            QColor(self.color_menu),
            self,
            "Seleccionar color de menú"
        )

        if color.isValid():
            self.color_menu = color.name()

            self.btn_color_menu.setText(
                self.color_menu
            )

    # Selector Color Letra

    def seleccionar_color_letra(self):

        color = QColorDialog.getColor(
            QColor(self.color_letra),
            self,
            "Seleccionar color de letra"
        )

        if color.isValid():
            self.color_letra = color.name()

            self.btn_color_letra.setText(
                self.color_letra
            )

    # SELECTOR DE FOTO

    def seleccionar_foto(self):

        ruta, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar foto de perfil",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if ruta:
            self.ruta_foto_seleccionada = ruta
            pixmap = QPixmap(ruta)

            pixmap = pixmap.scaled(
                100,
                100,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            self.foto_perfil.setPixmap(
                pixmap
            )

    # CARGAR DATOS DESDE ARCHIVO A UI
    def cargar_datos_en_interfaz(self):
        # Nombre usuario
        self.nombre_usuario.setText(self.config_actual.get("nombre_usuario", ""))

        # Idioma
        idioma = self.config_actual.get("idioma", "es-ES")
        idx_idioma = self.idioma.findText(idioma)
        if idx_idioma >= 0:
            self.idioma.setCurrentIndex(idx_idioma)

        # Tamaño fuente
        self.tamano_fuente.setValue(self.config_actual.get("tamano_fuente", 12))

        # Tema
        tema = self.config_actual.get("tema_interfaz", "claro")
        idx_tema = self.tema.findText(tema)
        if idx_tema >= 0:
            self.tema.setCurrentIndex(idx_tema)

        # Colores
        self.color_menu = self.config_actual.get("color_barra_menu", "#d9d9d9")
        self.btn_color_menu.setText(self.color_menu)

        self.color_letra = self.config_actual.get("color_letra", "#000000")
        self.btn_color_letra.setText(self.color_letra)

        # Foto perfil
        ruta = self.config_actual.get("foto_perfil", "")
        if ruta:
            pixmap = QPixmap(ruta)
            if not pixmap.isNull():
                pixmap = pixmap.scaled(
                    100, 100,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.foto_perfil.setPixmap(pixmap)

    # GUARDAR DATOS DESDE UI A ARCHIVO
    def guardar_cambios(self):
        self.config_actual["nombre_usuario"] = self.nombre_usuario.text()
        self.config_actual["idioma"] = self.idioma.currentText()
        self.config_actual["tamano_fuente"] = self.tamano_fuente.value()
        self.config_actual["tema_interfaz"] = self.tema.currentText()
        self.config_actual["color_barra_menu"] = self.color_menu
        self.config_actual["color_letra"] = self.color_letra
        self.config_actual["foto_perfil"] = self.ruta_foto_seleccionada

        exito = AppConfig.guardar_configuracion(self.config_actual)
        if exito:
            self.accept()

    # ESTILO

    def aplicar_estilo(self):

        self.setStyleSheet("""

            QDialog {
                background-color: #15171C;
            }

            QLabel {
                color: #EDEDED;
                font-size: 14px;
            }

            #tituloSettings {
                font-size: 21px;
                font-weight: bold;
                padding: 12px;
            }

            #tituloPrincipal {
                font-size: 27px;
                font-weight: bold;
                padding-top: 10px;
                padding-bottom: 5px;
            }

            #subtitulo {
                font-size: 18px;
                font-weight: bold;
                margin-top: 15px;
            }

            #descripcion {
                color: #A5A5A5;
                font-size: 14px;
                padding-bottom: 20px;
            }

            QPushButton {
                background-color: #20232A;
                color: #EDEDED;
                border: 1px solid #3A3D46;
                border-radius: 7px;
                padding: 10px;
                font-size: 14px;
            }

            QPushButton:hover {
                background-color: #343740;
            }

            #botonActivo {
                background-color: #7048A8;
                border: none;
                font-weight: bold;
            }

            #botonGuardar {
                background-color: #7048A8;
                border: none;
                color: white;
                font-weight: bold;
                padding: 12px 20px;
            }

            #botonGuardar:hover {
                background-color: #8359BB;
            }

            QLineEdit,
            QComboBox,
            QSpinBox {
                background-color: #20232A;
                color: #EDEDED;
                border: 1px solid #444750;
                border-radius: 5px;
                padding: 9px;
            }

            QComboBox QAbstractItemView {
                background-color: #20232A;
                color: #EDEDED;
                selection-background-color: #7048A8;
            }

            #preview {
                background-color: #20232A;
                border: 1px solid #3A3D46;
                border-radius: 10px;
                padding: 20px;
            }

            #fotoPerfil {
                background-color: #7048A8;
                border-radius: 60px;
                font-size: 55px;
            }
        """)


# VENTANA PRINCIPAL

class VentanaPrincipal(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle(
            "Gestión de Configuración de Usuario"
        )

        self.setMinimumSize(
            1000,
            650
        )

        self.crear_menu()
        self.crear_interfaz()
        self.aplicar_estilo()

    # MENÚ SUPERIOR
    def crear_menu(self):
        barra = self.menuBar()

        # ----------------------------------------------------
        # ARCHIVO
        # ----------------------------------------------------

        archivo = barra.addMenu("Archivo")

        nuevo = QAction("Nuevo", self)
        abrir = QAction("Abrir", self)
        guardar = QAction("Guardar", self)
        archivo.addAction(nuevo)
        archivo.addAction(abrir)
        archivo.addAction(guardar)

        archivo.addSeparator()

        cerrar = QAction("Cerrar", self)
        salir = QAction("Salir", self)

        archivo.addAction(cerrar)
        archivo.addAction(salir)

        salir.triggered.connect(
            self.close
        )

        # EDICIÓN
        edicion = barra.addMenu("Edición")

        edicion.addAction(
            QAction("Deshacer", self)
        )

        edicion.addAction(
            QAction("Rehacer", self)
        )

        # ----------------------------------------------------
        # VER
        # ----------------------------------------------------

        ver = barra.addMenu("Ver")

        ver.addAction(
            QAction("Pantalla principal", self)
        )

        ver.addAction(
            QAction("Vista de configuración", self)
        )

        # AJUSTES
        settings = barra.addMenu("Settings")

        abrir_settings = QAction(
            "Abrir Settings",
            self
        )

        settings.addAction(
            abrir_settings
        )

        abrir_settings.triggered.connect(
            self.abrir_settings
        )

        # ----------------------------------------------------
        # AYUDA
        # ----------------------------------------------------

        ayuda = barra.addMenu("Ayuda")

        ayuda.addAction(
            QAction("Acerca de", self)
        )

    # INTERFAZ PRINCIPAL

    def crear_interfaz(self):
        central = QWidget()

        layout = QHBoxLayout()
        central.setLayout(layout)

        # ----------------------------------------------------
        # PANEL IZQUIERDO
        # ----------------------------------------------------

        panel_izquierdo = QWidget()
        panel_izquierdo.setFixedWidth(270)

        layout_izquierdo = QVBoxLayout()
        panel_izquierdo.setLayout(
            layout_izquierdo
        )

        # Foto
        foto = QLabel("👤")

        foto.setObjectName(
            "fotoPrincipal"
        )

        foto.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        foto.setFixedSize(
            120,
            120
        )

        layout_izquierdo.addWidget(
            foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Bienvenida
        bienvenida = QLabel(
            "¡Bienvenido!"
        )

        bienvenida.setObjectName(
            "bienvenida"
        )

        bienvenida.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout_izquierdo.addWidget(
            bienvenida
        )

        descripcion = QLabel(
            "Gestiona tu configuración\ndesde Settings."
        )

        descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descripcion.setObjectName(
            "descripcion"
        )

        layout_izquierdo.addWidget(
            descripcion
        )

        layout_izquierdo.addStretch()

        layout.addWidget(
            panel_izquierdo
        )

        # ----------------------------------------------------
        # PANEL CENTRAL
        # ----------------------------------------------------
        panel_central = QWidget()

        layout_central = QVBoxLayout()
        panel_central.setLayout(
            layout_central
        )

        layout_central.addStretch()

        # Icono
        icono = QLabel("⚙")

        icono.setObjectName(
            "icono"
        )

        icono.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout_central.addWidget(
            icono
        )

        # Título
        titulo = QLabel(
            "Gestión de Configuración de Usuario"
        )

        titulo.setObjectName(
            "titulo"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout_central.addWidget(
            titulo
        )

        # Texto
        texto = QLabel(
            "Personaliza tu experiencia y guarda tu\n"
            "configuración de forma segura."
        )

        texto.setObjectName(
            "texto"
        )

        texto.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout_central.addWidget(
            texto
        )

        # Botón
        boton_settings = QPushButton(
            "⚙   Abrir Settings"
        )

        boton_settings.setObjectName(
            "botonPrincipal"
        )

        boton_settings.clicked.connect(
            self.abrir_settings
        )

        layout_central.addWidget(
            boton_settings,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_central.addStretch()

        layout.addWidget(
            panel_central
        )

        self.setCentralWidget(
            central
        )


    # SETTINGS o AJUSTES
    def abrir_settings(self):
        ventana = VentanaSettings(self)

        ventana.exec()


    # ESTILO
    def aplicar_estilo(self):
        self.setStyleSheet("""

            QMainWindow {
                background-color: #15171C;
            }

            QMenuBar {
                background-color: #2B2D31;
                color: #EDEDED;
                padding: 6px;
                font-size: 14px;
            }

            QMenuBar::item:selected {
                background-color: #7048A8;
            }

            QMenu {
                background-color: #20232A;
                color: #EDEDED;
                border: 1px solid #3A3D46;
            }

            QMenu::item:selected {
                background-color: #7048A8;
            }

            QLabel {
                color: #EDEDED;
            }

            #bienvenida {
                color: #A978E0;
                font-size: 24px;
                font-weight: bold;
            }

            #fotoPrincipal {
                background-color: #7048A8;
                border-radius: 60px;
                font-size: 55px;
            }

            #icono {
                color: #A978E0;
                font-size: 90px;
            }

            #titulo {
                font-size: 29px;
                font-weight: bold;
            }

            #texto {
                color: #AAAAAA;
                font-size: 15px;
            }

            #botonPrincipal {
                background-color: #7048A8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 13px 25px;
                font-size: 15px;
                font-weight: bold;
            }

            #botonPrincipal:hover {
                background-color: #8359BB;
            }
        """)

def main():
    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()

    ventana.show()

    sys.exit(
        app.exec()
    )


if __name__ == "__main__":
    main()