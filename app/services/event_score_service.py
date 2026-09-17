def calcular_event_score(clima_data: dict, horario_evento: str) -> dict:
    if not clima_data:
        return None

    score_fatores = {"clima": 0, "chuva": 0,
                     "temperatura": 0, "horario": 0, "uv": 0}

    condicao = clima_data['condicao'].lower()
    if any(c in condicao for c in ['sol', 'limpo']):
        score_fatores['clima'] = 30
    elif any(c in condicao for c in ['nublado', 'parcialmente']):
        score_fatores['clima'] = 20
    elif any(c in condicao for c in ['garoa', 'chuva leve']):
        score_fatores['clima'] = 10
    else:
        score_fatores['clima'] = 0

    chance_chuva = clima_data['chance_chuva']
    if chance_chuva <= 20:
        score_fatores['chuva'] = 25
    elif chance_chuva <= 50:
        score_fatores['chuva'] = 15
    elif chance_chuva <= 80:
        score_fatores['chuva'] = 5

    temp = clima_data['temperatura_max']
    if 20 <= temp <= 28:
        score_fatores['temperatura'] = 20
    elif 15 <= temp < 20 or 28 < temp <= 32:
        score_fatores['temperatura'] = 10
    elif temp > 32 or temp < 15:
        score_fatores['temperatura'] = 5

    try:
        hora = int(horario_evento.split(":")[0])
        if 8 <= hora <= 17:
            score_fatores['horario'] = 15
        else:
            score_fatores['horario'] = 10
    except:
        score_fatores['horario'] = 10

    uv = clima_data['indice_uv_max']
    if uv <= 4:
        score_fatores['uv'] = 10
    elif uv <= 7:
        score_fatores['uv'] = 5

    total_score = sum(score_fatores.values())

    if total_score >= 80:
        nivel = "EXCELENTE"
    elif total_score >= 60:
        nivel = "BOM"
    elif total_score >= 40:
        nivel = "REGULAR"
    else:
        nivel = "RUIM"

    return {
        "score": total_score,
        "nivel": nivel,
        "fatores": score_fatores
    }
