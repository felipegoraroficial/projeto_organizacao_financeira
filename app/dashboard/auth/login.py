import streamlit as st

from app.auth.auth_service import autenticar_usuario


def render_login():
    st.title("🔐 Login")

    email = st.text_input("Email")
    senha = st.text_input("Senha", type="password")

    if st.button("Entrar"):
        usuario = autenticar_usuario(email, senha)

        if usuario:
            st.session_state["usuario"] = usuario
            st.rerun()
        else:
            st.error("Email ou senha incorretos.")

    st.markdown("---")

    if st.button("Criar nova conta"):
        st.session_state["mostrar_login"] = False
        st.session_state["reset_password"] = False
        st.rerun()

    if st.button("Esqueci minha senha"):
        st.session_state["mostrar_login"] = False
        st.session_state["reset_password"] = True
        st.rerun()
