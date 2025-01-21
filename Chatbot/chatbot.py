import streamlit as st
import plotly.express as px
import pandas as pd
import os

from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from graficas import Graficador

from config import KEY

# Cargamos los datos
directory = os.path.join(os.getcwd(), 'data')
file_path = os.path.join(directory, 'train_data.csv')

data = pd.read_csv(file_path)

# Creamos una instancia de la clase Graficador
graficador = Graficador(data)


# Configuración de la clave de OpenAI
openai_api_key = KEY


# Configuración del modelo ChatOpenAI
llm = ChatOpenAI(model="gpt-4", temperature=0, openai_api_key=openai_api_key)
general_llm = ChatOpenAI(model="gpt-4", temperature=0.7, openai_api_key=openai_api_key)


# Configuración del prompt
prompt = PromptTemplate(
    input_variables=["consulta"],
    template="""
    Eres un asistente de análisis de datos. Los datos tienen las siguientes columnas:
    'Duración_Estancia', 'Género', 'Edad', 'Niños', 'Destino', 'Alojamiento'

    Tu tarea es interpretar las solicitudes del usuario y devolver las variables necesarias para crear gráficos basados en las solicitudes, incluyendo:
    - Gráficos barras 
    - Gráficos de barras apiladas
    - Gráficos de violín
    - Gráficos de dispersión
    
    Devuelve las variables de la siguiente manera:
    Gráfico: tipo de gráfico, por ejemplo, "barras", "violin", "barras apiladas", "dispersión"
    X: nombre de la columna para el eje X
    Y: nombre de la columna para el eje Y, si aplica
    Color: si aplica.

    Si solo te den dan dos columnas siempre son x y y , nunca es una sola columna y color

    En dado caso que no aplique alguna variable, dejala en blanco.

    Reglas:
    1. Si la solicitud es para un gráfico específico (por ejemplo, "gráfico de dispersión entre duración y edad"), selecciona las columnas que correspondan al gráfico solicitado.
    2. Si la solicitud no es clara, indica que no entendiste.

    Responde siempre interpretando correctamente la solicitud y ajustando las variables al tipo de gráfico requerido.

    Solicitud del usuario: {consulta}
    """
)
chain = LLMChain(llm=llm, prompt=prompt)

st.title("Chatbot con LangChain para Análisis de Datos")

# historial de mensajes
if "messages" not in st.session_state:
    st.session_state.messages = []

# Mostrar mensajes del historial
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])


if prompt := st.chat_input("Escribe tu mensaje aquí..."):
    
    st.session_state.messages.append({"role": "user", "content": prompt})
    
    
    with st.chat_message("user"):
        st.markdown(prompt)

    
    with st.chat_message("assistant"):
        response_placeholder = st.empty()

        keywords = ["gráfico", "análisis", "gráfica", "grafica", "grafico"]

        if any(keyword in prompt.lower() for keyword in keywords):
            
            response_text = chain.run({"consulta": prompt})
         

            if "Gráfico" in response_text:
                
                variables = {}
                for linea in response_text.split("\n"):
                    if ":" in linea:
                        clave, valor = linea.split(":")
                        variables[clave.strip()] = valor.strip()
                
                # Mostrar las variables interpretadas
                #st.write("Variables interpretadas:")
                #for clave, valor in variables.items():
                    #st.write(f"{clave}: {valor}")

                
                grafico = variables.get("Gráfico", "").lower()
                x = variables.get("X", None)
                y = variables.get("Y", None)
                color = variables.get("Color", None)

                #st.write(grafico, x, y, color)
                st.write("Diccionario interpretado:", variables)


                if grafico == "dispersión" and x and y and color:
                    # Generar gráfico de dispersión
                    fig = graficador.generar_grafica_dispersion_bivariado(x, y, color)
                    response_placeholder.markdown(f"Aquí tienes el gráfico de dispersión: {x} vs {y} por {color}.")
                    st.plotly_chart(fig)

                elif grafico == "violín" and x and y:
                    # Generar gráfico de violín
                    fig = graficador.generar_grafico_violin_bivariado(x, y)
                    response_placeholder.markdown(f"Aquí tienes el gráfico de violín: {y} por {x}.")
                    st.plotly_chart(fig)

                elif grafico == "barras apiladas" and x and y:
                    # Generar gráfico de barras apiladas
                    fig = graficador.generar_grafico_barras_apiladas_bivariado(x, y)
                    response_placeholder.markdown(f"Aquí tienes el gráfico de barras apiladas para {x} por {y}.")
                    st.plotly_chart(fig)

                elif grafico == "barras" and x:
                    # Generar gráfico de barras univariado
                    fig = graficador.generar_grafica_barras_univariado(x)
                    response_placeholder.markdown(f"Aquí tienes el gráfico de barras para {x}.")
                    st.plotly_chart(fig)
                else:
                    response_placeholder.markdown("No pude generar el gráfico porque faltan columnas o no entendí tu solicitud.")
            else:
                response_placeholder.markdown("No entendí tu solicitud. Por favor, pide un gráfico válido.")

        else:
            general_response = general_llm.predict(f"Usuario: {prompt}")
            response_placeholder.markdown(general_response)