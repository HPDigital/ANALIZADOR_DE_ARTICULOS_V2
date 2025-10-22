"""
Ventana principal de la aplicación con interfaz Tkinter.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
from pathlib import Path
import threading
import logging
from datetime import datetime

from ..config.settings import Config
from ..utils.pdf_extractor import PDFExtractor
from ..analyzer import ArticleAnalyzer

logger = logging.getLogger(__name__)


class MainWindow:
    """Ventana principal de la aplicación."""

    def __init__(self, root: tk.Tk):
        """
        Inicializa la ventana principal.

        Args:
            root (tk.Tk): Ventana raíz de Tkinter.
        """
        self.root = root
        self.root.title("Analizador de Artículos Científicos")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)

        # Variables
        self.pdf_path = tk.StringVar()
        self.api_key = tk.StringVar()
        self.analyzer: ArticleAnalyzer = None
        self.current_results = {}
        self.is_analyzing = False

        # Configurar estilo
        self.setup_style()

        # Crear widgets
        self.create_widgets()

        # Cargar API key desde config si existe
        self.load_api_key()

        logger.info("Interfaz gráfica inicializada")

    def setup_style(self):
        """Configura el estilo de los widgets."""
        style = ttk.Style()
        style.theme_use('clam')

        # Configurar colores
        style.configure('Title.TLabel', font=('Helvetica', 16, 'bold'))
        style.configure('Subtitle.TLabel', font=('Helvetica', 10, 'bold'))
        style.configure('TButton', padding=6)
        style.configure('Success.TButton', foreground='green')

    def create_widgets(self):
        """Crea todos los widgets de la interfaz."""
        # Frame principal con padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Configurar grid
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Título
        title_label = ttk.Label(
            main_frame,
            text="📚 Analizador de Artículos Científicos",
            style='Title.TLabel'
        )
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)

        # Frame de configuración
        self.create_config_frame(main_frame)

        # Frame de análisis
        self.create_analysis_frame(main_frame)

        # Barra de estado
        self.create_status_bar(main_frame)

    def create_config_frame(self, parent):
        """Crea el frame de configuración."""
        config_frame = ttk.LabelFrame(parent, text="⚙️ Configuración", padding="10")
        config_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        config_frame.columnconfigure(1, weight=1)

        # API Key
        ttk.Label(config_frame, text="OpenAI API Key:").grid(
            row=0, column=0, sticky=tk.W, pady=5
        )
        api_entry = ttk.Entry(config_frame, textvariable=self.api_key, show="*", width=50)
        api_entry.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)

        ttk.Button(
            config_frame,
            text="👁️",
            width=3,
            command=self.toggle_api_key_visibility
        ).grid(row=0, column=2, pady=5)

        self.api_entry_widget = api_entry

        # Archivo PDF
        ttk.Label(config_frame, text="Archivo PDF:").grid(
            row=1, column=0, sticky=tk.W, pady=5
        )
        ttk.Entry(config_frame, textvariable=self.pdf_path, state='readonly').grid(
            row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5
        )
        ttk.Button(
            config_frame,
            text="📁 Seleccionar PDF",
            command=self.select_pdf
        ).grid(row=1, column=2, pady=5)

        # Botón de analizar
        self.analyze_button = ttk.Button(
            config_frame,
            text="🚀 Iniciar Análisis",
            command=self.start_analysis,
            style='Success.TButton'
        )
        self.analyze_button.grid(row=2, column=0, columnspan=3, pady=10)

    def create_analysis_frame(self, parent):
        """Crea el frame de análisis y resultados."""
        analysis_frame = ttk.LabelFrame(parent, text="📊 Análisis y Resultados", padding="10")
        analysis_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        analysis_frame.columnconfigure(0, weight=1)
        analysis_frame.rowconfigure(1, weight=1)

        # Frame superior con progreso
        progress_frame = ttk.Frame(analysis_frame)
        progress_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)

        self.progress_label = ttk.Label(progress_frame, text="Esperando inicio...")
        self.progress_label.grid(row=0, column=0, sticky=tk.W)

        self.progress_bar = ttk.Progressbar(
            progress_frame,
            mode='determinate',
            length=300
        )
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)

        # Notebook con pestañas para resultados
        self.notebook = ttk.Notebook(analysis_frame)
        self.notebook.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Pestaña de vista completa
        self.create_full_view_tab()

        # Botones de acciones
        button_frame = ttk.Frame(analysis_frame)
        button_frame.grid(row=2, column=0, pady=(10, 0))

        ttk.Button(
            button_frame,
            text="💾 Guardar Resultados",
            command=self.save_results
        ).pack(side=tk.LEFT, padx=5)

        ttk.Button(
            button_frame,
            text="🗑️ Limpiar",
            command=self.clear_results
        ).pack(side=tk.LEFT, padx=5)

    def create_full_view_tab(self):
        """Crea la pestaña de vista completa."""
        full_frame = ttk.Frame(self.notebook)
        self.notebook.add(full_frame, text="📄 Vista Completa")

        # Text widget con scroll
        self.results_text = scrolledtext.ScrolledText(
            full_frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Courier', 10)
        )
        self.results_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def create_status_bar(self, parent):
        """Crea la barra de estado."""
        self.status_label = ttk.Label(
            parent,
            text="Listo",
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status_label.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(10, 0))

    def load_api_key(self):
        """Carga la API key desde la configuración."""
        if Config.OPENAI_API_KEY:
            self.api_key.set(Config.OPENAI_API_KEY)
            logger.info("API key cargada desde configuración")

    def toggle_api_key_visibility(self):
        """Alterna la visibilidad de la API key."""
        if self.api_entry_widget['show'] == '*':
            self.api_entry_widget['show'] = ''
        else:
            self.api_entry_widget['show'] = '*'

    def select_pdf(self):
        """Abre un diálogo para seleccionar un archivo PDF."""
        filename = filedialog.askopenfilename(
            title="Seleccionar artículo PDF",
            filetypes=[("Archivos PDF", "*.pdf"), ("Todos los archivos", "*.*")]
        )
        if filename:
            self.pdf_path.set(filename)
            logger.info(f"PDF seleccionado: {filename}")
            self.update_status(f"PDF seleccionado: {Path(filename).name}")

    def start_analysis(self):
        """Inicia el análisis del artículo."""
        # Validaciones
        if not self.api_key.get():
            messagebox.showerror("Error", "Por favor, ingresa tu API Key de OpenAI")
            return

        if not self.pdf_path.get():
            messagebox.showerror("Error", "Por favor, selecciona un archivo PDF")
            return

        if self.is_analyzing:
            messagebox.showwarning("Advertencia", "Ya hay un análisis en progreso")
            return

        # Limpiar resultados anteriores
        self.clear_results()

        # Deshabilitar botón
        self.analyze_button.config(state='disabled')
        self.is_analyzing = True

        # Ejecutar análisis en hilo separado
        thread = threading.Thread(target=self.run_analysis, daemon=True)
        thread.start()

    def run_analysis(self):
        """Ejecuta el análisis en un hilo separado."""
        try:
            # Actualizar estado
            self.update_status("Extrayendo texto del PDF...")
            self.update_progress("Extrayendo texto...", 0, 10)

            # Extraer texto del PDF
            texto = PDFExtractor.extract_text(self.pdf_path.get())

            if not texto:
                self.show_error("El PDF no contiene texto extraíble")
                return

            self.update_progress("Texto extraído", 1, 10)

            # Inicializar analizador
            self.update_status("Inicializando analizador...")
            self.analyzer = ArticleAnalyzer(
                api_key=self.api_key.get(),
                model=Config.OPENAI_MODEL,
                max_tokens=Config.MAX_TOKENS
            )

            self.update_progress("Analizador inicializado", 2, 10)

            # Ejecutar análisis con callback de progreso
            self.update_status("Analizando artículo...")

            results = self.analyzer.analyze_article(
                texto,
                progress_callback=self.progress_callback
            )

            # Guardar y mostrar resultados
            self.current_results = results
            self.display_results(results)

            self.update_status("¡Análisis completado exitosamente!")
            messagebox.showinfo("Éxito", "El análisis se completó correctamente")

        except FileNotFoundError as e:
            self.show_error(f"Archivo no encontrado: {e}")

        except Exception as e:
            logger.error(f"Error durante el análisis: {e}", exc_info=True)
            self.show_error(f"Error durante el análisis: {str(e)}")

        finally:
            self.is_analyzing = False
            self.root.after(0, lambda: self.analyze_button.config(state='normal'))
            self.root.after(0, lambda: self.progress_bar.config(value=0))

    def progress_callback(self, step_name: str, step_description: str, current: int, total: int):
        """
        Callback para actualizar el progreso.

        Args:
            step_name (str): Nombre del paso.
            step_description (str): Descripción del paso.
            current (int): Paso actual.
            total (int): Total de pasos.
        """
        progress = (current / total) * 100
        self.update_progress(f"{step_description} ({current}/{total})", progress, 100)
        logger.info(f"Progreso: {current}/{total} - {step_description}")

    def display_results(self, results: dict):
        """
        Muestra los resultados del análisis.

        Args:
            results (dict): Diccionario con los resultados.
        """
        # Limpiar pestañas anteriores (excepto la primera)
        for i in range(len(self.notebook.tabs()) - 1, 0, -1):
            self.notebook.forget(i)

        # Actualizar vista completa
        self.results_text.delete(1.0, tk.END)
        full_text = self.format_full_results(results)
        self.results_text.insert(1.0, full_text)

        # Crear pestañas individuales para cada sección
        for step in ArticleAnalyzer.ANALYSIS_STEPS:
            if step.name in results:
                self.create_result_tab(step.description, results[step.name])

    def create_result_tab(self, title: str, content: str):
        """
        Crea una pestaña con un resultado específico.

        Args:
            title (str): Título de la pestaña.
            content (str): Contenido a mostrar.
        """
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title[:20])

        text_widget = scrolledtext.ScrolledText(
            frame,
            wrap=tk.WORD,
            width=80,
            height=20,
            font=('Courier', 10)
        )
        text_widget.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        text_widget.insert(1.0, content)
        text_widget.config(state='disabled')

    def format_full_results(self, results: dict) -> str:
        """
        Formatea todos los resultados para mostrar.

        Args:
            results (dict): Diccionario con resultados.

        Returns:
            str: Texto formateado.
        """
        output = []
        output.append("=" * 80)
        output.append("ANÁLISIS COMPLETO DEL ARTÍCULO CIENTÍFICO")
        output.append("=" * 80)
        output.append(f"\nFecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        output.append(f"Archivo: {Path(self.pdf_path.get()).name}")
        output.append("\n")

        for step in ArticleAnalyzer.ANALYSIS_STEPS:
            if step.name in results:
                output.append("\n" + "-" * 80)
                output.append(f"\n{step.description.upper()}")
                output.append("-" * 80)
                output.append(f"\n{results[step.name]}\n")

        return "\n".join(output)

    def save_results(self):
        """Guarda los resultados en un archivo."""
        if not self.current_results:
            messagebox.showwarning("Advertencia", "No hay resultados para guardar")
            return

        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")],
            initialfile=f"analisis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )

        if filename:
            try:
                with open(filename, 'w', encoding='utf-8') as f:
                    f.write(self.format_full_results(self.current_results))

                messagebox.showinfo("Éxito", f"Resultados guardados en:\n{filename}")
                logger.info(f"Resultados guardados en: {filename}")

            except Exception as e:
                messagebox.showerror("Error", f"Error al guardar: {e}")
                logger.error(f"Error al guardar resultados: {e}")

    def clear_results(self):
        """Limpia los resultados mostrados."""
        self.results_text.delete(1.0, tk.END)
        self.current_results = {}

        # Eliminar pestañas excepto la primera
        for i in range(len(self.notebook.tabs()) - 1, 0, -1):
            self.notebook.forget(i)

        self.update_status("Resultados limpiados")

    def update_status(self, message: str):
        """Actualiza la barra de estado."""
        self.root.after(0, lambda: self.status_label.config(text=message))

    def update_progress(self, message: str, value: float, maximum: float):
        """Actualiza la barra de progreso."""
        def update():
            self.progress_label.config(text=message)
            self.progress_bar.config(value=value, maximum=maximum)

        self.root.after(0, update)

    def show_error(self, message: str):
        """Muestra un mensaje de error."""
        self.root.after(0, lambda: messagebox.showerror("Error", message))
        self.update_status(f"Error: {message}")

    def run(self):
        """Inicia el bucle principal de la aplicación."""
        logger.info("Iniciando aplicación")
        self.root.mainloop()
