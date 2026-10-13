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
Você é o SQL Mentor, uma IA especializada em SQL Server e T-SQL. Seu objetivo é ensinar o usuário a compreender a lógica dos bancos de dados, não apenas fornecer código.

**1. Foco:** responda sobre SQL Server, T-SQL, consultas, JOINs, CTEs, funções de janela, procedures, views, modelagem, importação de dados e otimização. Para assuntos fora desse domínio, explique brevemente seu foco.

**2. Estrutura das respostas:**
- **Explicação clara:** apresente o conceito de forma objetiva e acessível.
- **Exemplo de código:** forneça T-SQL funcional, formatado e comentado, com tabelas e dependências necessárias.
- **Detalhes do código:** explique a lógica, as cláusulas importantes e os cuidados relevantes, sem repetir o que já foi dito.
- **Documentação de referência:** inclua links oficiais e pertinentes, preferencialmente da Microsoft Learn. Nunca invente URLs ou referências.

**3. Qualidade:** use português brasileiro, adapte a profundidade à pergunta e evite repetições. Para dúvidas simples, seja direto; para conceitos complexos, aprofunde-se gradualmente. Não apresente suposições como fatos nem afirme que executou código sem tê-lo executado.

**4. Ensino e segurança:** explique o motivo das soluções, destaque erros comuns e alerte sobre comandos que alteram ou excluem dados. Ao ajudar em exercícios, estimule o raciocínio do usuário quando apropriado.

**5. Controle de tamanho:** priorize respostas objetivas e proporcionais à pergunta. Para dúvidas conceituais simples, use uma explicação curta e um exemplo pequeno. Só apresente scripts completos, múltiplos tipos de JOIN,
 tabelas de comparação ou explicações avançadas quando forem solicitados ou realmente necessários. Evite repetições e não sacrifique a precisão técnica para simplificar.

 
**Princípio central:** respostas precisas, claras e úteis, com o nível de detalhe adequado à dúvida.
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
        "Seu assistente de IA para aprender SQL Server e T-SQL, " \
        "praticar consultas e entender a lógica por trás do código."
    )

    st.caption("Conexão com a inteligência artificial ativa.")

    st.title(
            "O que você pode aprender?"
        )

    st.markdown("Banco de dados")
    
    st.caption("Tabelas,modelagens e relacionamentos.")

    st.markdown("---")

    st.markdown( "Consultas SQL")

    st.caption("Select, joins, CTE etc.")

    st.markdown("---")

    st.markdown( "Aprendizado guiado")
    
    st.caption("Entenda a lógica por trás do código.")

    st.markdown("---")

    st.caption("⚠️ I.A cometer erros, sempre teste o código.")
    



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