"""
Configuración de la aplicación.
Maneja variables de entorno y configuraciones globales.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
load_dotenv()


class Config:
    """Clase de configuración centralizada."""

    # Directorio raíz del proyecto
    BASE_DIR = Path(__file__).resolve().parent.parent.parent

    # API Keys
    OPENAI_API_KEY: Optional[str] = os.getenv("OPENAI_API_KEY")

    # Configuración de OpenAI
    OPENAI_MODEL: str = os.getenv("OPENAI_MODEL", "gpt-4o-2024-08-06")
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))

    # Directorios
    OUTPUT_DIR = BASE_DIR / "output"
    TEMP_DIR = BASE_DIR / "temp"

    @classmethod
    def validate(cls) -> bool:
        """
        Valida que todas las configuraciones necesarias estén presentes.

        Returns:
            bool: True si la configuración es válida, False en caso contrario.
        """
        if not cls.OPENAI_API_KEY:
            return False

        # Crear directorios necesarios
        cls.OUTPUT_DIR.mkdir(exist_ok=True)
        cls.TEMP_DIR.mkdir(exist_ok=True)

        return True

    @classmethod
    def get_api_key(cls) -> str:
        """
        Obtiene la API key de OpenAI.

        Returns:
            str: API key de OpenAI.

        Raises:
            ValueError: Si la API key no está configurada.
        """
        if not cls.OPENAI_API_KEY:
            raise ValueError(
                "OPENAI_API_KEY no está configurada. "
                "Por favor, configura tu API key en el archivo .env"
            )
        return cls.OPENAI_API_KEY
