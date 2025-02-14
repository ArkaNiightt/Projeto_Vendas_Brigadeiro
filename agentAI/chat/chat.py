import streamlit as st
from agentAI.tool.agentPostgresqlExec import agents_executors_database
from database.supabaseUtils import get_all_data
import pandas as pd
from time import sleep


def dataframe_vendas():

    response = get_all_data()
    if not response.empty:
        # Cria o DataFrame a partir dos registros obtidos
        df = pd.DataFrame(response)

        # Reordena e seleciona as colunas desejadas, renomeando se necessário
        df = df[[
            "produto",
            "cliente",
            "valor",
            "quantidade",
            "data",
            "fiado",
            "forma_de_pagamento",
            "vendedor"
        ]]

        st.dataframe(
            df,
            use_container_width=True,
            column_config={
                "produto": st.column_config.TextColumn("Produto"),
                "cliente": st.column_config.TextColumn("Cliente"),
                "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                "quantidade": st.column_config.NumberColumn("Quantidade"),
                "data": st.column_config.DateColumn("Data"),
                "fiado": st.column_config.CheckboxColumn("Fiado", pinned=True),
                "forma_de_pagamento": st.column_config.TextColumn("Pagamento"),
                "vendedor": st.column_config.TextColumn("Vendedor")
            },
            key="dataframe_customers_chat"
        )


def chat_agent_response():
    if st.session_state['page'] == "chat":
        try:
            st.header("Chat com Agente de IA", help="", divider=True)
            st.write(
                "Este é um chat com um agente de IA que pode responder perguntas com base em um conjunto de dados.")

            pergunta = st.text_input(
                label="Digite sua pergunta aqui:",
                key="pergunta_agent",
                help="Digite uma pergunta para o agente de IA responder.",
                placeholder="Exemplo: Gostaria de saber quais são os clientes que compraram fiado e o valor total de suas compras.",
            )

            if pergunta:

                with st.spinner("Processando...", show_time=True):
                    response = agents_executors_database(question=pergunta)
                    st.write(response)
                    with st.spinner("Exibindo dados..."):
                        sleep(1)
                        dataframe_vendas()

        except KeyboardInterrupt:
            st.error("Finalizado pelo usuário.", icon="⚠️")
            st.stop()
            exit()
            return
        except Exception as e:
            st.error(f"Erro ao processar a pergunta: {e}", icon="❌")
            return
