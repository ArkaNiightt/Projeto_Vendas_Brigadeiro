import streamlit as st

st.set_page_config(
    page_title="Sistema de Vendas",
    page_icon="🛒",
    layout="wide"
)

from view import viewApp
from database.supabaseUtils import inicializar_supabase

supabase = inicializar_supabase()
HERO_IMAGE = "assets/loginHero.jpg"

def check_login(email, password):
    try:
        user = supabase.auth.sign_in_with_password({"email": email, "password": password})
        if user:
            return True
    except Exception as e:
        print(f"Erro ao fazer login: {str(e)}")
    return False

def protected_page():
    viewApp()

def login_page():
    col_01, col_02 = st.columns(2, vertical_alignment="center", gap="large")

    with col_01:
        st.image(image=HERO_IMAGE, use_container_width=True)

    with col_02:
        st.header("Faça login para acessar as funcionalidades.", divider=True)
        email = st.text_input(
            label="Email",
            key="email_login_input",
            placeholder="Digite seu email"
        )
        password = st.text_input(
            label="Senha",
            type="password",
            key="password_login_input",
            placeholder="Digite sua senha"
        )

        if st.button(
            label="Entrar",
            key="btn_login",
            type="secondary",
            icon="🚀",
            use_container_width=True
        ):
            if check_login(email, password):
                st.session_state['logged_in'] = True
                st.success("Login bem-sucedido!", icon="✅")
                st.rerun()  # Recarrega a página para atualizar o estado
            else:
                st.error("Credenciais inválidas", icon="❌")

def main():
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['page'] = "login"

    if st.session_state['logged_in']:
        st.session_state['page'] = "home"
        protected_page()
    else:
        login_page()

if __name__ == "__main__":
    main()
