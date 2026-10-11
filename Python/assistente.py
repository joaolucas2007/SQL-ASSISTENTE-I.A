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
    layout= "wide",
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

st.title("Assistente de I.A - Aprendizado em SQL")

#Adicionando um texto auxiliar
st.caption("Digite sua pergunta ou dúvida para a I.A")

#Criando e iniciando o histórico de perguntas e respostas
if "messages" not in st.session_state: #armazena dados da sessão do usuário
   st.session_state.messages = [] #Criando uma lista vazia para armazenar mensagens

    #Mostrando o histórico de perguntas e respostas
for message in st.session_state.messages: # For percorre a lista criada anteriormente
       with st.chat_message(message["role"]): #Cria visualmente uma mensagem no chat, acessa o valor do role que está no for,
                                            #se for user será exibida como mensagem du usuário, se for assistant será exibida como mensagem do assistente          
    
        st.markdown(message["content"]) #Cria a mensagem na tela

    # Assim criamos um histórico de perguntas e respostas


    #Criando a variavel Client
client = None #None significa vazio, não tem cliente ainda conectado

    #Criando um if para garantir que a chave API foi inserida corretamente

if groq_api_key:
        try: # Criando o cliente groq com a chave API fornecida
            client = Groq(api_key = groq_api_key)


        except Exception as e:
            #Exibindo erro caso não tenha uma chave da API registrada, ou seja invalida
            st.sidebar.error(f"erro ao inicializar o cliete Groq: {e}")
            st.stop() # para a execução do código

    #Caso não tenha chave, mas já existam mensagens, mostra o aviso
elif st.session_state.messages:
        st.warning("Por favor, insira sua chave da API Groq para continuar a conversa.")


        #Caixa de texto do chat na parte principal da página
# Caixa de texto do chat na parte principal da página
if prompt := st.chat_input("Qual sua dúvida sobre SQL?"):

        # Se não houver cliente válido, mostra o aviso na tela e para
        if not client:
            st.warning("Por favor, insira sua chave da API Groq na barra lateral para continuar.")
            st.stop()

        # Armazena a mensagem do usuário no estado da sessão
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Exibindo a mensagem do usuário no chat
        with st.chat_message("user"):
            st.markdown(prompt)

        # PREPARANDO A VARIÁVEL AQUI (Logo após a mensagem do usuário)
        messages_for_api = [{"role": "system", "content": CUSTOM_PROMPT}]
        for msg in st.session_state.messages:
            messages_for_api.append(msg)

        # Criando a resposta do assistente no chat
        with st.chat_message("assistant"):
            with st.spinner("analisando sua pergunta..."):
                try:
                    chat_completion = client.chat.completions.create(
                        messages=messages_for_api,  # Agora ela existe e será lida corretamente aqui!
                        model="openai/gpt-oss-230b",
                        temperature=0.7,
                        max_tokens=2048,
                    )

                    ia_resposta = chat_completion.choices[0].message.content
                    st.markdown(ia_resposta)

                    st.session_state.messages.append({"role": "assistant", "content": ia_resposta})

                except Exception as e:
                    st.error(f"Ocorreu um erro ao se comunicar com API da Groq: {e}")


    # Criando a resposta do assistente no chat
# Criando a resposta do assistente no chat
# Criando a resposta do assistente no chat
with st.chat_message("assistant"):
        with st.spinner("analisando sua pergunta..."):
            try:
                # Verifica se a chave foi inserida antes de chamar a API
                if not client:
                    st.warning("Por favor, insira sua chave da API Groq na barra lateral.")
                    st.stop()

                chat_completion = client.chat.completions.create(
                    messages=messages_for_api,
                    model="openai/gpt-oss-120b",
                    temperature=0.7,
                    max_tokens=2048,
                )

                # Extrai a resposta gerada pela I.A
                ia_resposta = chat_completion.choices[0].message.content

                # Mostrando a resposta na tela
                st.markdown(ia_resposta)

                # Armazena a resposta do assistente no estado da sessão
                st.session_state.messages.append({"role": "assistant", "content": ia_resposta})

            except Exception as e:
                st.error(f"Ocorreu um erro ao se comunicar com API da Groq: {e}")

st.markdown("""
            <div style="position: fixed; bottom: 0; width: 100%; text-align: center; background-color: #f1f1f1; padding: 10px;">
                <p style="margin: 0;">Desenvolvido por João Lucas - 2024</p>
            </div>
            """, unsafe_allow_html=True
    )