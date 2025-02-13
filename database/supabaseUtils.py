from supabase import create_client, Client
import streamlit as st
import pandas as pd

DATABASE = "vendas"


# Inicializar o cliente Supabase
@st.cache_resource
def inicializar_supabase():
    try:
        supabase_url = st.secrets["supabase"]["SUPABASE_URL"]
        supabase_key = st.secrets["supabase"]["SUPABASE_KEY"]
        supabase: Client = create_client(supabase_url, supabase_key)
        return supabase
    except KeyError:
        print("Credenciais do Supabase não encontradas. Verifique o arquivo secrets.toml.")
        st.stop()


def get_all_data():
    supabase = inicializar_supabase()
    try:
        response = supabase.table(DATABASE).select("*").execute()

        if response.data:
            df = pd.DataFrame(response.data)
            return df
        else:
            st.error(
                "Erro ao obter dados do banco de dados: Nenhum dado retornado.",
                icon="❌",
            )
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao conectar ao banco de dados: {e}", icon="❌")
        return pd.DataFrame()
    except KeyboardInterrupt:
        st.error("Finalizado pelo usuário.", icon="⚠️")
        return []
