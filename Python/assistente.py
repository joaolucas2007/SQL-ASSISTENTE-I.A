#Importando o modulo para interagir com sistema operacional
import os 
# Importando a biblioteca Streamlit para criar a interface web
import streamlit as st

# Importando a classe Groq para conectar à API
from groq import Groq


# Configurando a página
st.set_page_config(
    page_title="SQL Mentor",
    layout="wide",
    initial_sidebar_state="expanded"
)


#EDITANDO A APARÊNCIA DO SITE  Com STYLE abrimos uma área css no código
st.markdown ( """
            <style>
    /* Cor de fundo da página */
    .stApp {
        background-color: #0f172a;
        color: #e2e8f0;
    }

    /* Aparência da barra lateral */
    [data-testid="stSidebar"] {
        background-color: #111827;
        border-right: 1px solid #334155;
    }

    /* Título principal */
    h1 {
        color: #f8fafc;
        font-weight: 800;
    }
        </style>
""", unsafe_allow_html=True)

# Definindo o prompt da Inteligência Artificial
CUSTOM_PROMPT = """
Você é uma I.A focado no aprendizado de SQL no SQL SERVER, T-SQL, tendo como objetivo maior auxiliar os usuários a entender como funciona um ambiente de dados, 
não somente gerar as respostas, mas explicar de forma clara e objetivo para conseguir os melhores resultados.
REGRAS DE OPERAÇÕES:

1. ** FOCO EM SQL T-SQL **:
Responda apenas perguntas focadas em sql  t-sql, desde simples conceitos como: como criar uma tabela, como fazer select, update, a conceitos mais complexo como tce, windows function,
view, procedure, como colocar arquivos csv no SQL Server, como modelar o conceito star schema, entre outros.

2. ** Estrutura das respostas**: Sempre entregue as respostas dessa maneira:

    **Explicacção clara:** Entregue uma explicação clara e objetiva em relação a pergunta do usuário, 
     lembre que seu foco é ensinar desde pessoas com conhecimento básico,
     pessoas com conhecimento prévios e pessoas que já dominam mas precisam 
     de ajuda somente com sintaxe, entregue respostas com explicações conceituais atualizadas.
    
    **Exemplo de código**: Forneça sempre um exemplo de código funcional e comentada, comentários diretos explicando o que cada linha faz.

    **Detalhes do código**: Após o bloco de código, escreva detalhadamente o que cada parte do código está fazendo, 
    explicando os códigos e funções detalhadamente de forma clara e precisa

    **Documentação e referência:** Ao final, inclua uma seção chamada "Documentação de referência", 
    com links das fontes ultilizadas para gerar as respostas, ultilize sempre links oficiais, 
    com qualidade garantida, sobre sql, para que o usuário possa aprofundar seu conhecimento.

3.  **Clareza e precisão**: Use uma linguagem clara. Evite palavras desnecessárias, suas respostas devem ser técnicas, 
    claras e precisas, lembre-se está ensinando possíveis iniciantes em SQL.
"""
# Ai I.A sempre entrega as respostas como está escrito nesse prompt, esse prompt formata como deve ser toda resposta dela

# Criando a barra lateral
with st.sidebar:
    st.markdown("""                                             
<div style="display:flex; align-items:center; gap:10px;">
    <svg width="30" height="30" viewBox="0 0 24 24"
         fill="none" stroke="#60a5fa" stroke-width="1.8"
         stroke-linecap="round" stroke-linejoin="round">                          
        <ellipse cx="12" cy="5" rx="8" ry="3"/>
        <path d="M4 5v14c0 1.7 3.6 3 8 3s8-1.3 8-3V5"/>
        <path d="M4 12c0 1.7 3.6 3 8 3s8-1.3 8-3"/>
    </svg>
    <span style="font-size:24px; font-weight:700; color:#f8fafc;">
        SQL Mentor
    </span>
</div>
""", unsafe_allow_html=True)                        #Titulo do sidebar e icone de banco de dados

    st.markdown(
        "Um assistente de I.A focado em ajudar você a aprender"
        "praticar e evoluir suas habilidades em SQL."
    )

    st.caption("Conexão com a inteligência artificial ativa.")

    st.markdown(
            "O que você pode aprender?. "
        )
    st.markdown("---")                              # adiciona um espaço entre as frases

    st.markdown("Banco de dados")
    
    st.caption("Tabelas,modelagens e relacionamentos.")

    st.markdown("---")

    st.markdown( "Consultas SQL")

    st.caption("Select, joins, CTE etc.")

    st.markdown("---")

    st.markdown( "Aprendizado guiado")
    
    st.caption("Entenda a lógica por trás do código.")


    



    # Link para o GitHub
    st.markdown("""
    <a href="https://github.com/joaolucas2007/SQL-ASSISTENTE-I.A"
       target="_blank"
       style="color: #cbd5e1; text-decoration: none; font-size: 15px;">
        &nbsp; Meu GitHub ↗
    </a>
    """, unsafe_allow_html=True) # Permite fazer alterações como se fosse html

    st.markdown("<br>", unsafe_allow_html=True)

    # Link para o LinkedIn
    st.markdown("""
    <a href="https://www.linkedin.com/in/joao-lucas-devsql"
       target="_blank"
       style="color: #cbd5e1; text-decoration: none; font-size: 15px;">
        &nbsp; Meu LinkedIn ↗
    </a>
    """, unsafe_allow_html=True)


