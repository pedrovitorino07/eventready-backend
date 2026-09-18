def calcular_event_score(clima_data: dict, horario: str) -> dict:
    chance_chuva = clima_data.get("chance_chuva", 0)
    temp_max = clima_data.get("temperatura_max", 25.0)

    pts_chuva = max(0, int(25 - (chance_chuva * 0.25)))

    if 20 <= temp_max <= 28:
        pts_temp = 25
    elif 18 <= temp_max < 20 or 28 < temp_max <= 33:
        pts_temp = 18
    else:
        pts_temp = 10

    condicao = clima_data.get("condicao", "").lower()
    if "claro" in condicao or "sol" in condicao:
        pts_clima = 25
    elif "nublado" in condicao:
        pts_clima = 20
    else:
        pts_clima = 12

    hora = int(horario.split(":")[0]) if ":" in horario else 12
    if 10 <= hora <= 17:
        pts_horario = 22
    else:
        pts_horario = 25

    score_total = pts_chuva + pts_temp + pts_clima + pts_horario

    if score_total >= 85:
        nivel = "EXCELENTE"
    elif score_total >= 70:
        nivel = "BOM"
    elif score_total >= 50:
        nivel = "REGULAR"
    else:
        nivel = "RUIM"

    return {
        "score": score_total,
        "nivel": nivel,
        "fatores": {
            "clima": pts_clima,
            "chuva": pts_chuva,
            "temperatura": pts_temp,
            "horario": pts_horario
        }
    }
