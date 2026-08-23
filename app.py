import os
import json
import shutil
from tkinter import Tk, Toplevel, Label, Entry, Button, Menu, messagebox, colorchooser, filedialog

# Pillow es necesario para poder mostrar JPG/JPEG (PhotoImage nativo de Tkinter solo soporta PNG/GIF/PPM)
try:
    from PIL import Image, ImageTk
    PIL_DISPONIBLE = True
except ImportError:
    PIL_DISPONIBLE = False

# Archivos de configuración
CONFIG_FILE = "config.json"
TEMP_FILE = "config.tmp"
BACKUP_FILE = "config.bak"

# Tamaño fijo para la miniatura de la foto de perfil
TAMANO_FOTO = (80, 80)

# Carpeta local donde se copian las fotos de perfil seleccionadas,
# para no depender de rutas virtuales/sincronizadas (ej. CrossDevice de Phone Link)
CARPETA_FOTOS = "fotos_perfil"

# Configuración por defecto
DEFAULT_CONFIG = {
    "nombre_usuario": "Usuario_Default",
    "tema_interfaz": "claro",
    "idioma": "es-ES",
    "tamano_fuente": 12,
    "color_barra_menu": "#d9d9d9",
    "color_letra": "#000000",
    "foto_perfil": ""
}


class AppConfig:
    """Clase encargada de la persistencia y manejo seguro de archivos."""

    @staticmethod
    def cargar_configuracion():
        if not os.path.exists(CONFIG_FILE):
            print("[INFO] Archivo no encontrado. Usando valores por defecto.")
            return DEFAULT_CONFIG.copy()

        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Validar que contenga las llaves necesarias
                for key in DEFAULT_CONFIG:
                    if key not in data:
                        raise ValueError(f"Falta el parámetro '{key}' en la configuración.")
                return data
        except (json.JSONDecodeError, ValueError) as e:
            messagebox.showwarning(
                "Error de Archivo",
                f"Archivo de configuración corrupto o inválido.\nSe cargará la configuración por defecto.\nDetalle: {e}"
            )
            return DEFAULT_CONFIG.copy()
        except PermissionError:
            messagebox.showerror(
                "Error de Permisos",
                "Sin permisos para leer el archivo de configuración.\nSe cargará la configuración por defecto."
            )
            return DEFAULT_CONFIG.copy()
        except Exception as e:
            messagebox.showerror("Error Inesperado", f"Error al leer la configuración: {e}")
            return DEFAULT_CONFIG.copy()

    @staticmethod
    def guardar_configuracion(config):
        try:
            # 1. Respaldo (Backup): Copiar el archivo original si existe
            if os.path.exists(CONFIG_FILE):
                shutil.copy2(CONFIG_FILE, BACKUP_FILE)

            # 2. Escritura segura: Guardar primero en archivo temporal (.tmp)
            with open(TEMP_FILE, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=4)

            # 3. Reemplazo atómico: Renombrar .tmp al archivo final
            if os.path.exists(CONFIG_FILE):
                os.remove(CONFIG_FILE)
            os.rename(TEMP_FILE, CONFIG_FILE)

            messagebox.showinfo("Éxito", "Configuración guardada correctamente.")
            return True

        except PermissionError:
            messagebox.showerror("Error de Permisos", "No se tienen permisos de escritura en el directorio.")
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            return False
        except Exception as e:
            messagebox.showerror("Error de Guardado", f"No se pudo guardar la configuración: {e}")
            if os.path.exists(TEMP_FILE):
                os.remove(TEMP_FILE)
            return False


