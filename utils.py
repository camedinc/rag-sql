# Librerías
#----------------------------------------------------------------------

import streamlit as st
import duckdb
import os

from langchain.prompts import PromptTemplate
from langchain.memory import ConversationSummaryMemory
from langchain.chains import ConversationChain

# Crear la base de datos
#------------------------------------------------------------------------------

def data_base(data_path, db_path, db_name):
    # Si ya existe
    if os.path.exists(db_path):
        # Conectar a la base lectura
        con = duckdb.connect(database=db_path, read_only=True)
        print(f"La base de datos '{db_path}' ya existe.")
    else:
        # Conectar y guardar
        con = duckdb.connect(database=db_path)
        con.execute(f"CREATE TABLE movies AS SELECT * FROM read_csv_auto({data_path})")
        print(f"La base de datos '{db_path}' ha sido creada y actualizada con nuevos datos.")

    # Extrae las columnas de la base de datos
    columns = con.execute(f"DESCRIBE {db_name}").fetchall()

    # Convertir columnas a string
    columns_str = ", ".join([col[0] for col in columns])
    return columns_str, con

# Obtener la consulta SQL para la pregunta
#------------------------------------------------------------------------------

def query_entrada(pregunta, columnas, llm):

    prompt_template = PromptTemplate(
                input_variables=["pregunta", "columnas"],
                template=   "Convierte la siguiente pregunta en una consulta SQL que sea válida sobre la tabla 'movies'.\n"
                            "La tabla movies tiene las siguientes columnas: {columnas}.\n"
                            "La pregunta es: {pregunta}.\n"
        )

    consulta_sql_metadatos = llm.invoke(
                             prompt_template.format(pregunta=pregunta, columnas=columnas)
                            )
    
    # Extraer sólo el texto de la consulta, sin metadatos
    consulta_sql = consulta_sql_metadatos.content
    return consulta_sql

# Obtener la respuesta en lenguaje natural
#------------------------------------------------------------------------------
def respuesta_llm(pregunta, resultado, llm):

    memoria = memory_chat(llm).memory.load_memory_variables({})

    prompt_template = PromptTemplate(
                        input_variables=["pregunta", "resultado", "memoria"],
                        template=   "Considera la pregunta que hizo el usuario, el resultado y la memoria y con ellas genera una respuesta amigable.\n"
                                    "El usuario realizó la siguiente pregunta: {pregunta}.\n"
                                    "El resultado que se obtuvo para la pregunta del usuario fue: {resultado}.\n"
                                    "La memoria de conversación acumulada hasta ahora es: {memoria}."
                        )
    
    respuesta_usuario = llm.invoke(
                        prompt_template.format(pregunta=pregunta, resultado=resultado, memoria=memoria)
                        )
    # Extraer sólo el texto de la respuesta, sin metadatos
    respuesta_texto = respuesta_usuario.content 

    return respuesta_texto

# Generar memoria
#------------------------------------------------------------------------------
def memory_chat(llm):
    # Crear memoria de conversación
    if "memory" not in st.session_state:
        st.session_state.memory = ConversationSummaryMemory(llm=llm)

    # Crear cadena de conversación con memoria
    chatbot_resumen = ConversationChain(
        llm=llm, 
        memory=st.session_state.memory, 
        verbose=True
        )
    
    # Retorna la cadena de conversación
    return chatbot_resumen