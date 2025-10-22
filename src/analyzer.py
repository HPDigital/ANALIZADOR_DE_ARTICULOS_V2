"""
Módulo principal de análisis de artículos científicos con OpenAI.
"""

from openai import OpenAI
from typing import Dict, List, Tuple, Callable, Optional
import logging
from dataclasses import dataclass

logger = logging.getLogger(__name__)


@dataclass
class AnalysisStep:
    """Representa un paso del análisis."""
    name: str
    description: str
    prompt: str


class ArticleAnalyzer:
    """Analizador de artículos científicos usando OpenAI GPT."""

    # Pasos de análisis predefinidos
    ANALYSIS_STEPS = [
        AnalysisStep(
            name="resumen_articulo",
            description="Resumen del Artículo",
            prompt="Elabora un resumen detallado del artículo científico, destacando los puntos más importantes."
        ),
        AnalysisStep(
            name="base_teorica",
            description="Bases Teóricas",
            prompt="¿Cuáles son las bases teóricas sobre las cuales se fundamenta el artículo de investigación?"
        ),
        AnalysisStep(
            name="metodologia",
            description="Metodología",
            prompt="¿Cuál es la metodología con la que trabaja este artículo de investigación? Describe detalladamente los métodos utilizados."
        ),
        AnalysisStep(
            name="conceptos_clave",
            description="Conceptos Clave",
            prompt="¿Cuáles son los conceptos clave que aborda el artículo? Enumera y explica brevemente cada uno."
        ),
        AnalysisStep(
            name="objetivos",
            description="Objetivos de Investigación",
            prompt="¿Cuáles son los objetivos principales de la investigación presentada en el artículo?"
        ),
        AnalysisStep(
            name="resultados",
            description="Resultados Principales",
            prompt="¿Cuáles son los principales resultados y hallazgos presentados en el artículo?"
        ),
        AnalysisStep(
            name="evaluacion_critica",
            description="Evaluación Crítica",
            prompt="Realiza una evaluación crítica de los métodos y resultados presentados. ¿Cuáles son las fortalezas y debilidades?"
        ),
        AnalysisStep(
            name="contexto_literatura",
            description="Contextualización en la Literatura",
            prompt="¿Cómo se contextualiza este artículo dentro de la literatura científica existente? ¿Qué aportes novedosos presenta?"
        ),
        AnalysisStep(
            name="implicaciones",
            description="Implicaciones y Futuras Direcciones",
            prompt="¿Cuáles son las implicaciones de estos hallazgos y qué futuras líneas de investigación sugiere el artículo?"
        ),
        AnalysisStep(
            name="conclusiones",
            description="Conclusiones",
            prompt="Resume las conclusiones principales del artículo y su relevancia científica."
        )
    ]

    def __init__(self, api_key: str, model: str = "gpt-4o-2024-08-06", max_tokens: int = 1024):
        """
        Inicializa el analizador.

        Args:
            api_key (str): API key de OpenAI.
            model (str): Modelo de OpenAI a utilizar.
            max_tokens (int): Máximo de tokens por respuesta.
        """
        self.client = OpenAI(api_key=api_key)
        self.model = model
        self.max_tokens = max_tokens
        logger.info(f"ArticleAnalyzer inicializado con modelo: {model}")

    def analyze_article(
        self,
        texto_completo: str,
        progress_callback: Optional[Callable[[str, str, int, int], None]] = None
    ) -> Dict[str, str]:
        """
        Analiza un artículo científico siguiendo múltiples pasos.

        Args:
            texto_completo (str): Texto del artículo a analizar.
            progress_callback (Optional[Callable]): Función callback para reportar progreso.
                Recibe (step_name, step_description, current_step, total_steps).

        Returns:
            Dict[str, str]: Diccionario con los resultados de cada paso del análisis.
        """
        logger.info("Iniciando análisis del artículo científico")

        if not texto_completo or not texto_completo.strip():
            raise ValueError("El texto del artículo está vacío")

        resultados = {}
        total_steps = len(self.ANALYSIS_STEPS)

        for idx, step in enumerate(self.ANALYSIS_STEPS, start=1):
            logger.info(f"Paso {idx}/{total_steps}: {step.description}")

            # Llamar al callback de progreso si existe
            if progress_callback:
                progress_callback(step.name, step.description, idx, total_steps)

            try:
                # Realizar el análisis para este paso
                resultado = self._analyze_step(texto_completo, step)
                resultados[step.name] = resultado

                logger.debug(f"Completado: {step.name}")

            except Exception as e:
                logger.error(f"Error en paso {step.name}: {e}")
                resultados[step.name] = f"Error: {str(e)}"

        logger.info("Análisis completado")
        return resultados

    def _analyze_step(self, texto: str, step: AnalysisStep) -> str:
        """
        Ejecuta un paso individual del análisis.

        Args:
            texto (str): Texto del artículo.
            step (AnalysisStep): Paso de análisis a ejecutar.

        Returns:
            str: Resultado del análisis.
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": step.prompt},
                    {"role": "user", "content": texto}
                ],
                max_tokens=self.max_tokens
            )

            if response.choices and len(response.choices) > 0:
                return response.choices[0].message.content.strip()
            else:
                return "Error: No se obtuvo respuesta del modelo"

        except Exception as e:
            logger.error(f"Error en llamada a OpenAI: {e}")
            raise

    def analyze_custom_step(
        self,
        texto: str,
        prompt: str,
        description: str = "Análisis personalizado"
    ) -> str:
        """
        Realiza un análisis personalizado con un prompt específico.

        Args:
            texto (str): Texto a analizar.
            prompt (str): Prompt personalizado.
            description (str): Descripción del análisis.

        Returns:
            str: Resultado del análisis.
        """
        step = AnalysisStep(name="custom", description=description, prompt=prompt)
        return self._analyze_step(texto, step)

    def get_analysis_steps_info(self) -> List[Dict[str, str]]:
        """
        Obtiene información sobre los pasos de análisis disponibles.

        Returns:
            List[Dict[str, str]]: Lista de información de cada paso.
        """
        return [
            {
                "name": step.name,
                "description": step.description,
                "prompt": step.prompt
            }
            for step in self.ANALYSIS_STEPS
        ]
