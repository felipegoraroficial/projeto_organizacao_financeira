import streamlit as st

from app.auth.new_password import atualizar_senha


def render_reset_password():
    st.title("🔑 Recuperar Senha")

    email = st.text_input("Digite seu e-mail cadastrado")

    nova_senha = st.text_input("Nova senha", type="password")
    confirmar = st.text_input("Confirmar nova senha", type="password")

    if st.button("Alterar senha"):
        if nova_senha != confirmar:
            st.error("As senhas não coincidem.")
            return

        sucesso = atualizar_senha(email, nova_senha)

        if sucesso:
            st.success("Senha alterada com sucesso! Faça login.")
            st.session_state["mostrar_login"] = True
            st.rerun()
        else:
            st.error("E-mail não encontrado.")

    if st.button("⬅️ Voltar para o Login"):
        st.session_state["mostrar_login"] = True
        st.session_state["reset_password"] = False
        st.rerun()
