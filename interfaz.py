import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QSpinBox, QFormLayout
from PyQt6.QtWidgets import QColorDialog, QFileDialog, QMessageBox, QStackedWidget
from PyQt6.QtGui import QAction, QFont, QColor, QPixmap, QPainter, QPainterPath, QPen
from PyQt6.QtCore import Qt

from app import AppConfig

def cargar_configuracion():

    resultado = AppConfig.cargar_configuracion()

    if isinstance(resultado, tuple):
        return resultado[0]

    return resultado

def guardar_configuracion(config):

    resultado = AppConfig.guardar_configuracion(config)

    if isinstance(resultado, tuple):
        return resultado

    return resultado, ""


def aplicar_recorte_circular(pixmap_original, size=120):
    pixmap_escalado = pixmap_original.scaled(
        size,
        size,
        Qt.AspectRatioMode.KeepAspectRatioByExpanding,
        Qt.TransformationMode.SmoothTransformation
    )

    pixmap_resultado = QPixmap(size, size)
    pixmap_resultado.fill(Qt.GlobalColor.transparent)

    painter = QPainter(pixmap_resultado)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)

    path = QPainterPath()
    path.addEllipse(0, 0, size, size)
    painter.setClipPath(path)

    x = (size - pixmap_escalado.width()) // 2
    y = (size - pixmap_escalado.height()) // 2
    painter.drawPixmap(x, y, pixmap_escalado)

    # Borde morado elegante
    pen = QPen(QColor("#7048A8"), 3)
    painter.setPen(pen)
    painter.drawEllipse(1, 1, size - 2, size - 2)

    painter.end()

    return pixmap_resultado


