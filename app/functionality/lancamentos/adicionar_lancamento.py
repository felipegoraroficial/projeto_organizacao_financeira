import streamlit as st
from datetime import datetime
from dateutil.relativedelta import relativedelta

from app.database import (
    insert_transaction,
    load_categories,
)


def render_adicionar_lancamento():
    categorias_raw = load_categories()

    categorias_por_tipo = {
        "Receita": [nome for nome, tipo in categorias_raw if tipo == "Receita"],
        "Despesa": [nome for nome, tipo in categorias_raw if tipo == "Despesa"],
    }

    recorrente = st.checkbox("Lançamento recorrente?")
    parcelas = st.slider("Repetir por quantos meses?", 1, 12, 1) if recorrente else 1

    col1, col2 = st.columns(2)
    date = col1.date_input("Data")
    tipo = col2.selectbox("Tipo", ["Receita", "Despesa"])

    # 🔥 AGORA FUNCIONA: fora do form, atualiza dinamicamente
    categorias_filtradas = categorias_por_tipo.get(tipo, [])
    category = st.selectbox(
        "Categoria",
        categorias_filtradas,
        key=f"categoria_{tipo}"
    )

    with st.form("form_lancamento"):
        description = st.text_input("Descrição")
        value = st.number_input("Valor", min_value=0.0, format="%.2f")
        status = st.selectbox("Status do lançamento", ["Pago", "Pendente"])

        submitted = st.form_submit_button("Adicionar")

        if submitted:
            insert_transaction(
                str(date),
                tipo,
                category,
                description,
                value,
                status.lower(),
                1 if recorrente else 0,
                parcelas,
            )

            if recorrente:
                data_base = datetime.strptime(str(date), "%Y-%m-%d")
                for i in range(1, parcelas):
                    nova_data = data_base + relativedelta(months=i)
                    insert_transaction(
                        nova_data.strftime("%Y-%m-%d"),
                        tipo,
                        category,
                        f"{description} (Parcela {i+1}/{parcelas})",
                        value,
                        "pendente",
                        0,
                        1,
                    )

            st.success("Lançamento(s) adicionado(s) com sucesso!")
            st.rerun()