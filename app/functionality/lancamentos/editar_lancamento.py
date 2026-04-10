import streamlit as st

from app.database.transactions import update_transaction


def editar_lancamento_form(lancamento):
    st.subheader("Editar Lançamento")

    data = st.date_input("Data", lancamento["Data"])
    categoria = st.text_input("Categoria", lancamento["Categoria"])
    descricao = st.text_input("Descrição", lancamento["Descrição"])
    valor = st.number_input("Valor", value=float(lancamento["Valor"]), step=0.01)
    status = st.selectbox(
        "Status",
        ["Pendente", "Pago"],
        index=0 if lancamento["Status"] == "Pendente" else 1,
    )
    recorrente = st.checkbox("Recorrente", value=bool(lancamento["Recorrente"]))
    parcelas = st.number_input(
        "Parcelas", value=int(lancamento["Parcelas"]) if lancamento["Parcelas"] else 1
    )
    data_pagamento = (
        st.date_input("Data de Pagamento", lancamento["DataPagamento"])
        if status == "Pago"
        else None
    )

    if st.button("Salvar alterações"):
        update_transaction(
            lancamento["ID"],
            data,
            categoria,
            descricao,
            valor,
            status,
            recorrente,
            parcelas,
            data_pagamento,
        )
        st.success("Lançamento atualizado com sucesso!")
        st.experimental_rerun()
