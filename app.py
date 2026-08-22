import os
import json
import shutil
from tkinter import Tk, Toplevel, Label, Entry, Button, Menu, messagebox, colorchooser, filedialog

# Archivos de configuración
CONFIG_FILE = "config.json"
TEMP_FILE = "config.tmp"
BACKUP_FILE = "config.bak"

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
            messagebox.showwarning("Error de Archivo", f"Archivo de configuración corrupto o inválido.\nSe cargará la configuración por defecto.\nDetalle: {e}")
            return DEFAULT_CONFIG.copy()
        except PermissionError:
            messagebox.showerror("Error de Permisos", "Sin permisos para leer el archivo de configuración.\nSe cargará la configuración por defecto.")
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
        self.root.geometry("400x300")

        self.config = AppConfig.cargar_configuracion()
        self.crear_menu()

        self.lbl_bienvenida = Label(self.root, text=f"Bienvenido, {self.config['nombre_usuario']}", font=("Arial", self.config['tamano_fuente']))
        self.lbl_bienvenida.pack(expand=True)

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
        self.lbl_bienvenida.config(text=f"Bienvenido, {self.config['nombre_usuario']}", font=("Arial", self.config['tamano_fuente']))

class VentanaSettings:
    """Ventana de configuración del usuario."""
    def __init__(self, parent, config_actual, callback_actualizar):
        self.top = Toplevel(parent)
        self.top.title("Configuración de Usuario (Settings)")
        self.top.geometry("380x420")
        
        self.config = config_actual.copy()
        self.callback = callback_actualizar

        # Formulario
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

        # Selectores
        Button(self.top, text="Seleccionar Color Barra Menú", command=self.seleccionar_color_menu).pack(fill="x", padx=10, pady=5)
        Button(self.top, text="Seleccionar Color Letra", command=self.seleccionar_color_letra).pack(fill="x", padx=10, pady=5)
        Button(self.top, text="Seleccionar Foto de Perfil", command=self.seleccionar_foto).pack(fill="x", padx=10, pady=5)

        Button(self.top, text="Guardar Configuración", bg="#4CAF50", fg="white", command=self.guardar).pack(fill="x", padx=10, pady=15)

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
        if ruta:
            self.config["foto_perfil"] = ruta

    def guardar(self):
        try:
            self.config["nombre_usuario"] = self.entry_usuario.get()
            self.config["tema_interfaz"] = self.entry_tema.get()
            self.config["idioma"] = self.entry_idioma.get()
            self.config["tamano_fuente"] = int(self.entry_fuente.get())

            if AppConfig.guardar_configuracion(self.config):
                self.callback(self.config)
                self.top.destroy()
        except ValueError:
            messagebox.showerror("Error de Entrada", "El tamaño de fuente debe ser un número entero válido.")

if __name__ == "__main__":
    root = Tk()
    app = InterfazPrincipal(root)
    root.mainloop()