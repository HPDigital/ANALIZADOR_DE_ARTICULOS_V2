"""
ANALIZADOR_DE_ARTICULOS_V2
"""

#!/usr/bin/env python
# coding: utf-8

# In[2]:


from openai import OpenAI
import fitz  # PyMuPDF

client = OpenAI(api_key="YOUR_API_KEY_HERE")

def extraer_texto_pdf(ruta_pdf):
    # Abrir el documento PDF
    documento = fitz.open(ruta_pdf)

    # Recopilar el texto de cada página
    texto_completo = ""
    for pagina in documento:
        texto_completo += pagina.get_text()

    # Cerrar el documento
    documento.close()
    return texto_completo

def analyze_article(texto_completo, client):
    print("Iniciando el análisis del artículo científico.")

    steps = [
        ("resumen_articulo", "Elabora un resumen detallado del resunem del articulo"),
        ("base teorica", "¿Cuáles son las bases teorícas sobre las cuales se basa el artiuclo de investigación?"),
        ("Metodologia", "¿Cuál es la metodología con la que trabaja este articolo de investigación?"),
        ("Conceptos clave", " ¿Cuales son los conceptos clave que aborda el artículo?"),
        ("preliminary_reading", "Lectura preliminar para evaluar pertinencia."),
        ("detailed_analysis", "Análisis detallado de cada sección del artículo."),
        ("critical_evaluation", "Evaluación crítica de métodos y resultados."),
        ("information_synthesis", "Síntesis de información encontrada."),
        ("contextualize_in_existing_literature", "Contextualización en la literatura existente."),
        ("reflections_on_implications", "Reflexión sobre implicaciones y futuras direcciones."),
        ("write_review_manuscript", "Redacción del manuscrito de revisión."),
        ("review_and_editing", "Revisión y edición del manuscrito."),
        ("peer_feedback", "Feedback de colegas.")
    ]

    for step_function, description in steps:
        print(f"\n{description}")

        response = client.chat.completions.create(
            model="gpt-4o-2024-08-06", 
            messages=[{"role": "system", "content": description},
                      {"role": "user", "content": texto_completo}],
            max_tokens=1024
        )

        # Asegurarse de que la respuesta tenga una estructura 
        if hasattr(response, 'choices') and len(response.choices) > 0:
            # Accede directamente al atributo 'content' del mensaje
            message_content = response.choices[0].message.content.strip()
            print(message_content)
        else:
            print("Error: No se obtuvieron resultados de la respuesta.")


ruta_del_pdf = r"C:\Users\HP\Desktop\DIPLOMADO INVESTIGACION CIENTIFICA\MODULO 2\trabajo fin de modulo\ARTICULOS\Estudio de mercado del sector automotriz como herramienta para toma de decisiones empresariales.pdf"
texto_completo = extraer_texto_pdf(ruta_del_pdf)
analisis= analyze_article(texto_completo, client)
print(analisis)



# In[ ]:






if __name__ == "__main__":
    pass
