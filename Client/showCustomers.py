import streamlit as st
from supabaseUtils import inicializar_supabase
import pandas as pd


def showCustomers():
    st.title("Lista de Clientes")
    st.markdown("Exibindo clientes extraídos da tabela 'vendas'.")

    supabase = inicializar_supabase()
    response = supabase.table("vendas").select("cliente").execute()

    if response.data:
        # Extrai clientes únicos da tabela "vendas"
        clientes = list({registro["cliente"] for registro in response.data})
        df = pd.DataFrame(clientes, columns=["Cliente"])

        # Customização do estilo do DataFrame
        styled_df = df.style.set_properties(
            **{
                "background-color": "#f5f5f5",
                "color": "#333",
                "text-align": "center",
                "font-size": "14px"
            }
        ).set_table_styles(
            [
                {
                    "selector": "th",
                    "props": [
                        ("background-color", "#4CAF50"),
                        ("color", "white"),
                        ("font-size", "16px"),
                        ("padding", "8px")
                    ],
                }
            ]
        )

        st.dataframe(styled_df, use_container_width=True)
    else:
        st.write("Nenhum cliente encontrado.")
