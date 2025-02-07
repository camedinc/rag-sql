# RAG SQL - Consulta de Películas con Lenguaje Natural

Descripción

RAG SQL es una aplicación que permite realizar preguntas en lenguaje natural sobre una base de datos de películas filmadas entre 1960 y 2024 que se ha obtenido del sitio IMDB mediante técnicas de scraping. Utiliza un modelo LLM (Large Language Model) para transformar la consulta del usuario en una instrucción SQL válida y retornar respuestas en lenguaje natural basadas en los resultados obtenidos. Esto se logra mediante la técnica de Retrieval-Augmented Generation (RAG), que combina la recuperación de información con la generación de texto.

## Características principales

 - Conversión de preguntas en lenguaje natural a consultas SQL.

- Generación de respuestas en lenguaje natural utilizando los resultados obtenidos.

- Memoria de conversación para mejorar la coherencia en interacciones sucesivas.

- Implementación con Streamlit para una interfaz intuitiva y accesible.

## Instalación

Clona este repositorio:
```
git clone https://github.com/tu_usuario/rag_sql.git
cd rag_sql
```

## Crea un entorno virtual e instala las dependencias:
```
python -m venv env
source env/bin/activate  # En Windows usa: env\Scripts\activate
pip install -r requirements.txt
```
## Crea un archivo .env en la raíz del proyecto y define tu clave de API de OpenAI:
```
OPENAI_API_KEY=tu_clave_aqui
```
## Uso

Para ejecutar la aplicación, utiliza el siguiente comando en la terminal:

streamlit run app_movies.py

Luego, accede a la aplicación en tu navegador a través de la URL que Streamlit proporcione.

## Estructura del Proyecto

```
rag_sql/
├── data_clean/              # Archivos de datos y base de datos
├── app_movies.py            # Script principal de la aplicación
├── utils.py                 # Funciones
└── .env                     # Archivo de variables de entorno
```

## Tecnologías utilizadas

- Python (v3.8+)

- Streamlit (para la interfaz de usuario)

- DuckDB (para gestión de bases de datos)

- LangChain (para integración con modelos LLM)

- OpenAI GPT-3.5 Turbo (para generación de consultas SQL y respuestas en lenguaje natural)

