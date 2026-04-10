from datetime import datetime

import pandas as pd
import streamlit as st

from app.database import (
    delete_transaction,
    load_transactions,
    marcar_como_pago,
)
from app.database.transactions.update_transaction import update_transaction


def render_listar_lancamentos():

    usuario_id = st.session_state["usuario"]["id"]
    data = load_transactions(usuario_id)

    df_lanc = pd.DataFrame(
        data,
        columns=[
            "ID",
            "Data",
            "Tipo",
            "Categoria",
            "Descrição",
            "Valor",
            "Status",
            "Recorrente",
            "Parcelas",
            "DataPagamento",
        ],
    )

    if df_lanc.empty:
        st.info("Nenhum lançamento cadastrado ainda.")
        return

    df_lanc["Data"] = pd.to_datetime(df_lanc["Data"])

    st.markdown("### 🔎 Filtros")

    categorias_unicas = ["Todas"] + sorted(df_lanc["Categoria"].unique())
    filtro_categoria = st.selectbox("Filtrar por Categoria", categorias_unicas)

    descricoes_unicas = ["Todas"] + sorted(df_lanc["Descrição"].dropna().unique())
    filtro_descricao = st.selectbox("Filtrar por Descrição", descricoes_unicas)

    df_filtrado = df_lanc.copy()

    if filtro_categoria != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Categoria"] == filtro_categoria]

    if filtro_descricao != "Todas":
        df_filtrado = df_filtrado[df_filtrado["Descrição"] == filtro_descricao]

    st.markdown("### 🗑️ / ✔️ / ✏️ Lançamentos filtrados")

    if df_filtrado.empty:
        st.info("Nenhum lançamento encontrado com os filtros selecionados.")
        return

    # Se estiver editando algum lançamento, renderiza o formulário
    if "editando" in st.session_state:
        lanc = df_lanc[df_lanc["ID"] == st.session_state["editando"]].iloc[0]

        st.subheader("✏️ Editar lançamento")

        nova_data = st.date_input("Data", lanc["Data"])
        nova_categoria = st.text_input("Categoria", lanc["Categoria"])
        nova_descricao = st.text_input("Descrição", lanc["Descrição"])
        novo_valor = st.number_input("Valor", value=float(lanc["Valor"]), step=0.01)
        novo_status = st.selectbox(
            "Status",
            ["pendente", "pago"],
            index=0 if lanc["Status"] == "pendente" else 1,
        )
        novo_recorrente = st.checkbox("Recorrente", value=bool(lanc["Recorrente"]))
        novas_parcelas = st.number_input(
            "Parcelas",
            value=int(lanc["Parcelas"]) if lanc["Parcelas"] else 1,
            min_value=1,
        )

        nova_data_pagamento = None
        if novo_status == "pago":
            nova_data_pagamento = st.date_input(
                "Data de Pagamento",
                lanc["DataPagamento"] if lanc["DataPagamento"] else datetime.today(),
            )

        if st.button("Salvar alterações"):
            update_transaction(
                lanc["ID"],
                nova_data,
                nova_categoria,
                nova_descricao,
                novo_valor,
                novo_status,
                novo_recorrente,
                novas_parcelas,
                nova_data_pagamento,
            )
            st.success("Lançamento atualizado com sucesso!")
            del st.session_state["editando"]
            st.rerun()

        if st.button("Cancelar edição"):
            del st.session_state["editando"]
            st.rerun()

        st.markdown("---")

    # Lista os lançamentos
    for _, row in df_filtrado.iterrows():
        colA, colB, colC, colD = st.columns([0.1, 0.1, 0.1, 0.7])

        # Excluir
        if colA.button("🗑️", key=f"del_{row['ID']}"):
            delete_transaction(row["ID"])
            st.warning(f"Lançamento {row['ID']} apagado!")
            st.rerun()

        # Marcar como pago
        if row["Status"] == "pendente":
            if colB.button("✔️", key=f"pago_{row['ID']}"):
                data_pag = st.date_input(
                    "Data do pagamento",
                    key=f"data_pag_{row['ID']}",
                    value=datetime.today(),
                )
                marcar_como_pago(row["ID"], str(data_pag))
                st.success(f"Lançamento {row['ID']} marcado como pago!")
                st.rerun()
        else:
            colB.write("✅")

        # Editar
        if colC.button("✏️", key=f"edit_{row['ID']}"):
            st.session_state["editando"] = row["ID"]
            st.rerun()

        texto = (
            f"**{row['Data'].date()}** — {row['Tipo']} — {row['Categoria']} — "
            f"{row['Descrição']} — R$ {row['Valor']:,.2f} — "
            f"Status: {row['Status'].capitalize()}"
        )

        if row["DataPagamento"]:
            texto += f" — Pago em: {row['DataPagamento']}"

        colD.write(texto)