# VENTANA PRINCIPAL
class VentanaPrincipal(QMainWindow):

    def __init__(self):

        super().__init__()

        self.config = cargar_configuracion()

        self.setWindowTitle(
            "Gestión de Configuración de Usuario"
        )

        self.setMinimumSize(1000, 650)

        self.crear_menu()
        self.crear_interfaz()
        self.aplicar_configuracion()

    # MENÚ
    def crear_menu(self):

        barra = self.menuBar()

        self.menu_archivo = barra.addMenu("Archivo")
        self.menu_edicion = barra.addMenu("Edición")
        self.menu_ver = barra.addMenu("Ver")
        self.menu_settings = barra.addMenu("Settings")
        self.menu_ayuda = barra.addMenu("Ayuda")

        # ---------------- ARCHIVO ----------------

        salir = QAction("Salir", self)
        salir.triggered.connect(self.close)

        self.menu_archivo.addAction(salir)

        # ---------------- SETTINGS ----------------

        abrir_settings = QAction(
            "Abrir Settings",
            self
        )

        abrir_settings.triggered.connect(
            self.abrir_settings
        )

        self.menu_settings.addAction(
            abrir_settings
        )

    # INTERFAZ PRINCIPAL

    def crear_interfaz(self):

        central = QWidget()

        layout = QHBoxLayout()
        layout.setContentsMargins(
            45,
            25,
            45,
            40
        )

        layout.setSpacing(0)

        # PANEL IZQUIERDO
        panel_izquierdo = QWidget()

        panel_izquierdo.setFixedWidth(270)

        layout_izquierdo = QVBoxLayout()

        layout_izquierdo.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout_izquierdo.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )

        # FOTO
        self.foto_principal = QLabel("👤")

        self.foto_principal.setFixedSize(
            120,
            120
        )

        self.foto_principal.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.foto_principal.setObjectName(
            "fotoPrincipal"
        )

        layout_izquierdo.addWidget(
            self.foto_principal,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout_izquierdo.addSpacing(15)

        # BIENVENIDA
        self.lbl_bienvenida = QLabel(
            "¡Bienvenido!"
        )

        self.lbl_bienvenida.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_bienvenida.setObjectName(
            "bienvenida"
        )

        layout_izquierdo.addWidget(
            self.lbl_bienvenida
        )

        # DESCRIPCIÓN
        descripcion = QLabel(
            "Gestiona tu configuración\n"
            "desde Settings."
        )

        descripcion.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descripcion.setObjectName(
            "descripcionIzquierda"
        )

        layout_izquierdo.addWidget(
            descripcion
        )

        panel_izquierdo.setLayout(
            layout_izquierdo
        )

        # PARTE CENTRAL

        panel_central = QWidget()

        layout_central = QVBoxLayout()

        layout_central.setContentsMargins(
            30,
            25,
            0,
            0
        )

        layout_central.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        # ENGRANAJE
        self.icono_settings = QLabel("⚙")

        self.icono_settings.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icono_settings.setObjectName(
            "iconoSettings"
        )

        layout_central.addWidget(
            self.icono_settings
        )

        layout_central.addSpacing(10)

        # ----------------------------------------------------
        # TÍTULO

        titulo = QLabel(
            "Gestión de Configuración de Usuario"
        )

        titulo.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        titulo.setObjectName(
            "tituloPrincipal"
        )

        layout_central.addWidget(
            titulo
        )

        layout_central.addSpacing(10)

        # DESCRIPCIÓN
        # ----------------------------------------------------

        descripcion_central = QLabel(
            "Personaliza tu experiencia y guarda tu\n"
            "configuración de forma segura."
        )

        descripcion_central.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        descripcion_central.setObjectName(
            "descripcionCentral"
        )

        layout_central.addWidget(
            descripcion_central
        )

        layout_central.addSpacing(18)

        # ----------------------------------------------------
        # BOTÓN
        # ----------------------------------------------------

        self.btn_settings = QPushButton(
            "⚙   Abrir Settings"
        )

        self.btn_settings.setObjectName(
            "botonPrincipal"
        )

        self.btn_settings.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        self.btn_settings.clicked.connect(
            self.abrir_settings
        )

        layout_central.addWidget(
            self.btn_settings,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        panel_central.setLayout(
            layout_central
        )

        # ====================================================
        # AGREGAR TODO

        layout.addWidget(
            panel_izquierdo
        )

        layout.addWidget(
            panel_central,
            1
        )

        central.setLayout(layout)

        self.setCentralWidget(central)

    # ABRIR SETTINGS
    def abrir_settings(self):

        ventana = VentanaSettings(
            self.config,
            self.actualizar_interfaz,
            self
        )

        ventana.exec()

    # ACTUALIZAR DESPUÉS DE GUARDAR

    def actualizar_interfaz(self, nueva_config):

        self.config = nueva_config.copy()

        self.aplicar_configuracion()

    # ========================================================
    # APLICAR CONFIGURACIÓN
    # ========================================================

    def aplicar_configuracion(self):

        tema = self.config.get(
            "tema_interfaz",
            "oscuro"
        )

        color_menu = self.config.get(
            "color_barra_menu",
            "#2B2D31"
        )

        color_letra = self.config.get(
            "color_letra",
            "#EDEDED"
        )

        tamano = self.config.get(
            "tamano_fuente",
            12
        )

        nombre = self.config.get(
            "nombre_usuario",
            "Usuario"
        )

        foto = self.config.get(
            "foto_perfil",
            ""
        )

        # NOMBRE

        if nombre:
            self.lbl_bienvenida.setText(
                f"¡Bienvenido, {nombre}!"
            )
        else:
            self.lbl_bienvenida.setText(
                "¡Bienvenido!"
            )

        # FOTO
        if foto and os.path.exists(foto):

            pixmap = QPixmap(foto)

            if not pixmap.isNull():

                pixmap_circular = aplicar_recorte_circular(pixmap, 120)

                self.foto_principal.setPixmap(
                    pixmap_circular
                )

                self.foto_principal.setText("")

            else:

                self.foto_principal.setText(
                    "👤"
                )

        else:

            self.foto_principal.setPixmap(QPixmap())
            self.foto_principal.setText("👤")

        # ESTILO
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: #15171C;
            }}

            QWidget {{
                font-size: {tamano}px;
            }}

            QMenuBar {{
                background-color: {color_menu};
                color: {color_letra};
                padding: 6px;
                font-size: 14px;
            }}

            QMenuBar::item:selected {{
                background-color: #7048A8;
            }}

            QMenu {{
                background-color: #20232A;
                color: {color_letra};
                border: 1px solid #3A3D46;
            }}

            QMenu::item:selected {{
                background-color: #7048A8;
            }}

            QLabel {{
                color: {color_letra};
            }}

            #bienvenida {{
                color: #A978E0;
                font-size: 24px;
                font-weight: bold;
            }}

            #fotoPrincipal {{
                background-color: #7048A8;
                border-radius: 60px;
                font-size: 55px;
                color: white;
                qproperty-alignment: 'AlignCenter';
            }}

            #descripcionIzquierda {{
                color: #A5A5A5;
                font-size: 13px;
            }}

            #iconoSettings {{
                color: #A978E0;
                font-size: 90px;
            }}

            #tituloPrincipal {{
                font-size: 29px;
                font-weight: bold;
                color: {color_letra};
            }}

            #descripcionCentral {{
                color: #AAAAAA;
                font-size: 15px;
            }}

            #botonPrincipal {{
                background-color: #7048A8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 13px 25px;
                font-size: 15px;
                font-weight: bold;
            }}

            #botonPrincipal:hover {{
                background-color: #8359BB;
            }}
            """
        )


# SETTINGS o AJUSTES

class VentanaSettings(QDialog):

    def __init__(
        self,
        config,
        actualizar_principal=None,
        parent=None
    ):

        super().__init__(parent)

        self.config = config.copy()

        self.actualizar_principal = (
            actualizar_principal
        )

        self.color_menu = self.config.get(
            "color_barra_menu",
            "#d9d9d9"
        )

        self.color_letra = self.config.get(
            "color_letra",
            "#000000"
        )

        self.foto_seleccionada = self.config.get(
            "foto_perfil",
            ""
        )

        self.setWindowTitle(
            "Settings"
        )

        self.setMinimumSize(
            800,
            550
        )

        self.crear_interfaz()
        self.aplicar_estilo()

    def crear_interfaz(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(0)

        # SIDEBAR
        panel_lateral = QWidget()

        panel_lateral.setFixedWidth(200)

        layout_lateral = QVBoxLayout()
        panel_lateral.setLayout(layout_lateral)

        titulo = QLabel("⚙  Settings")
        titulo.setObjectName("tituloSettings")
        layout_lateral.addWidget(titulo)

        self.btn_general = QPushButton("⚙   General")
        self.btn_apariencia = QPushButton("◈   Apariencia")
        self.btn_colores = QPushButton("●   Colores")
        self.btn_cuenta = QPushButton("♙   Cuenta")

        layout_lateral.addWidget(
            self.btn_general
        )

        layout_lateral.addWidget(
            self.btn_apariencia
        )

        layout_lateral.addWidget(
            self.btn_colores
        )

        layout_lateral.addWidget(
            self.btn_cuenta
        )

        layout_lateral.addStretch()
        layout.addWidget(panel_lateral)

        # STACK

        contenido = QWidget()

        contenido_layout = QVBoxLayout()
        contenido.setLayout(contenido_layout)

        self.stack = QStackedWidget()

        self.stack.addWidget(
            self.crear_general()
        )

        self.stack.addWidget(
            self.crear_apariencia()
        )

        self.stack.addWidget(
            self.crear_colores()
        )

        self.stack.addWidget(
            self.crear_cuenta()
        )

        contenido_layout.addWidget(
            self.stack
        )

        layout.addWidget(contenido)

        # ====================================================
        # CONEXIONES

        self.btn_general.clicked.connect(
            lambda: self.cambiar_pagina(0)
        )

        self.btn_apariencia.clicked.connect(
            lambda: self.cambiar_pagina(1)
        )

        self.btn_colores.clicked.connect(
            lambda: self.cambiar_pagina(2)
        )

        self.btn_cuenta.clicked.connect(
            lambda: self.cambiar_pagina(3)
        )

        self.setLayout(layout)

    # BOTONERA INFERIOR REUTILIZABLE
    def crear_botonera_inferior(self, layout_pagina):
        botones = QHBoxLayout()
        botones.addStretch()

        cancelar = QPushButton(
            "Cancelar"
        )

        cancelar.clicked.connect(
            self.reject
        )

        guardar = QPushButton(
            "💾  Guardar cambios"
        )

        guardar.setObjectName("botonGuardar")

        guardar.clicked.connect(
            self.guardar
        )

        botones.addWidget(
            cancelar
        )

        botones.addWidget(
            guardar
        )

        layout_pagina.addLayout(
            botones
        )

    # ========================================================
    # CAMBIAR PÁGINA

    def cambiar_pagina(self, indice):

        self.stack.setCurrentIndex(
            indice
        )

        botones = [
            self.btn_general,
            self.btn_apariencia,
            self.btn_colores,
            self.btn_cuenta
        ]

        for i, boton in enumerate(botones):

            if i == indice:
                boton.setObjectName("botonActivo")
            else:
                boton.setObjectName("")

            boton.style().unpolish(
                boton
            )

            boton.style().polish(
                boton
            )

    # ========================================================
    # GENERAL

    def crear_general(self):

        pagina = QWidget()

        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel(
            "Configuración General"
        )

        titulo.setObjectName("tituloPrincipalSettings")

        layout.addWidget(
            titulo
        )

        descripcion = QLabel(
            "Configura los datos principales de tu aplicación."
        )

        descripcion.setObjectName("descripcionSettings")

        layout.addWidget(
            descripcion
        )

        formulario = QFormLayout()

        self.txt_nombre = QLineEdit()

        self.txt_nombre.setPlaceholderText(
            "Ingrese su nombre de usuario"
        )

        self.txt_nombre.setText(
            self.config.get(
                "nombre_usuario",
                ""
            )
        )

        formulario.addRow(
            "Nombre de usuario:",
            self.txt_nombre
        )

        self.combo_idioma = QComboBox()

        self.combo_idioma.addItem(
            "Español (es-ES)",
            "es-ES"
        )

        self.combo_idioma.addItem(
            "English (en-US)",
            "en-US"
        )

        posicion = self.combo_idioma.findData(
            self.config.get(
                "idioma",
                "es-ES"
            )
        )

        if posicion >= 0:
            self.combo_idioma.setCurrentIndex(
                posicion
            )

        formulario.addRow(
            "Idioma:",
            self.combo_idioma
        )

        self.spin_fuente = QSpinBox()

        self.spin_fuente.setMinimum(
            8
        )

        self.spin_fuente.setMaximum(
            40
        )

        self.spin_fuente.setValue(
            self.config.get(
                "tamano_fuente",
                12
            )
        )

        formulario.addRow(
            "Tamaño de fuente:",
            self.spin_fuente
        )

        layout.addLayout(formulario)

        layout.addStretch()

        self.crear_botonera_inferior(layout)

        return pagina

    # ========================================================
    # APARIENCIA

    def crear_apariencia(self):

        pagina = QWidget()

        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel(
            "Apariencia"
        )

        titulo.setObjectName("tituloPrincipalSettings")

        layout.addWidget(
            titulo
        )

        descripcion = QLabel(
            "Selecciona el tema que deseas utilizar."
        )

        descripcion.setObjectName("descripcionSettings")

        layout.addWidget(
            descripcion
        )

        formulario = QFormLayout()

        self.combo_tema = QComboBox()

        self.combo_tema.addItem(
            "Claro",
            "claro"
        )

        self.combo_tema.addItem(
            "Oscuro",
            "oscuro"
        )

        posicion = self.combo_tema.findData(
            self.config.get(
                "tema_interfaz",
                "oscuro"
            )
        )

        if posicion >= 0:
            self.combo_tema.setCurrentIndex(
                posicion
            )

        formulario.addRow(
            "Tema de interfaz:",
            self.combo_tema
        )

        layout.addLayout(formulario)

        titulo_preview = QLabel(
            "Vista previa"
        )

        titulo_preview.setObjectName("subtitulo")

        layout.addWidget(
            titulo_preview
        )

        self.preview = QWidget()

        self.preview.setObjectName("preview")

        preview_layout = QVBoxLayout()

        self.preview.setLayout(
            preview_layout
        )

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

        layout.addWidget(
            self.preview
        )

        layout.addStretch()

        self.crear_botonera_inferior(layout)

        return pagina

    # ========================================================
    # COLORES

    def crear_colores(self):

        pagina = QWidget()

        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel(
            "Colores"
        )

        titulo.setObjectName("tituloPrincipalSettings")

        layout.addWidget(
            titulo
        )

        descripcion = QLabel(
            "Personaliza los colores utilizados por la aplicación."
        )

        descripcion.setObjectName("descripcionSettings")

        layout.addWidget(
            descripcion
        )

        formulario = QFormLayout()

        # COLOR MENÚ

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

        # COLOR LETRA

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

        self.crear_botonera_inferior(layout)

        return pagina

    # ========================================================
    # CUENTA

    def crear_cuenta(self):

        pagina = QWidget()

        layout = QVBoxLayout()
        pagina.setLayout(layout)

        titulo = QLabel(
            "Cuenta"
        )

        titulo.setObjectName("tituloPrincipalSettings")

        layout.addWidget(
            titulo
        )

        descripcion = QLabel(
            "Personaliza tu información de perfil."
        )

        descripcion.setObjectName("descripcionSettings")

        layout.addWidget(
            descripcion
        )

        self.lbl_foto = QLabel(
            "👤"
        )

        self.lbl_foto.setObjectName(
            "fotoPerfil"
        )

        self.lbl_foto.setFixedSize(
            120,
            120
        )

        self.lbl_foto.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(
            self.lbl_foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.btn_foto = QPushButton(
            "Cambiar foto"
        )

        self.btn_foto.clicked.connect(
            self.seleccionar_foto
        )

        layout.addWidget(
            self.btn_foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        self.crear_botonera_inferior(layout)

        self.actualizar_foto()

        return pagina

    # ========================================================
    # FOTO

    def seleccionar_foto(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar foto de perfil",
            "",
            "Imágenes (*.png *.jpg *.jpeg *.bmp)"
        )

        if archivo:

            self.foto_seleccionada = archivo

            self.actualizar_foto()

    def actualizar_foto(self):

        if (
            self.foto_seleccionada
            and os.path.exists(
                self.foto_seleccionada
            )
        ):

            pixmap = QPixmap(
                self.foto_seleccionada
            )

            if not pixmap.isNull():

                pixmap_circular = aplicar_recorte_circular(pixmap, 120)

                self.lbl_foto.setPixmap(
                    pixmap_circular
                )

                self.lbl_foto.setText("")

                return

        self.lbl_foto.setPixmap(QPixmap())
        self.lbl_foto.setText(
            "👤"
        )

    # ========================================================
    # COLORES

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

    # ========================================================
    # GUARDAR

    def guardar(self):

        nombre = self.txt_nombre.text().strip()

        if not nombre:

            QMessageBox.warning(
                self,
                "Dato requerido",
                "Ingrese un nombre de usuario."
            )

            return

        self.config["nombre_usuario"] = nombre

        self.config["tema_interfaz"] = (
            self.combo_tema.currentData()
        )

        self.config["idioma"] = (
            self.combo_idioma.currentData()
        )

        self.config["tamano_fuente"] = (
            self.spin_fuente.value()
        )

        self.config["color_barra_menu"] = (
            self.color_menu
        )

        self.config["color_letra"] = (
            self.color_letra
        )

        self.config["foto_perfil"] = (
            self.foto_seleccionada
        )

        exito, mensaje = guardar_configuracion(
            self.config
        )

        if exito:

            if self.actualizar_principal:

                self.actualizar_principal(
                    self.config
                )

            self.accept()

        else:

            QMessageBox.critical(
                self,
                "Error",
                mensaje if mensaje else
                "No se pudo guardar la configuración."
            )

    # ========================================================
    # ESTILO SETTINGS

    def aplicar_estilo(self):

        self.setStyleSheet(
            """
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

            #tituloPrincipalSettings {
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

            #descripcionSettings {
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
                color: white;
                qproperty-alignment: 'AlignCenter';
            }
            """
        )

        self.cambiar_pagina(0)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()

    ventana.show()

    sys.exit(app.exec())