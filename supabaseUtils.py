from supabase import create_client, Client
import streamlit as st
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
