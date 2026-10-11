## Será criada uma interface web ligada a uma API com uma assistente de I.A focado no auxilio ao aprender SQL, mais especificamente T-SQL e no SQL Server

# importando o modulo para interagir com o sistema operacional
import os

#Importando a biblioteca streamlit biblioteca usada para criar a interface web
import streamlit as st

#Importando a classe Groq para se conectar a API
from groq import Groq

#Configurando a pagina com titulo e icno
st.set_page_config(
    page_title="Assistente de I.A",
    page_icon="🤖",
    layout= "Wide",
    initial_sidebar_state= "expanded"
)

# O titulo da página com icone já está definido


#  agora definindo como o Prompt da i.a será feito