# Área principal da aplicação
st.title("Assistente de I.A - Aprendizado em SQL")  # Titulo para área principal 

st.caption("Digite sua pergunta ou dúvida sobre SQL Server e T-SQL.")


# Inicializando o histórico da conversa
if "messages" not in st.session_state:
    st.session_state.messages = []                  # Criando uma lista para receber as mensagens do cliente e as respostad da I.A


# Exibindo o histórico de perguntas e respostas
for message in st.session_state.messages:
    with st.chat_message(message["role"]):  # Cria um ambiente visual para como uma conversa entre usuário e a I.A
        st.markdown(message["content"]) # Exibindo o conteúdo da mensagem na interface


# # Inicializando o cliente Groq com a chave protegida
try:
    groq_api_key = st.secrets["GROQ_API_KEY"]               # Chama a chave da API configurada no streamlit s.secrets acessa as configurações do streamlit
    client = Groq(api_key=groq_api_key)     # Cria o cliente Groq a partir da chave da API

except KeyError:
    st.error(
        "A chave da API não foi configurada. "              #Caso a chave da API perder a funcionalidade 
        "Será nescessário verificar o Streamlit."
    )
    st.stop()

except Exception:
    st.error("Não foi possível inicializar a conexão com a IA.")   #Erro axebido na tela
    st.stop()

# Campo de entrada para as perguntas
if prompt := st.chat_input("Qual sua dúvida sobre SQL?"):

    # Armazenando a pergunta do usuário no histórico
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Exibindo a pergunta do usuário
    with st.chat_message("user"):
        st.markdown(prompt)

    # Preparando as mensagens para enviar à API
    messages_for_api = [
        {
            "role": "system",
            "content": CUSTOM_PROMPT   #Define as regras para a resposta da I.A
        }
    ]

    # Adicionando o histórico da conversa
    for msg in st.session_state.messages:
        messages_for_api.append(msg)

    # Gerando e exibindo a resposta da IA
    with st.chat_message("assistant"):
        with st.spinner("Analisando sua pergunta..."):      #Mensagem mostrada na tela enquanto o usuário espera a resposta
            try:
                chat_completion = client.chat.completions.create(   # Envia as perguntas do usuário e espera uma resposta
                    messages=messages_for_api,      # é a instruções para I.A e histórico de perguntas e respostas
                    model="openai/gpt-oss-120b",    #Modelo de I.A ultilziado no sistema
                    temperature=0.7,  #Controla a variedade de possiveis respostas
                    max_tokens=2048,    #Define a quantidade máxima de tokens, ou respostas
                )

                # Extraindo o conteúdo da resposta
                ia_resposta = (
                    chat_completion.choices[0].message.content
                )

                # Exibindo a resposta na interface
                st.markdown(ia_resposta)

                # Salvando a resposta no histórico
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": ia_resposta
                })

            except Exception as e:
                st.error(
                    f"Ocorreu um erro ao se comunicar com a API da Groq: {e}"   # Caso ocorra um erro com API mostra essa mensagem ao usuário
                )

#Criando rodapé 
st.markdown(
    """
    <style>
    .footer-autor {
        position: fixed;
        bottom: 0;
        left: 0;
        width: 100%;
        text-align: center;
        background-color: #0f172a;
        color: #cbd5e1;
        padding: 8px 10px;
        font-size: 13px;
        border-top: 1px solid #334155;
        z-index: 999;
    }

    /* Reserva espaço para o rodapé */
    .stMainBlockContainer {
        padding-bottom: 55px;
    }
    </style>

    <div class="footer-autor">
        SQL Mentor | Desenvolvido por João Lucas Freire da Silva
    </div>
    """,
    unsafe_allow_html=True
)