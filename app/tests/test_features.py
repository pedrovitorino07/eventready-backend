from app.services.climate_analysis_service import analisar_clima
from app.services.event_score_service import calcular_event_score


def test_clima_excelente_e_score():
    clima_bom = {
        "condicao": "Céu limpo",
        "temperatura_max": 25.0,
        "sensacao_max": 26.0,
        "chance_chuva": 10,
        "vento_max": 10.0,
        "indice_uv_max": 3.0,
    }

    analise = analisar_clima(clima_bom)
    assert analise["nivel"] == "IDEAL"
    assert len(analise["motivos"]) == 0

    score = calcular_event_score(clima_bom, "14:00")
    assert score["score"] == 100
    assert score["nivel"] == "EXCELENTE"


def test_clima_chuva_forte_e_score():
    clima_ruim = {
        "condicao": "Chuva forte",
        "temperatura_max": 14.0,
        "sensacao_max": 12.0,
        "chance_chuva": 90,
        "vento_max": 35.0,
        "indice_uv_max": 2.0,
    }

    analise = analisar_clima(clima_ruim)
    assert "Alta probabilidade de chuva" in analise["motivos"]
    assert analise["nivel"] == "ALERTA"

    score = calcular_event_score(clima_ruim, "20:00")
    assert score["score"] == 25
    assert score["nivel"] == "RUIM"
