import streamlit as st

from app.dashboard.view.dashboard_view import render_dashboard
from app.database import init_categories, init_saldos, init_transactions
from app.functionality.categoria.categoria_view import render_categorias
from app.functionality.lancamentos.lancamentos_view import render_lancamentos


def main():
    # Inicialização do banco
    init_transactions()
    init_categories()
    init_saldos()

    st.set_page_config(page_title="Finanças Pessoais", layout="wide")

    st.title("💰 Painel de Organização Financeira Pessoal")

    # Abas principais
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
