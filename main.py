#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Punto de entrada principal de la aplicación.
Analizador de Artículos Científicos con interfaz gráfica Tkinter.
"""

import tkinter as tk
import sys
import logging
from pathlib import Path

# Agregar el directorio src al path
sys.path.insert(0, str(Path(__file__).parent))

from src.config.settings import Config
from src.utils.logger import setup_logger
from src.gui.main_window import MainWindow


def main():
    """Función principal de la aplicación."""
    # Configurar logging
    logger = setup_logger(__name__, level=logging.INFO)
    logger.info("Iniciando Analizador de Artículos Científicos V2")

    # Validar configuración básica
    if not Config.validate():
        logger.warning("Configuración incompleta. Por favor configura tu API key.")
        # La aplicación continúa, pero el usuario deberá ingresar la API key manualmente

    try:
        # Crear ventana principal
        root = tk.Tk()

        # Crear e iniciar aplicación
        app = MainWindow(root)
        app.run()

    except Exception as e:
        logger.error(f"Error fatal en la aplicación: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
