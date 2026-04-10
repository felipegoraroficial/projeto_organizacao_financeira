import streamlit as st

from app.dashboard.auth.login import render_login
from app.dashboard.auth.register import render_register
from app.dashboard.auth.reset_password import render_reset_password
from app.dashboard.view.dashboard_view import render_dashboard
from app.database import init_categories, init_saldos, init_transactions
from app.database.auth.create_users_table import create_users_table
from app.functionality.categoria.categoria_view import render_categorias
from app.functionality.lancamentos.lancamentos_view import render_lancamentos


def main():
    # Inicialização do banco
    init_transactions()
    init_categories()
    init_saldos()
    create_users_table()

    st.set_page_config(page_title="Finanças Pessoais", layout="wide")

    # Controle de tela inicial
    if "mostrar_login" not in st.session_state:
        st.session_state["mostrar_login"] = True

    if "reset_password" not in st.session_state:
        st.session_state["reset_password"] = False

    # Se não estiver logado → login ou cadastro
    if "usuario" not in st.session_state:
        if st.session_state["reset_password"]:
            render_reset_password()
        elif st.session_state["mostrar_login"]:
            render_login()
        else:
            render_register()
        return

    # Logout na sidebar
    with st.sidebar:
        st.markdown("---")
        if st.button("Sair", key="logout_btn"):
            st.session_state.clear()
            st.rerun()

    # Título
    st.title("💰 Painel de Organização Financeira Pessoal")

    # Abas
    aba_dashboard, aba_lancamentos, aba_categorias = st.tabs(
        ["📊 Dashboard", "📝 Lançamentos", "🗂️ Categorias"]
    )

    with aba_dashboard:
        render_dashboard()

    with aba_lancamentos:
        render_lancamentos()

    with aba_categorias:
        render_categorias()


if __name__ == "__main__":
    main()
