from app.database import get_saldo_inicial, set_saldo_inicial


def calcular_saldo_anterior(df, ano_sel, mes_sel):

    # CASO 1 — Nenhum filtro aplicado
    if ano_sel == "Todos" and mes_sel == "Todos":
        primeira_data = df["Data"].min()
        ano = primeira_data.year
        mes = primeira_data.month

        saldo_manual = get_saldo_inicial(ano, mes)
        if saldo_manual != 0:
            return saldo_manual

        df_anterior = df[df["Data"] < primeira_data]

        receitas = df_anterior[df_anterior["Tipo"] == "Receita"]["Valor"].sum()
        despesas = df_anterior[df_anterior["Tipo"] == "Despesa"]["Valor"].sum()

        return receitas - despesas

    # CASO 2 — Apenas o ano filtrado
    if ano_sel != "Todos" and mes_sel == "Todos":
        ano = int(ano_sel)

        # 1) Tenta encontrar o primeiro mês do ano com saldo inicial manual
        for mes in range(1, 13):
            saldo_manual = get_saldo_inicial(ano, mes)
            if saldo_manual != 0:
                return saldo_manual

        # 2) Se não houver saldo manual, calcula tudo antes do ano
        df_anterior = df[df["Data"].dt.year < ano]

        receitas = df_anterior[df_anterior["Tipo"] == "Receita"]["Valor"].sum()
        despesas = df_anterior[df_anterior["Tipo"] == "Despesa"]["Valor"].sum()

        return receitas - despesas

    # CASO 3 — Ano + mês filtrados (sua lógica original)
    ano_atual = int(ano_sel)
    mes_atual = int(mes_sel)

    saldo_manual = get_saldo_inicial(ano_atual, mes_atual)
    if saldo_manual != 0:
        return saldo_manual

    if mes_atual == 1:
        mes_ant = 12
        ano_ant = ano_atual - 1
    else:
        mes_ant = mes_atual - 1
        ano_ant = ano_atual

    saldo_inicial_mes_ant = get_saldo_inicial(ano_ant, mes_ant)

    df_mes_ant = df[(df["Data"].dt.year == ano_ant) & (df["Data"].dt.month == mes_ant)]

    total_rec_ant = df_mes_ant[df_mes_ant["Tipo"] == "Receita"]["Valor"].sum()
    total_desp_ant = df_mes_ant[df_mes_ant["Tipo"] == "Despesa"]["Valor"].sum()

    saldo_final_mes_ant = saldo_inicial_mes_ant + (total_rec_ant - total_desp_ant)

    set_saldo_inicial(ano_atual, mes_atual, saldo_final_mes_ant)

    return saldo_final_mes_ant
