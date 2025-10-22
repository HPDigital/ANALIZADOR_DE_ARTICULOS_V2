# 📚 Analizador de Artículos Científicos V2

## Descripción

Aplicación de escritorio con interfaz gráfica (Tkinter) para analizar artículos científicos en formato PDF utilizando inteligencia artificial (OpenAI GPT-4). La herramienta realiza un análisis exhaustivo del artículo científico, extrayendo información clave como resumen, bases teóricas, metodología, resultados, evaluación crítica y más.

## Características

- ✅ Interfaz gráfica intuitiva y fácil de usar
- 📄 Extracción automática de texto desde archivos PDF
- 🤖 Análisis inteligente con OpenAI GPT-4
- 📊 Análisis multi-dimensional:
  - Resumen del artículo
  - Bases teóricas
  - Metodología de investigación
  - Conceptos clave
  - Objetivos de investigación
  - Resultados principales
  - Evaluación crítica
  - Contextualización en la literatura
  - Implicaciones y futuras direcciones
  - Conclusiones
- 💾 Exportación de resultados en formato texto
- 🔒 Gestión segura de credenciales API con variables de entorno
- 📈 Barra de progreso en tiempo real
- 🎨 Resultados organizados en pestañas para fácil navegación

## Requisitos

### Software

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Dependencias

Instalar todas las dependencias con:

```bash
pip install -r requirements.txt
```

Las dependencias incluyen:
- `openai>=1.0.0` - API de OpenAI
- `PyMuPDF>=1.23.0` - Procesamiento de archivos PDF
- `python-dotenv>=1.0.0` - Gestión de variables de entorno
- `colorlog>=6.7.0` - Logging mejorado (opcional)

## Configuración

### 1. Clonar o descargar el repositorio

```bash
git clone https://github.com/tu-usuario/ANALIZADOR_DE_ARTICULOS_V2.git
cd ANALIZADOR_DE_ARTICULOS_V2
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar API Key de OpenAI

Tienes dos opciones:

**Opción A: Archivo .env (recomendado)**

Edita el archivo `.env` incluido en el proyecto y agrega tu API key:

```env
OPENAI_API_KEY=tu-api-key-aqui
OPENAI_MODEL=gpt-4o-2024-08-06
MAX_TOKENS=1024
```

**Opción B: Ingresar manualmente en la interfaz**

Puedes ingresar tu API key directamente en la interfaz gráfica al ejecutar la aplicación.

**IMPORTANTE**:
- Nunca compartas tu API key
- Asegúrate de que `.env` esté en `.gitignore`
- Puedes obtener tu API key en: https://platform.openai.com/api-keys

## Uso

### Ejecutar la aplicación

```bash
python main.py
```

### Pasos para analizar un artículo

1. **Ingresar API Key** (si no está en `.env`)
   - Pega tu API key de OpenAI en el campo correspondiente
   - Usa el botón 👁️ para mostrar/ocultar la clave

2. **Seleccionar PDF**
   - Haz clic en "📁 Seleccionar PDF"
   - Elige el archivo PDF del artículo científico

3. **Iniciar análisis**
   - Haz clic en "🚀 Iniciar Análisis"
   - Espera mientras se procesa (puede tomar varios minutos)

4. **Ver resultados**
   - Los resultados aparecerán en pestañas organizadas
   - Navega entre las diferentes secciones del análisis

5. **Guardar resultados**
   - Haz clic en "💾 Guardar Resultados"
   - Elige la ubicación para guardar el archivo de texto

## Estructura del Proyecto

```
ANALIZADOR_DE_ARTICULOS_V2/
├── main.py                          # Punto de entrada de la aplicación
├── README.md                        # Este archivo
├── requirements.txt                 # Dependencias del proyecto
├── .env                            # Variables de entorno (configurar con tu API key)
├── .gitignore                      # Archivos ignorados por git
├── src/
│   ├── __init__.py
│   ├── analyzer.py                 # Lógica de análisis con OpenAI
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py            # Configuración centralizada
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── pdf_extractor.py       # Extracción de texto de PDF
│   │   └── logger.py              # Sistema de logging
│   └── gui/
│       ├── __init__.py
│       └── main_window.py         # Interfaz gráfica Tkinter
├── output/                         # Directorio para resultados (auto-creado)
└── temp/                          # Directorio temporal (auto-creado)
```

## Arquitectura

### Módulos principales

- **src/analyzer.py**: Contiene la clase `ArticleAnalyzer` que gestiona el análisis con OpenAI
- **src/utils/pdf_extractor.py**: Clase `PDFExtractor` para extraer texto de PDFs
- **src/config/settings.py**: Configuración centralizada de la aplicación
- **src/gui/main_window.py**: Interfaz gráfica completa con Tkinter

### Flujo de trabajo

1. Usuario selecciona PDF
2. `PDFExtractor` extrae el texto
3. `ArticleAnalyzer` procesa el texto en múltiples pasos
4. Cada paso envía una consulta específica a GPT-4
5. Resultados se muestran en la interfaz
6. Usuario puede exportar los resultados

## Tecnologías utilizadas

- **Python 3.8+**: Lenguaje principal
- **Tkinter**: Interfaz gráfica de usuario
- **OpenAI API**: Análisis inteligente con GPT-4
- **PyMuPDF (fitz)**: Extracción de texto de PDFs
- **python-dotenv**: Gestión de variables de entorno

## Solución de problemas

### Error: "OPENAI_API_KEY no está configurada"

- Verifica que hayas creado el archivo `.env` con tu API key
- O ingresa la API key manualmente en la interfaz

### Error: "El PDF no contiene texto extraíble"

- Algunos PDFs son solo imágenes escaneadas
- Necesitas un PDF con texto real, no imágenes de texto

### La aplicación se congela durante el análisis

- El análisis puede tardar varios minutos dependiendo del tamaño del artículo
- El proceso se ejecuta en segundo plano, pero la UI puede parecer congelada
- Verifica la barra de progreso para confirmar que está funcionando

### Errores de conexión con OpenAI

- Verifica tu conexión a internet
- Confirma que tu API key es válida
- Revisa que tengas créditos disponibles en tu cuenta de OpenAI

## Contribuir

Las contribuciones son bienvenidas. Por favor:

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## Autor

[Tu Nombre]
- GitHub: [@tu-usuario](https://github.com/tu-usuario)
- Email: tu-email@ejemplo.com

## Agradecimientos

- OpenAI por proporcionar la API de GPT-4
- PyMuPDF por la excelente biblioteca de procesamiento de PDFs
- La comunidad de Python por las herramientas y librerías

## Changelog

### Version 2.0.0 (2025-10-22)

- ✨ Refactorización completa del código
- ✨ Nueva interfaz gráfica con Tkinter
- ✨ Arquitectura modular mejorada
- ✨ Gestión segura de credenciales con .env
- ✨ Sistema de logging mejorado
- ✨ Análisis multi-paso más completo
- ✨ Exportación de resultados
- ✨ Barra de progreso en tiempo real
- 🐛 Corrección de errores tipográficos
- 🐛 Corrección de rutas hardcodeadas
- 📝 Documentación completa

### Version 1.0.0

- Versión inicial basada en Jupyter Notebook

## Notas importantes

- Este proyecto requiere una API key válida de OpenAI
- El uso de la API tiene costos asociados según los tokens consumidos
- Se recomienda revisar los precios en: https://openai.com/pricing
- El análisis de un artículo típico consume aproximadamente 10,000-20,000 tokens
- Mantén tu API key segura y nunca la compartas públicamente
- Los archivos `.env` están excluidos del control de versiones por seguridad
