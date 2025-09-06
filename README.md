# Generación de informes arbitrales con IA

Este proyecto consiste en mi ***Trabajo Final de Máster**. En él, he aplicado Inteligencia Artificial Generativa para ayudar a un grupo específico de personas a realizar tareas de revisión de arbitraje en el fútbol utilizando informes directamente obtenidos de la Real Federación Española de Fútbol.

# ¿Qué hace este proyecto?

- Lee informes arbitrales **oficiales** dados en formato PDF o TXT.
- Procesa el informe y entiende la información mediante NLP y un LLM (Gemma3:12b)
- Transmite la información a un LLM (Gemma3:12b)
- Genera resúmenes de manera automática, personalizándolos para cada posible rol:
    - Árbitro principal
    - Asistentes
    - Cuarto árbitro
- He creado una interfaz web con Flask para subir los informes y recibir un resumen inmediato
Así pasamos de un documento extenso y tedioso como los PDF, o críptico y difícil de leer como los TXT, a un resumen automático que nos transmite los puntos importantes del rol analizado.

# ¿Qué ventajas presenta?

Como el arbitraje es una parte crítica en el deporte, y más aún en uno como el fútbol, es imprescindible que la evaluación del rendimiento de los que lo ejercen sea lo más objetiva, eficaz y clara posible.
Con este proyecto:
- Se ahorra tiempo de revisión de los informes
- Se estandarizan los criterios de ambos formatos
- Se facilita el análisis para los revisores y una presentación resumida para la federación

# Tecnologías clave utilizadas

- Python 3.12.9
- Flask para la interfaz web
- Ollama + Gemma3:12b para la generación de texto
- PdfPlumber para el procesamiento de los informes PDF
- Prompts diseñados a medida para cada rol arbitral

# Funcionamiento

![Procesamiento](https://github.com/user-attachments/assets/7ae17f5e-5825-4d38-acce-fb2bc1306cf0)
Esquema de procesamiento de los informes

![Web](https://github.com/user-attachments/assets/8e5e53c8-743a-49cd-beb0-4f88f4824633)
Interfaz web que muestra cómo se procesa un informe

# Objetivos prácticos

Con este proyecto, pretendía demostrar mi capacidad para diseñar y desplegar un sistema E2E con IA, integrando un procesamiento de NLP junto a un LLM moderno. Además, se añadió una aplicación web con una aplicabilidad práctica para satisfacer las necesidades específicas de unos usuarios focalizados en el ambiente deportivo.
