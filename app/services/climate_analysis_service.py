def analisar_clima(clima: dict) -> dict:
    motivos = []
    recomendacoes = []
    nivel = "BOM"

    chance_chuva = clima.get("chance_chuva", 0)
    indice_uv = clima.get("indice_uv_max", 0)
    vento = clima.get("vento_max", 0)
    temp = clima.get("temperatura_max", 25)

    if chance_chuva >= 60:
        nivel = "ATENCAO"
        motivos.append("Alta probabilidade de chuva")
        recomendacoes.append("Prefira um local coberto")
    elif chance_chuva >= 30:
        if nivel != "ATENCAO":
            nivel = "REGULAR"
        motivos.append("Possibilidade moderada de chuva")
        recomendacoes.append("Tenha um plano B caso garoe")

    if indice_uv >= 8.0:
        if nivel == "BOM":
            nivel = "ATENCAO"
        motivos.append("Índice UV muito alto")
        recomendacoes.append("Utilize protetor solar e busque áreas de sombra")

    if vento > 25.0:
        nivel = "ATENCAO"
        motivos.append("Ventos fortes previstos")
        recomendacoes.append("Evite estruturas leves ao ar livre")

    if temp > 35.0:
        nivel = "ATENCAO"
        motivos.append("Temperatura muito elevada")
        recomendacoes.append("Mantenha os participantes hidratados")
    elif temp < 12.0:
        if nivel == "BOM":
            nivel = "REGULAR"
        motivos.append("Temperatura baixa")
        recomendacoes.append("Considere áreas aquecidas ou agasalhos")

    if not motivos:
        motivos.append("Condições climáticas estáveis e favoráveis")
        recomendacoes.append("Aproveite o evento ao ar livre")

    return {
        "nivel": nivel,
        "motivos": motivos,
        "recomendacoes": recomendacoes
    }