class InterfazPrincipal:
    """Ventana principal y menú simulado."""

    def __init__(self, root):
        self.root = root
        self.root.title("Lab 1 - Gestión de Configuración")
        self.root.geometry("400x350")

        self.config = AppConfig.cargar_configuracion()
        self.crear_menu()

        # Label para la foto de perfil (se llena en aplicar_estilos)
        self.imagen_perfil = None  # referencia obligatoria para que no se recolecte como basura
        self.lbl_foto = Label(self.root)
        self.lbl_foto.pack(pady=(15, 5))

        self.lbl_bienvenida = Label(
            self.root,
            text=f"Bienvenido, {self.config['nombre_usuario']}",
            font=("Arial", self.config['tamano_fuente'])
        )
        self.lbl_bienvenida.pack(expand=True)

        self.aplicar_estilos()

    def crear_menu(self):
        menubar = Menu(self.root)

        # Subopciones simuladas
        menu_archivo = Menu(menubar, tearoff=0)
        menu_archivo.add_command(label="Nuevo (Simulado)", command=lambda: None)
        menu_archivo.add_command(label="Abrir (Simulado)", command=lambda: None)
        menubar.add_cascade(label="Archivo", menu=menu_archivo)

        menu_edicion = Menu(menubar, tearoff=0)
        menu_edicion.add_command(label="Copiar (Simulado)", command=lambda: None)
        menubar.add_cascade(label="Edición", menu=menu_edicion)

        menu_ver = Menu(menubar, tearoff=0)
        menu_ver.add_command(label="Zoom (Simulado)", command=lambda: None)
        menubar.add_cascade(label="Ver", menu=menu_ver)

        # Settings funcional
        menubar.add_command(label="Settings", command=self.abrir_settings)

        self.root.config(menu=menubar)

    def abrir_settings(self):
        VentanaSettings(self.root, self.config, self.actualizar_app)

    def actualizar_app(self, nueva_config):
        self.config = nueva_config
        self.lbl_bienvenida.config(
            text=f"Bienvenido, {self.config['nombre_usuario']}",
            font=("Arial", self.config['tamano_fuente'])
        )
        self.aplicar_estilos()

    def aplicar_estilos(self):
        """Aplica color de letra, color de fondo y foto de perfil a la ventana principal."""

        # --- Color de letra ---
        color_letra = self.config.get("color_letra", "#000000")
        self.lbl_bienvenida.config(fg=color_letra)

        # --- Color de fondo (simula la 'barra de menú' coloreando la ventana,
        #     ya que el widget Menu nativo de Tkinter ignora bg/fg en Windows) ---
        color_fondo = self.config.get("color_barra_menu", "#d9d9d9")
        self.root.config(bg=color_fondo)
        self.lbl_bienvenida.config(bg=color_fondo)
        self.lbl_foto.config(bg=color_fondo)

        # --- Foto de perfil ---
        ruta_foto = self.config.get("foto_perfil", "")
        if ruta_foto and os.path.exists(ruta_foto):
            try:
                if PIL_DISPONIBLE:
                    img = Image.open(ruta_foto)
                    img.thumbnail(TAMANO_FOTO)
                    self.imagen_perfil = ImageTk.PhotoImage(img)
                else:
                    # Fallback sin Pillow: solo funciona con PNG/GIF/PPM
                    from tkinter import PhotoImage
                    self.imagen_perfil = PhotoImage(file=ruta_foto)

                self.lbl_foto.config(image=self.imagen_perfil, text="")
            except Exception as e:
                self.imagen_perfil = None
                self.lbl_foto.config(image="", text=f"[No se pudo cargar la foto: {e}]")
        else:
            self.imagen_perfil = None
            self.lbl_foto.config(image="", text="")


