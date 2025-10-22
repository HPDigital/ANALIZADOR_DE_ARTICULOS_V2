"""
Módulo para extracción de texto desde archivos PDF.
"""

import fitz  # PyMuPDF
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)


class PDFExtractor:
    """Clase para extraer texto de documentos PDF."""

    @staticmethod
    def extract_text(pdf_path: str) -> Optional[str]:
        """
        Extrae texto de un archivo PDF.

        Args:
            pdf_path (str): Ruta al archivo PDF.

        Returns:
            Optional[str]: Texto extraído del PDF, o None si hay error.

        Raises:
            FileNotFoundError: Si el archivo no existe.
            ValueError: Si el archivo no es un PDF válido.
        """
        try:
            # Validar que el archivo existe
            path = Path(pdf_path)
            if not path.exists():
                raise FileNotFoundError(f"El archivo no existe: {pdf_path}")

            if not path.suffix.lower() == '.pdf':
                raise ValueError(f"El archivo no es un PDF: {pdf_path}")

            logger.info(f"Extrayendo texto de: {pdf_path}")

            # Abrir el documento PDF
            documento = fitz.open(pdf_path)

            # Recopilar el texto de cada página
            texto_completo = ""
            total_paginas = len(documento)

            for num_pagina, pagina in enumerate(documento, start=1):
                logger.debug(f"Procesando página {num_pagina}/{total_paginas}")
                texto_pagina = pagina.get_text()
                texto_completo += texto_pagina + "\n"

            # Cerrar el documento
            documento.close()

            if not texto_completo.strip():
                logger.warning("El PDF no contiene texto extraíble")
                return None

            logger.info(
                f"Extracción completada: {len(texto_completo)} caracteres, "
                f"{total_paginas} páginas"
            )

            return texto_completo.strip()

        except FileNotFoundError as e:
            logger.error(f"Archivo no encontrado: {e}")
            raise

        except ValueError as e:
            logger.error(f"Error de validación: {e}")
            raise

        except Exception as e:
            logger.error(f"Error al extraer texto del PDF: {e}")
            raise RuntimeError(f"Error al procesar el PDF: {e}")

    @staticmethod
    def get_pdf_info(pdf_path: str) -> dict:
        """
        Obtiene información metadata del PDF.

        Args:
            pdf_path (str): Ruta al archivo PDF.

        Returns:
            dict: Diccionario con información del PDF.
        """
        try:
            documento = fitz.open(pdf_path)
            info = {
                'num_paginas': len(documento),
                'metadata': documento.metadata,
                'tamano_kb': Path(pdf_path).stat().st_size / 1024
            }
            documento.close()
            return info

        except Exception as e:
            logger.error(f"Error al obtener información del PDF: {e}")
            return {}
