import os
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QHBoxLayout, QVBoxLayout, QFrame, QLabel, QPushButton
from PyQt6.QtWidgets import QDialog, QLineEdit, QComboBox, QSpinBox
from PyQt6.QtWidgets import QColorDialog, QFileDialog, QMessageBox
from PyQt6.QtGui import QAction, QFont
from PyQt6.QtCore import Qt

from PyQt6.QtWidgets import QLabel,QPushButton,QStackedWidget
from PyQt6.QtGui import QPixmap

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

        panel_izquierdo.setFixedWidth(310)

        layout_izquierdo = QVBoxLayout()

        layout_izquierdo.setContentsMargins(
            20,
            0,
            20,
            0
        )

        layout_izquierdo.setAlignment(
            Qt.AlignmentFlag.AlignTop
        )


        # FOTO
        self.foto_principal = QLabel()

        self.foto_principal.setFixedSize(
            180,
            180
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

        self.lbl_bienvenida.setFont(
            QFont(
                "Arial",
                28,
                QFont.Weight.Bold
            )
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

        descripcion.setFont(
            QFont(
                "Arial",
                13
            )
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

        self.icono_settings.setFont(
            QFont(
                "Arial",
                80
            )
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

        titulo.setFont(
            QFont(
                "Arial",
                28,
                QFont.Weight.Bold
            )
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

        descripcion_central.setFont(
            QFont(
                "Arial",
                14
            )
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

        self.btn_settings.setFixedSize(
            275,
            65
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
            "#20232A"
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

        # TEMA OSCURO
        if tema == "oscuro":

            fondo = "#15171C"
            texto = "#EDEDED"
            texto_secundario = "#AAAAAA"
            morado = "#7048A8"
            morado_claro = "#A978E0"

        # TEMA CLARO
        else:

            fondo = "#F4F4F5"
            texto = "#222222"
            texto_secundario = "#666666"
            morado = "#7048A8"
            morado_claro = "#7048A8"

        # NOMBRE

        self.lbl_bienvenida.setText(
            f"¡Bienvenido, {nombre}!"
        )



        # FOTO
        if foto and os.path.exists(foto):

            pixmap = QPixmap(foto)

            if not pixmap.isNull():

                pixmap = pixmap.scaled(
                    170,
                    170,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

                self.foto_principal.setPixmap(
                    pixmap
                )

            else:

                self.foto_principal.setText(
                    "Sin fotografía"
                )

        else:

            self.foto_principal.setText(
                "Sin fotografía"
            )

        # ESTILO
        self.setStyleSheet(
            f"""
            QMainWindow {{
                background-color: {fondo};
            }}

            QWidget {{
                background-color: {fondo};
                color: {texto};
                font-size: {tamano}px;
            }}

            QMenuBar {{
                background-color: {color_menu};
                color: {color_letra};
                padding: 8px 20px;
                border: none;
            }}

            QMenuBar::item {{
                background-color: transparent;
                padding: 8px 16px;
                margin-right: 8px;
            }}

            QMenuBar::item:selected {{
                background-color: {morado};
                border-radius: 6px;
            }}

            QMenu {{
                background-color: #20232A;
                color: #EDEDED;
                border: 1px solid #3A3D46;
                padding: 5px;
            }}

            QMenu::item {{
                padding: 8px 25px;
            }}

            QMenu::item:selected {{
                background-color: {morado};
                border-radius: 5px;
            }}

            QLabel#fotoPrincipal {{
                background-color: {morado};
                border-radius: 90px;
                color: {texto};
                font-size: 14px;
            }}

            QLabel#bienvenida {{
                color: {morado_claro};
            }}

            QLabel#descripcionIzquierda {{
                color: {texto};
            }}

            QLabel#iconoSettings {{
                color: {morado_claro};
                background-color: transparent;
            }}

            QLabel#tituloPrincipal {{
                color: {texto};
            }}

            QLabel#descripcionCentral {{
                color: {texto_secundario};
            }}

            QPushButton {{
                background-color: {morado};
                color: white;
                border: none;
                border-radius: 12px;
                font-size: 18px;
                font-weight: bold;
            }}

            QPushButton:hover {{
                background-color: #8259BC;
            }}

            QPushButton:pressed {{
                background-color: #603A91;
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
            "#20232A"
        )

        self.color_letra = self.config.get(
            "color_letra",
            "#EDEDED"
        )

        self.foto_seleccionada = self.config.get(
            "foto_perfil",
            ""
        )

        self.setWindowTitle(
            "Settings"
        )

        self.setMinimumSize(
            850,
            560
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
        sidebar = QFrame()

        sidebar.setFixedWidth(200)

        sidebar_layout = QVBoxLayout()

        sidebar_layout.setContentsMargins(
            20,
            30,
            20,
            20
        )

        titulo = QLabel("SETTINGS")

        titulo.setFont(
            QFont(
                "Arial",
                18,
                QFont.Weight.Bold
            )
        )

        sidebar_layout.addWidget(
            titulo
        )

        subtitulo = QLabel(
            "Configuración"
        )

        sidebar_layout.addWidget(
            subtitulo
        )

        sidebar_layout.addSpacing(30)

        self.btn_general = self.crear_boton(
            "General"
        )

        self.btn_apariencia = self.crear_boton(
            "Apariencia"
        )

        self.btn_colores = self.crear_boton(
            "Colores"
        )

        self.btn_cuenta = self.crear_boton(
            "Cuenta"
        )

        sidebar_layout.addWidget(
            self.btn_general
        )

        sidebar_layout.addWidget(
            self.btn_apariencia
        )

        sidebar_layout.addWidget(
            self.btn_colores
        )

        sidebar_layout.addWidget(
            self.btn_cuenta
        )

        sidebar_layout.addStretch()

        sidebar.setLayout(
            sidebar_layout
        )


        # STACK

        contenido = QWidget()

        contenido_layout = QVBoxLayout()

        contenido_layout.setContentsMargins(
            35,
            30,
            35,
            25
        )

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

        # GUARDAR

        botones = QHBoxLayout()

        botones.addStretch()

        cancelar = QPushButton(
            "Cancelar"
        )

        cancelar.clicked.connect(
            self.reject
        )

        guardar = QPushButton(
            "Guardar cambios"
        )

        guardar.clicked.connect(
            self.guardar
        )

        botones.addWidget(
            cancelar
        )

        botones.addWidget(
            guardar
        )

        contenido_layout.addLayout(
            botones
        )

        contenido.setLayout(
            contenido_layout
        )

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

        layout.addWidget(sidebar)
        layout.addWidget(contenido)

        self.setLayout(layout)

    # ========================================================
    # BOTÓN SIDEBAR

    def crear_boton(self, texto):

        boton = QPushButton(texto)

        boton.setMinimumHeight(42)

        boton.setCursor(
            Qt.CursorShape.PointingHandCursor
        )

        return boton

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

        for boton in botones:

            boton.setProperty(
                "activo",
                False
            )

            boton.style().unpolish(
                boton
            )

            boton.style().polish(
                boton
            )

        boton = botones[indice]

        boton.setProperty(
            "activo",
            True
        )

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

        titulo = QLabel(
            "General"
        )

        titulo.setFont(
            QFont(
                "Arial",
                24,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Configura los datos generales de la aplicación."
            )
        )

        layout.addSpacing(20)

        layout.addWidget(
            QLabel(
                "Nombre de usuario"
            )
        )

        self.txt_nombre = QLineEdit()

        self.txt_nombre.setText(
            self.config.get(
                "nombre_usuario",
                ""
            )
        )

        layout.addWidget(
            self.txt_nombre
        )

        layout.addWidget(
            QLabel(
                "Idioma"
            )
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

        layout.addWidget(
            self.combo_idioma
        )

        layout.addWidget(
            QLabel(
                "Tamaño de fuente"
            )
        )

        self.spin_fuente = QSpinBox()

        self.spin_fuente.setRange(
            8,
            40
        )

        self.spin_fuente.setValue(
            self.config.get(
                "tamano_fuente",
                12
            )
        )

        layout.addWidget(
            self.spin_fuente
        )

        layout.addStretch()

        pagina.setLayout(layout)

        return pagina

    # ========================================================
    # APARIENCIA


    def crear_apariencia(self):

        pagina = QWidget()

        layout = QVBoxLayout()

        titulo = QLabel(
            "Apariencia"
        )

        titulo.setFont(
            QFont(
                "Arial",
                24,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Selecciona el tema de la interfaz."
            )
        )

        layout.addSpacing(20)

        layout.addWidget(
            QLabel(
                "Tema de interfaz"
            )
        )

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

        layout.addWidget(
            self.combo_tema
        )

        layout.addSpacing(20)

        layout.addWidget(
            QLabel(
                "Vista previa"
            )
        )

        self.preview = QFrame()

        self.preview.setMinimumHeight(
            180
        )

        preview_layout = QVBoxLayout()

        texto = QLabel(
            "Gestión de Configuración de Usuario"
        )

        texto.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        texto.setFont(
            QFont(
                "Arial",
                18,
                QFont.Weight.Bold
            )
        )

        preview_layout.addStretch()
        preview_layout.addWidget(texto)
        preview_layout.addStretch()

        self.preview.setLayout(
            preview_layout
        )

        layout.addWidget(
            self.preview
        )

        layout.addStretch()

        pagina.setLayout(layout)

        self.combo_tema.currentIndexChanged.connect(
            self.actualizar_preview
        )

        self.actualizar_preview()

        return pagina

    # ========================================================
    # COLORES

    def crear_colores(self):

        pagina = QWidget()

        layout = QVBoxLayout()

        titulo = QLabel(
            "Colores"
        )

        titulo.setFont(
            QFont(
                "Arial",
                24,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Personaliza los colores de la interfaz."
            )
        )

        layout.addSpacing(25)

        # COLOR MENÚ

        fila_menu = QHBoxLayout()

        fila_menu.addWidget(
            QLabel(
                "Color de barra de menú"
            )
        )

        fila_menu.addStretch()

        self.btn_color_menu = QPushButton(
            self.color_menu
        )

        self.btn_color_menu.setFixedWidth(
            150
        )

        self.btn_color_menu.clicked.connect(
            self.seleccionar_color_menu
        )

        fila_menu.addWidget(
            self.btn_color_menu
        )

        layout.addLayout(
            fila_menu
        )

        # COLOR LETRA

        fila_letra = QHBoxLayout()

        fila_letra.addWidget(
            QLabel(
                "Color de letra"
            )
        )

        fila_letra.addStretch()

        self.btn_color_letra = QPushButton(
            self.color_letra
        )

        self.btn_color_letra.setFixedWidth(
            150
        )

        self.btn_color_letra.clicked.connect(
            self.seleccionar_color_letra
        )

        fila_letra.addWidget(
            self.btn_color_letra
        )

        layout.addLayout(
            fila_letra
        )

        layout.addStretch()

        pagina.setLayout(layout)

        return pagina

    # ========================================================
    # CUENTA

    def crear_cuenta(self):

        pagina = QWidget()

        layout = QVBoxLayout()

        titulo = QLabel(
            "Cuenta"
        )

        titulo.setFont(
            QFont(
                "Arial",
                24,
                QFont.Weight.Bold
            )
        )

        layout.addWidget(
            titulo
        )

        layout.addWidget(
            QLabel(
                "Configura tu fotografía de perfil."
            )
        )

        layout.addSpacing(20)

        self.lbl_foto = QLabel(
            "Sin fotografía"
        )

        self.lbl_foto.setFixedSize(
            180,
            180
        )

        self.lbl_foto.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.lbl_foto.setObjectName(
            "fotoSettings"
        )

        layout.addWidget(
            self.lbl_foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        self.btn_foto = QPushButton(
            "Seleccionar fotografía"
        )

        self.btn_foto.clicked.connect(
            self.seleccionar_foto
        )

        layout.addWidget(
            self.btn_foto,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addStretch()

        pagina.setLayout(layout)

        self.actualizar_foto()

        return pagina

    # ========================================================
    # FOTO

    def seleccionar_foto(self):

        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Seleccionar fotografía",
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

                pixmap = pixmap.scaled(
                    160,
                    160,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )

                self.lbl_foto.setPixmap(
                    pixmap
                )

                return

        self.lbl_foto.setText(
            "Sin fotografía"
        )

    # ========================================================
    # COLORES

    def seleccionar_color_menu(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.color_menu = color.name()

            self.btn_color_menu.setText(
                self.color_menu
            )

    def seleccionar_color_letra(self):

        color = QColorDialog.getColor()

        if color.isValid():

            self.color_letra = color.name()

            self.btn_color_letra.setText(
                self.color_letra
            )

    # ========================================================
    # PREVIEW

    def actualizar_preview(self):

        if self.combo_tema.currentData() == "oscuro":

            self.preview.setStyleSheet(
                """
                QFrame {
                    background-color: #15171C;
                    border: 1px solid #3A3D46;
                    border-radius: 12px;
                }

                QLabel {
                    color: #EDEDED;
                }
                """
            )

        else:

            self.preview.setStyleSheet(
                """
                QFrame {
                    background-color: #F4F4F4;
                    border: 1px solid #CCCCCC;
                    border-radius: 12px;
                }

                QLabel {
                    color: #222222;
                }
                """
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

            QMessageBox.information(
                self,
                "Configuración",
                mensaje if mensaje else
                "¡Configuración guardada con éxito!"
            )

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
            }

            QLineEdit,
            QComboBox,
            QSpinBox {
                background-color: #20232A;
                color: #EDEDED;
                border: 1px solid #3A3D46;
                border-radius: 8px;
                padding: 9px;
            }

            QPushButton {
                background-color: #7048A8;
                color: white;
                border: none;
                border-radius: 8px;
                padding: 10px 16px;
            }

            QPushButton:hover {
                background-color: #8259BC;
            }

            QPushButton[activo="true"] {
                background-color: #7048A8;
            }

            QPushButton[activo="false"] {
                background-color: #20232A;
            }

            QLabel#fotoSettings {
                background-color: #20232A;
                border: 2px solid #7048A8;
                border-radius: 90px;
            }
            """
        )

        self.cambiar_pagina(0)


if __name__ == "__main__":

    app = QApplication(sys.argv)

    ventana = VentanaPrincipal()

    ventana.show()

    sys.exit(app.exec())