class VentanaSettings:
    """Ventana de configuración del usuario."""

    def __init__(self, parent, config_actual, callback_actualizar):
        self.top = Toplevel(parent)
        self.top.title("Configuración de Usuario (Settings)")
        self.top.geometry("400x500")

        self.config = config_actual.copy()
        self.callback = callback_actualizar

        # Variable para almacenar la ruta de la foto seleccionada
        self.ruta_foto_seleccionada = self.config.get("foto_perfil", "")

        # Formulario de texto
        Label(self.top, text="Nombre de Usuario:").pack(anchor="w", padx=10, pady=2)
        self.entry_usuario = Entry(self.top)
        self.entry_usuario.insert(0, self.config["nombre_usuario"])
        self.entry_usuario.pack(fill="x", padx=10)

        Label(self.top, text="Tema (claro/oscuro):").pack(anchor="w", padx=10, pady=2)
        self.entry_tema = Entry(self.top)
        self.entry_tema.insert(0, self.config["tema_interfaz"])
        self.entry_tema.pack(fill="x", padx=10)

        Label(self.top, text="Idioma (ej. es-ES, en-US):").pack(anchor="w", padx=10, pady=2)
        self.entry_idioma = Entry(self.top)
        self.entry_idioma.insert(0, self.config["idioma"])
        self.entry_idioma.pack(fill="x", padx=10)

        Label(self.top, text="Tamaño de Fuente:").pack(anchor="w", padx=10, pady=2)
        self.entry_fuente = Entry(self.top)
        self.entry_fuente.insert(0, str(self.config["tamano_fuente"]))
        self.entry_fuente.pack(fill="x", padx=10)

        # Selectores de color
        Button(self.top, text="Seleccionar Color Barra Menú", command=self.seleccionar_color_menu).pack(
            fill="x", padx=10, pady=5)
        Button(self.top, text="Seleccionar Color Letra", command=self.seleccionar_color_letra).pack(
            fill="x", padx=10, pady=5)

        # Selector de Foto y Etiqueta para mostrar la ruta actual
        Button(self.top, text="Seleccionar Foto de Perfil", command=self.seleccionar_foto).pack(
            fill="x", padx=10, pady=5)

        texto_foto_inicial = self.ruta_foto_seleccionada if self.ruta_foto_seleccionada else "Ninguna foto seleccionada"
        self.lbl_foto_ruta = Label(self.top, text=f"Foto: {texto_foto_inicial}", fg="gray", wraplength=350, justify="left")
        self.lbl_foto_ruta.pack(fill="x", padx=10)

        # Vista previa de la foto seleccionada
        self.preview_foto = None
        self.lbl_preview = Label(self.top)
        self.lbl_preview.pack(pady=5)
        self._actualizar_preview()

        # Botón Guardar
        Button(self.top, text="Guardar Configuración", bg="#4CAF50", fg="white", command=self.guardar).pack(
            fill="x", padx=10, pady=15)

    def seleccionar_color_menu(self):
        color = colorchooser.askcolor(title="Color Barra de Menú")[1]
        if color:
            self.config["color_barra_menu"] = color

    def seleccionar_color_letra(self):
        color = colorchooser.askcolor(title="Color de Letra")[1]
        if color:
            self.config["color_letra"] = color

    def seleccionar_foto(self):
        ruta = filedialog.askopenfilename(filetypes=[("Imágenes", "*.png *.jpg *.jpeg *.gif")])
        if not ruta:
            return

        # Validar que el archivo realmente se pueda abrir como imagen antes de aceptarlo.
        # Esto detecta casos como rutas de "CrossDevice"/Phone Link donde el archivo
        # mostrado es solo un placeholder aún no sincronizado.
        try:
            if PIL_DISPONIBLE:
                with Image.open(ruta) as img_test:
                    img_test.verify()
            elif not os.path.getsize(ruta) > 0:
                raise ValueError("El archivo está vacío.")
        except Exception as e:
            messagebox.showerror(
                "Imagen no válida",
                f"El archivo seleccionado no se pudo leer como imagen.\n"
                f"Si viene de 'Enlace con tu teléfono' (CrossDevice), es posible que aún no "
                f"se haya descargado por completo. Intenta copiarla primero a una carpeta "
                f"local (ej. Escritorio o Documentos) y selecciónala de nuevo.\n\nDetalle: {e}"
            )
            return

        # Copiar la imagen a una carpeta local propia de la app, para no depender
        # de rutas virtuales/sincronizadas que puedan desaparecer o dar errores.
        try:
            os.makedirs(CARPETA_FOTOS, exist_ok=True)
            nombre_archivo = os.path.basename(ruta)
            destino = os.path.join(CARPETA_FOTOS, nombre_archivo)

            # Evitar colisiones de nombre si ya existe una foto distinta con el mismo nombre
            base, ext = os.path.splitext(nombre_archivo)
            contador = 1
            while os.path.exists(destino) and not self._mismo_archivo(ruta, destino):
                destino = os.path.join(CARPETA_FOTOS, f"{base}_{contador}{ext}")
                contador += 1

            shutil.copy2(ruta, destino)
            ruta_final = destino
        except Exception as e:
            messagebox.showwarning(
                "Aviso",
                f"No se pudo copiar la foto a una carpeta local, se usará la ruta original.\nDetalle: {e}"
            )
            ruta_final = ruta

        self.ruta_foto_seleccionada = ruta_final
        self.lbl_foto_ruta.config(text=f"Foto: {ruta_final}", fg="green")
        self._actualizar_preview()

    @staticmethod
    def _mismo_archivo(ruta_a, ruta_b):
        try:
            return os.path.getsize(ruta_a) == os.path.getsize(ruta_b)
        except OSError:
            return False

    def _actualizar_preview(self):
        """Muestra una vista previa pequeña de la foto seleccionada dentro de Settings."""
        if self.ruta_foto_seleccionada and os.path.exists(self.ruta_foto_seleccionada):
            try:
                if PIL_DISPONIBLE:
                    img = Image.open(self.ruta_foto_seleccionada)
                    img.thumbnail(TAMANO_FOTO)
                    self.preview_foto = ImageTk.PhotoImage(img)
                else:
                    from tkinter import PhotoImage
                    self.preview_foto = PhotoImage(file=self.ruta_foto_seleccionada)
                self.lbl_preview.config(image=self.preview_foto, text="")
            except Exception as e:
                self.preview_foto = None
                self.lbl_preview.config(image="", text=f"[No se pudo previsualizar: {e}]")
        else:
            self.preview_foto = None
            self.lbl_preview.config(image="", text="")

    def guardar(self):
        try:
            # Asignar campos de texto
            self.config["nombre_usuario"] = self.entry_usuario.get()
            self.config["tema_interfaz"] = self.entry_tema.get()
            self.config["idioma"] = self.entry_idioma.get()
            self.config["tamano_fuente"] = int(self.entry_fuente.get())

            # Asignar la ruta de la foto de perfil
            self.config["foto_perfil"] = self.ruta_foto_seleccionada

            # Guardar en archivo JSON
            if AppConfig.guardar_configuracion(self.config):
                self.callback(self.config)
                self.top.destroy()
        except ValueError:
            messagebox.showerror("Error de Entrada", "El tamaño de fuente debe ser un número entero válido.")


if __name__ == "__main__":
    if not PIL_DISPONIBLE:
        print("[AVISO] Pillow no está instalado. Instálalo con 'pip install pillow' para poder usar fotos JPG/JPEG.")

    root = Tk()
    app = InterfazPrincipal(root)
    root.mainloop()