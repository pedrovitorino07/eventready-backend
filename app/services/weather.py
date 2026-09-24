from typing import Optional, Tuple
import httpx

WMO_CODES = {
    0: "Céu limpo",
    1: "Predominantemente limpo",
    2: "Parcialmente nublado",
    3: "Nublado",
    45: "Nevoeiro",
    48: "Nevoeiro com geada",
    51: "Garoa leve",
    53: "Garoa moderada",
    55: "Garoa densa",
    61: "Chuva leve",
    63: "Chuva moderada",
    65: "Chuva forte",
    80: "Pancadas de chuva leves",
    81: "Pancadas de chuva moderadas",
    82: "Pancadas de chuva violentas",
    95: "Trovoada leve ou moderada",
}


def obter_coordenadas(local: str) -> Tuple[Optional[float], Optional[float]]:
    url = "https://geocoding-api.open-meteo.com/v1/search"
    params = {"name": local, "count": 1, "language": "pt", "format": "json"}

    try:
        response = httpx.get(url, params=params, timeout=5.0)
        data = response.json()
        if data.get("results"):
            primeiro = data["results"][0]
            return primeiro["latitude"], primeiro["longitude"]
    except Exception as e:
        print(f"Erro no Geocoding: {e}")

    return None, None


def obter_previsao_clima(
    lat: float, lon: float, data_evento: str
) -> Tuple[Optional[dict], Optional[str]]:
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": [
            "weather_code",
            "temperature_2m_max",
            "apparent_temperature_max",
            "precipitation_probability_max",
            "wind_speed_10m_max",
            "uv_index_max",
            "sunrise",
            "sunset",
        ],
        "start_date": data_evento,
        "end_date": data_evento,
        "timezone": "auto",
    }

    try:
        response = httpx.get(url, params=params, timeout=5.0)
        data = response.json()

        if response.status_code == 200:
            return data, None
        else:
            erro_msg = data.get(
                "reason", f"Erro Open-Meteo (Status {response.status_code})"
            )
            return None, erro_msg
    except Exception as e:
        return None, f"Exceção de conexão: {str(e)}"


def gerar_recomendacao(
    chance_chuva: int, vento_kmh: float, uv_index: float, temp_max: float
) -> str:
    recomendacoes = []

    if chance_chuva >= 70:
        recomendacoes.append(
            "Alta probabilidade de chuva — garanta local coberto")
    elif chance_chuva >= 40:
        recomendacoes.append(
            "Chance de chuva moderada — considere um plano B coberto")

    if vento_kmh >= 30:
        recomendacoes.append(
            "Ventos fortes — evite estruturas temporárias soltas (tendas/ombrelones)")
    elif vento_kmh >= 20:
        recomendacoes.append(
            "Vento moderado — atente-se à fixação de decoração e tendas")

    if uv_index >= 7:
        recomendacoes.append(
            "Índice UV muito alto — providencie áreas de sombra e protetor solar")
    if temp_max >= 32:
        recomendacoes.append(
            "Dia muito quente — reforce a oferta de bebidas geladas e ventilação")

    if not recomendacoes:
        return "Condições meteorológicas favoráveis para eventos ao ar livre!"

    return " | ".join(recomendacoes)


def formatar_resposta_clima(evento_nome: str, dados_raw: dict) -> dict:
    daily = dados_raw.get("daily", {})

    code = daily.get("weather_code", [0])[
        0] if daily.get("weather_code") else 0

    temp_max = float(daily.get("temperature_2m_max", [0.0])[0])
    sensacao_max = float(daily.get("apparent_temperature_max", [0.0])[0])
    chance_chuva = int(daily.get("precipitation_probability_max", [0])[0] or 0)
    vento_max = float(daily.get("wind_speed_10m_max", [0.0])[0])
    uv_max = float(daily.get("uv_index_max", [0.0])[0])

    nascer_raw = daily.get("sunrise", [""])[0]
    por_raw = daily.get("sunset", [""])[0]

    nascer_hora = nascer_raw.split(
        "T")[-1] if "T" in nascer_raw else nascer_raw
    por_hora = por_raw.split("T")[-1] if "T" in por_raw else por_raw

    recomendacao = gerar_recomendacao(
        chance_chuva=chance_chuva,
        vento_kmh=vento_max,
        uv_index=uv_max,
        temp_max=temp_max,
    )

    return {
        "condicao": WMO_CODES.get(code, "Condição desconhecida"),
        "temperatura_max": temp_max,
        "sensacao_max": sensacao_max,
        "chance_chuva": chance_chuva,
        "vento_max": vento_max,
        "indice_uv_max": uv_max,
        "sol": {"nascer": nascer_hora, "por": por_hora},
        "recomendacao": recomendacao,
    }
