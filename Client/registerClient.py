import streamlit as st
from datetime import datetime, time
from database.supabaseUtils import inicializar_supabase

supabase = inicializar_supabase()


def is_authenticated():
    user = supabase.auth.user()
    return user is not None


def carregar_registro_vendas():
    if st.session_state['page'] == "cadastrar_venda":

        st.header(body="Registrar uma venda", divider=True)

        with st.form( 
            key="registro_venda", 
            clear_on_submit=True,
            border=True
            ):
            produto = st.text_input(
                label="Produto",
                key="produto_input",
                placeholder="Digite o nome do produto"
            )
            cliente = st.text_input(
                label="Cliente",
                key="cliente_input",
                placeholder="Digite o nome do cliente")
            valor = st.number_input(
                label="Valor",
                min_value=1.0,
                format="%.2f",
                key="valor_input",
                placeholder="Digite o valor do produto"
            )
            quantidade = st.number_input(
                label="Quantidade",
                min_value=1,
                step=1,
                key="quantidade_input",
                placeholder="Digite a quantidade de produtos")
            data_venda = st.date_input(
                label="Data da Venda",
                value=datetime.now(),
                key="data_input"
            )
            fiado = st.checkbox(
                label="Fiado",
                key="fiado_checkbox"
            )
            forma_pagamento = st.selectbox(
                label="Forma de Pagamento",
                options=["Dinheiro", "Cartão", "Pix", "Boleto"],
                key="forma_pagamento_selectbox"
            )
            submit = st.form_submit_button(
                label="Registrar Venda", 
                type="primary", 
                icon="📝", 
                use_container_width=True
            )

        if submit:
            venda = {
                "produto": produto,
                "cliente": cliente,
                "valor": valor,
                "quantidade": quantidade,
                "data": datetime.combine(data_venda, time.min).isoformat(),
                "fiado": fiado,
                "forma_de_pagamento": forma_pagamento
            }
            try:
                response = supabase.table("vendas").insert(venda).execute()
                if response:
                    st.toast(f"Dados inseridos com sucesso", icon="✅")
                    st.write(response.data)
            except Exception as e:
                st.error(f"Erro: {str(e)}")
