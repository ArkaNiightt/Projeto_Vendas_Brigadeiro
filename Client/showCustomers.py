import streamlit as st
from database.supabaseUtils import get_all_data
import pandas as pd
import datetime
import time


def showCustomers():
    if st.session_state['page'] == "listar_vendas":

        st.title("Lista de Clientes")
        st.markdown("Exibindo clientes extraídos da tabela 'vendas'.")

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
                "forma_de_pagamento"
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
                },
                key="dataframe_customers"
            )
            # Converte a coluna "data" para datetime e remove a informação de fuso horário
            df['data'] = pd.to_datetime(df['data']).dt.tz_localize(None)

            # Seleção de intervalo de datas
            start_date = st.date_input("Data de Início", df['data'].min().date())
            end_date = st.date_input("Data Final", df['data'].max().date())

            # Filtra os registros pelo intervalo selecionado
            filtered_df = df[(df['data'] >= pd.Timestamp(start_date)) & (df['data'] <= pd.Timestamp(end_date))]

            # Calcula os totais
            total_vendas = filtered_df.shape[0]  # número de vendas
            total_quantidade = filtered_df['quantidade'].sum()
            total_valor = filtered_df['valor'].sum()

            st.markdown("## Totais de Vendas")
            st.write("Total de vendas:", total_vendas)
            st.write("Quantidade total vendida:", total_quantidade)
            st.write("Valor total: R$ {:.2f}".format(total_valor))
        else:
            st.write("Nenhum cliente encontrado.")
        
