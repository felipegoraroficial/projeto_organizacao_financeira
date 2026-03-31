def filtrar_por_periodo(df, ano_sel, mes_sel):
    df_filtrado = df.copy()

    if ano_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Data"].dt.year == int(ano_sel)]

    if mes_sel != "Todos":
        df_filtrado = df_filtrado[df_filtrado["Data"].dt.month == int(mes_sel)]

    return df_filtrado
