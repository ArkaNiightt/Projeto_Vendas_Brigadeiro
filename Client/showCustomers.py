import streamlit as st
from database.supabaseUtils import get_all_data
import pandas as pd
from time import sleep


def showCustomers():
    if st.session_state['page'] == "listar_vendas":

        st.title("Lista de Clientes")
        st.markdown("Exibindo clientes extraídos da tabela 'vendas'.")
        with st.spinner("Processando...", show_time=True):
            sleep(1)

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
                    key="dataframe_customers"
                )
                # Converte a coluna "data" para datetime e remove a informação de fuso horário
                df['data'] = pd.to_datetime(df['data']).dt.tz_localize(None)

                # Seleção de intervalo de datas
                start_date = st.date_input(
                    "Data de Início", df['data'].min().date())
                end_date = st.date_input("Data Final", df['data'].max().date())

                # Filtra os registros pelo intervalo selecionado
                filtered_df = df[(df['data'] >= pd.Timestamp(start_date)) & (
                    df['data'] <= pd.Timestamp(end_date))]

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


def showCustomer():
    if st.session_state['page'] == "listar_vendas":
        st.title("Pesquisar Cliente")
        st.markdown("Digite o nome do cliente que deseja pesquisar.")

        # Get all data for searching
        response = get_all_data()
        if response.empty:
            st.error("Não foi possível carregar os dados dos clientes.")
            return

        # Create dataframe
        df = pd.DataFrame(response)

        # Get unique customer names for dropdown
        customers = sorted(df['cliente'].unique())
        customer_name = st.selectbox("Selecione o Cliente", options=customers)

        if st.button("Pesquisar"):
            with st.spinner("Buscando registros..."):
                # Filter records for the selected customer
                customer_df = df[df['cliente'] == customer_name]

                if not customer_df.empty:
                    # Convert date for display
                    customer_df['data'] = pd.to_datetime(
                        customer_df['data']).dt.tz_localize(None)

                    # Show customer records
                    st.success(
                        f"Encontrados {len(customer_df)} registros para {customer_name}")

                    st.dataframe(
                        customer_df,
                        use_container_width=True,
                        column_config={
                            "produto": st.column_config.TextColumn("Produto"),
                            "valor": st.column_config.NumberColumn("Valor", format="R$ %.2f"),
                            "quantidade": st.column_config.NumberColumn("Quantidade"),
                            "data": st.column_config.DateColumn("Data"),
                            "fiado": st.column_config.CheckboxColumn("Fiado"),
                            "forma_de_pagamento": st.column_config.TextColumn("Pagamento"),
                            "vendedor": st.column_config.TextColumn("Vendedor")
                        }
                    )

                    # Calculate statistics for this customer
                    total_purchases = len(customer_df)
                    total_items = customer_df['quantidade'].sum()
                    total_spent = customer_df['valor'].sum()
                    fiado_count = customer_df['fiado'].sum()

                    # Display statistics
                    st.markdown("## Resumo do Cliente")
                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total de Compras", total_purchases)
                    col2.metric("Quantidade Total", total_items)
                    col3.metric("Valor Total", f"R$ {total_spent:.2f}")

                    if fiado_count > 0:
                        fiado_total = customer_df[customer_df['fiado'] == True]['valor'].sum(
                        )
                        st.warning(
                            f"Cliente possui {fiado_count} compras fiadas, totalizando R$ {fiado_total:.2f}")
                else:
                    st.warning(
                        f"Nenhum registro encontrado para {customer_name}.")
