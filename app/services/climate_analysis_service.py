def analisar_clima(clima_data: dict) -> dict:
    if not clima_data:
        return None

    motivos = []
    recomendacoes = []

    if clima_data['chance_chuva'] >= 70:
        motivos.append("Alta probabilidade de chuva")
        recomendacoes.append("Prefira um local coberto")
    elif clima_data['chance_chuva'] >= 40:
        motivos.append("Risco moderado de chuva")
        recomendacoes.append("Tenha um plano B para áreas abertas")

    if clima_data['indice_uv_max'] >= 8:
        motivos.append("Índice UV muito alto")
        recomendacoes.append("Providencie áreas de sombra e protetor solar")

    if clima_data['temperatura_max'] >= 32:
        motivos.append("Temperatura muito alta")
        recomendacoes.append("Garanta hidratação e ventilação adequada")
    elif clima_data['temperatura_max'] <= 15:
        motivos.append("Temperatura baixa")
        recomendacoes.append("Recomende agasalhos ou providencie aquecedores")

    if clima_data['vento_max'] >= 30:
        motivos.append("Ventos fortes")
        recomendacoes.append(
            "Cuidado com estruturas leves montadas ao ar livre")

    qtd_motivos = len(motivos)
    if qtd_motivos == 0:
        nivel = "IDEAL"
    elif qtd_motivos <= 2:
        nivel = "ATENCAO"
    else:
        nivel = "ALERTA"

    return {
        "nivel": nivel,
        "motivos": motivos,
        "recomendacoes": recomendacoes
    }
