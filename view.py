import streamlit as st
from Client.registerClient import carregar_registro_vendas
from Client.showCustomers import showCustomers
from database.supabaseUtils import inicializar_supabase

supabase = inicializar_supabase()


def viewApp():
    try:
        with st.sidebar:
            st.title("⚡ Ferramentas de vendas")
            st.markdown("Selecione uma das opções abaixo para começar:")

            opcao = st.selectbox(
                "Escolha sua análise:",
                ["Registrar Cliente", "Listar Vendas", "Chat com Agente de IA"],
                key="opcao_analise",
                format_func=lambda x: (
                    f"📈 {x}" if x == "Registrar Cliente"
                    else f"⭐ {x}" if x == "Listar Vendas"
                    else f"🌐 {x}"
                ),
                help="Selecione a ferramenta desejada para vendas",
                placeholder="Listar Vendas",
            )

            if st.button(
                label="Logout",
                key="btn_logout",
                type="tertiary",
                icon="🔒",
                use_container_width=True
            ):
                supabase.auth.sign_out()
                st.session_state['logged_in'] = False
                st.session_state['page'] = "login"
                st.rerun()

        st.markdown("---")
        if opcao == "Registrar Cliente":
            st.session_state['page'] = "cadastrar_venda"
            carregar_registro_vendas()
            st.toast("Dados carregados com sucesso.", icon="✅")
        elif opcao == "Listar Vendas":
            st.session_state['page'] = "listar_vendas"
            showCustomers()
            st.toast("Dados carregados com sucesso.", icon="✅")
        elif opcao == "Chat com Agente de IA":
            st.toast("Chat iniciado com sucesso.", icon="✅")
        st.sidebar.markdown("---")
        with st.sidebar:
            st.info(
                "💡 Dica: Certifique-se de usar a melhor ferramenta para obter os melhores resultados."
            )
    except KeyboardInterrupt:
        st.error("O aplicativo foi interrompido.")
        st.stop()
        exit()
    except Exception as e:
        print(e)
