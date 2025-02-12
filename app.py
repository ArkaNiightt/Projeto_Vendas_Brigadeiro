import streamlit as st
from supabaseUtils import inicializar_supabase
from view import viewApp

st.set_page_config(
    page_title="Sistema de Vendas",
    page_icon="🛒",
    layout="centered"
)

supabase = inicializar_supabase()

if 'page' not in st.session_state:
    st.session_state['page'] = "login"

# Função para verificar o login


def check_login(email, password):
    try:
        user = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )
        if user:
            return True
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")
    return False

# Função para proteger a página


def protected_page():
    viewApp()

# Interface do Streamlit


def main():
    if st.session_state['page'] == "login":
        st.markdown("### Bem-vindo ao sistema de vendas!")
        st.header("Faça login para acessar as funcionalidades.", divider=True)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False

    if not st.session_state['logged_in']:
        email = st.text_input("Email")
        password = st.text_input("Senha", type="password")

        if st.button("Login"):
            if check_login(email, password):
                st.session_state['logged_in'] = True
                st.success("Login bem-sucedido!")
                st.session_state['page'] = "cadastrar_venda"
                st.rerun()
            else:
                st.error("Credenciais inválidas")
    else:
        protected_page()
        if st.button("Logout"):
            supabase.auth.sign_out()
            st.session_state['logged_in'] = False
            st.session_state['page'] = "login"
            st.rerun()


if __name__ == "__main__":
    main()
