import streamlit as st

from app.auth.new_user_auth import cadastrar_usuario


def render_register():
    st.title("📝 Criar Conta")

    nome = st.text_input("Nome completo")
    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")
    confirmar = st.text_input("Confirmar senha", type="password")

    if st.button("Cadastrar"):
        if senha != confirmar:
            st.error("As senhas não coincidem.")
            return

        sucesso = cadastrar_usuario(nome, email, senha)

        if sucesso:
            st.success("Conta criada com sucesso! Faça login para continuar.")
            st.session_state["mostrar_login"] = True
            st.rerun()
        else:
            st.error("Este email já está cadastrado.")

    if st.button("⬅️ Voltar para o Login"):
        st.session_state["mostrar_login"] = True
        st.session_state["reset_password"] = False
        st.rerun()
