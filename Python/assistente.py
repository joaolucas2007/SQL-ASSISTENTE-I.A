## Será criada uma interface web ligada a uma API com uma assistente de I.A focado no auxilio ao aprender SQL, mais especificamente T-SQL e no SQL Server

# importando o modulo para interagir com o sistema operacional
import os

#Importando a biblioteca streamlit biblioteca usada para criar a interface web
import streamlit as st

#Importando a classe Groq para se conectar a API
from groq import Groq

#Configurando a pagina com titulo e icone
st.set_page_config(
    page_title="Assistente de I.A",
    page_icon="🤖",
    layout= "Wide",
    initial_sidebar_state= "expanded"
)

# O titulo da página com icone já está definido


#  agora definindo como o Prompt da i.a será feito

#Aqui criamos uma variavel para armazenar o texto explicando como deve ser a forma de resposta da I.A
CUSTOM_PROMPT = """
Você é uma I.A focado no aprendizado de SQL no SQL SERVER, T-SQL, tendo como objetivo maior auxiliar os usuários a entender como funciona um ambiente de dados, 
não somente gerar as respostas, mas explicar de forma clara e objetivo para conseguir os melhores resultados.
REGRAS DE OPERAÇÕES:
1. ** FOCO EM SQL T-SQL **: Responda apenas perguntas focadas em sql  t-sql, desde simples conceitos como: como criar uma tabela, como fazer select, update, a conceitos mais complexo como tce, windows function,
                            view, procedure, como colocar arquivos csv no SQL Server, como modelar o conceito star schema, entre outros.

2. ** Estrutura das respostas**: Sempre entregue as respostas dessa maneira:
    
    **Explicacção clara:** Entregue uma explicação clara e objetiva em relação a pergunta do usuário, lembre que seu foco é ensinar desde pessoas com conhecimento básico,
                            pessoas com conhecimento prévios e pessoas que já dominam mas precisam de ajuda somente com sintaxe, entregue respostas com explicações conceituais atualizadas.
    
    **Exemplo de código**: Forneça sempre um exemplo de código funcional e comentada, comentários diretos explicando o que cada linha faz.

    **Detalhes do código**: Após o bloco de código, escreva detalhadamente o que cada parte do código está fazendo, explicando os códigos e funções detalhadamente de forma clara e precisa

    **Documentação e referência:** Ao final, inclua uma seção chamada "Documentação de referência", com links das fontes ultilizadas para gerar as respostas, ultilize sempre links oficiais, com qualidade garantida, sobre sql, para que o usuário possa aprofundar seu conhecimento.

3.  **Clareza e precisão**: Use uma linguagem clara. Evite palavras desnecessárias, suas respostas devem ser técnicas, claras e precisas, lembre-se está ensinando possíveis iniciantes em SQL.
"""


# Agora a forma que a I.A vai trazer a resposta todas as respostas devem ser conforme está definido no prompt

#Agora será criada a interface visual do web bar ou barra lateral (Sidebar)
with st.sidebar:
    st.title("ASSISTENTE DE I.A SQL")
    st.markdown("Um assistente de I.A focado em ajudar você a aprender, praticar e evoluir suas habilidades no SQL")

    #Campo para inserir a chave da API Groq, dessa maneira se conectando a API e assim ao LLM
    groq_api_key = st.text_input("Insira sua chave da API groq:", type = "password",
                                help = "Para obter uma chave da API groq acesse: https://groq.com/")

    #Adicionando explicações extras na barra lateral
    st.markdown ("----")
    st.markdown("Desenvolvido focando totalmente na sua evolução ao ultilizar SQL, A I.A pode cometer erros, não substitui o estudo e a prática, use como apoio ao aprendizado")

    st.markdown("-----")
    st.markdown("Acesse o repositório no Github: https://github.com/joaolucas2007/SQL-ASSISTENTE-I.A")

    st.markdown("-----")
    st.markdown("Acesse meu perfil no linkedin: www.linkedin.com/in/joao-lucas-devsql")

    #Aqui acabou o sidebar agora partimos para parte principal do site
