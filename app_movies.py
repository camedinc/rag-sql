#------------------------------------------------------------------------------
# ------------------------------- RAG SQL -------------------------------------
# La aplicación permite realizar preguntas en lenguage natural sobre una base de
# datos con información de películas que se han filmado entre 1960 y 2024. 
# Utiliza el modelo LLM en la transformación de la pregunta del usuario a una
# query SQL y luego para contruir una respuesta en lenguaje natural al usuario
# a partir de un prompt que combina la pregunta inicial, la consulta SQL y un
# resumen de la conversación como contexto siguiendo el principio 
# # RAG (Retrieval-Augmented Generation (Generación Aumentada por Recuperación).
#------------------------------------------------------------------------------

"""
# Instrucciones de ejecución
#------------------------------------------------------------------------------
BASH: cd ~/ruta/rag sql
BASH: streamlit run app_movies.py
Ctrl + C
"""

# Librerías
#------------------------------------------------------------------------------

from utils import data_base, query_entrada, respuesta_llm, memory_chat
import streamlit as st
from dotenv import load_dotenv
from dotenv import dotenv_values # Verificar el contenido del archivo .env
from langchain_openai import ChatOpenAI
import os
import duckdb

# Crear una instancia del modelo GPT-3.5
#------------------------------------------------------------------------------
    
# Cargar la variable desde el archivo .env
load_dotenv()

# Verificar la carga de la clave
api_key = os.getenv("OPENAI_API_KEY")

if api_key is None:
    raise ValueError("OPENAI_API_KEY no se encuentra configurada. Revisa el archivo .env.")

llm = ChatOpenAI(
        model = "gpt-3.5-turbo",  # Especifica el modelo
        temperature = 0.7,        # Ajusta el nivel de creatividad (rango 0-2)
        max_tokens = 250,         # Número máximo de tokens en la respuesta
        verbose = False,           # Muestra los detalles del proceso
        openai_api_key = api_key  # Api Key
    )

# Capa usuario
#------------------------------------------------------------------------------

# Inicializar memoria en session_state
memory_chat(llm)

# Carga el pdf
st.header("Base de películas IMDB")

# Mostrar historial acumulado
if "memory" in st.session_state:
    historial = st.session_state.memory.load_memory_variables({})["history"]
    if historial:
        st.write("### Historial de Conversación:")
        st.info(historial)

# Almacena la pregunta del usuario
pregunta_usuario = st.text_input("Has una pregunta:")

# Ejecución
#------------------------------------------------------------------------------

# Condición que evita el blanco en pregunta usuario
if pregunta_usuario:
    data_path = "data_clean/merged_movies_data.csv"
    db_path = "data_clean/movies.db"
    db_name = "movies"

    columnas, con = data_base(data_path, db_path, db_name)
    query = query_entrada(pregunta_usuario, columnas, llm)

    if query:
        resultado = con.execute(query).fetchall()
        respuesta = respuesta_llm(pregunta_usuario, resultado, llm)

        # Guardar la conversación en memoria
        st.session_state.memory.save_context({"input": pregunta_usuario}, {"output": respuesta})

        st.write("### Respuesta:")
        st.write(respuesta)
    else:
        st.warning("No se puede generar una consulta SQL válida.")