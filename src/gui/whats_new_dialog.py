import customtkinter as ctk
import os
from PIL import Image

# =============================================================================
# CONFIGURACIÓN DEL CONTENIDO DE LA VERSIÓN (EDITAR AQUÍ PARA CADA VERSIÓN)
# =============================================================================
VERSION_TITLE = "DowP 1.4.2: Integración con DaVinci Resolve Studio"

VERSION_TEXT = """Esta actualización se centra en potenciar el flujo de trabajo de los editores, incorporando compatibilidad directa con DaVinci Resolve, mejoras en la organización dentro de Premiere y opciones de instalación más flexibles.

Novedades y Mejoras Principales:

• Integración con DaVinci Resolve (Solo versión Studio):
  - Ahora puedes enviar todas tus descargas y medios procesados de forma automática al Media Pool de DaVinci Resolve.
  - Importación a la Línea de Tiempo: También tienes la opción de insertar los medios directamente en tu línea de tiempo activa, justo donde esté el cabezal de reproducción (esta acción es segura y no desconfigura tu edición actual).
  - Categorización Inteligente: DaVinci organizará automáticamente los medios importados en subcarpetas de Video, Audio e Imagen en tu Media Pool.

• Nueva sección "Integraciones": Hemos reorganizado el panel de configuración. Las opciones para conectar DowP con Adobe y DaVinci Resolve ahora se encuentran agrupadas de forma clara en los ajustes.

• Limpieza Automática de Títulos: Se ha añadido una nueva función para evitar errores de importación causados por caracteres especiales (muy útil para DaVinci Resolve y versiones antiguas de Premiere). Al activarla, se limpian los títulos automáticamente, manteniendo intacto el soporte para idiomas como el japonés o chino.

• Mejoras en DowP Importer (Adobe): El importador para Adobe ha sido mejorado y ahora organiza automáticamente los medios importados creando subcarpetas dedicadas para Video, Audio e Imagen dentro del proyecto.

• Flexibilidad en el Instalador (Setup): Hemos devuelto la posibilidad de elegir rutas personalizadas para la instalación de DowP en cualquier parte de tu disco duro. (Nota: Por compatibilidad, sigue siendo necesario evitar carpetas del sistema que exijan permisos de administrador como Program Files o ProgramData).

Bugs Conocidos:
• Descargas por Lotes: Actualmente existe un problema al utilizar el botón "Aplicar Modo Global". Recomendamos no usar esta opción por ahora mientras trabajamos en su corrección para la próxima versión."""

# =============================================================================

class WhatsNewDialog(ctk.CTkToplevel):
    def __init__(self, master, go_to_integrations_callback=None, *args, **kwargs):
        super().__init__(master, *args, **kwargs)
        self.title("Novedades de la Versión")
        
        # Centrar la ventana en la pantalla
        window_width = 700
        window_height = 550
        
        # Obtener dimensiones de la pantalla
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        # Calcular posición (x, y)
        x_cordinate = int((screen_width/2) - (window_width/2))
        y_cordinate = int((screen_height/2) - (window_height/2))
        
        self.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")
        self.minsize(600, 400)
        
        self.transient(master)  # Hace que la ventana dependa de la principal
        self.grab_set()         # Bloquea la interacción con la ventana principal hasta que esta se cierre
        
        # Configurar icono si existe
        try:
            from .dialogs import apply_icon
            apply_icon(self)
        except:
            pass

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # 1. Título
        title_label = ctk.CTkLabel(
            self, 
            text=VERSION_TITLE, 
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.grid(row=0, column=0, padx=20, pady=(20, 10), sticky="w")

        # 2. Contenido Textual (Scrollable)
        textbox = ctk.CTkTextbox(
            self, 
            wrap="word", 
            font=ctk.CTkFont(size=14),
            fg_color="transparent"
        )
        textbox.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="nsew")
        textbox.insert("0.0", VERSION_TEXT)
        textbox.configure(state="disabled") # Solo lectura

        # 3. Frame para Botones/Enlaces inferiores
        bottom_frame = ctk.CTkFrame(self, fg_color="transparent")
        bottom_frame.grid(row=2, column=0, padx=20, pady=(0, 20), sticky="ew")
        bottom_frame.grid_columnconfigure(0, weight=1)
        bottom_frame.grid_columnconfigure(1, weight=0)

        # Enlace opcional a las integraciones (SE PUEDE BORRAR EN FUTURAS VERSIONES)
        if go_to_integrations_callback:
            link_btn = ctk.CTkButton(
                bottom_frame, 
                text="Estas nuevas opciones estan en Ajustes-General-en la seccin de Integraciones", 
                fg_color="transparent",
                hover_color="#2c2c2c",  # Color de hover sutil
                text_color="#1f538d",   # Color azul tipo enlace (ajustar si usas tema oscuro)
                font=ctk.CTkFont(underline=True),
                command=lambda: self._on_link_click(go_to_integrations_callback)
            )
            # Adaptar el color del enlace según el tema actual si es posible
            if ctk.get_appearance_mode() == "Dark":
                link_btn.configure(text_color="#569cd6")
                
            link_btn.grid(row=0, column=0, sticky="w")

        # Botón de cerrar (Entendido)
        close_btn = ctk.CTkButton(
            bottom_frame, 
            text="¡Entendido!", 
            width=120,
            command=self.destroy
        )
        close_btn.grid(row=0, column=1, sticky="e")

        # Asegurar foco
        self.focus_force()

    def _on_link_click(self, callback):
        """Maneja el clic en el enlace, cierra la ventana y ejecuta el callback"""
        try:
            callback()
        except Exception as e:
            print(f"DEBUG: Error al ejecutar el callback del Splash Screen: {e}")
        finally:
            self.destroy()
