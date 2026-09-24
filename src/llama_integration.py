import json

import requests


DEFAULT_MODEL = "llama3.2:3b"


def _json_default(value):
    if hasattr(value, "item"):
        return value.item()
    raise TypeError(f"{type(value).__name__} is not JSON serializable")


def run_llama(prompt: str, model: str = DEFAULT_MODEL) -> str:
    """Run the configured local Ollama model and surface execution failures."""
    try:
        response = requests.post(
            "http://127.0.0.1:11434/api/generate",
            json={
                "model": model,
                "prompt": prompt,
                "stream": False,
                "keep_alive": "10m",
                "options": {"num_predict": 220, "temperature": 0.2},
            },
            timeout=(5, 300),
        )
        response.raise_for_status()
    except requests.ConnectionError as error:
        raise RuntimeError(
            "Ollama hizmetine baglanilamadi. `ollama serve` ile hizmeti baslatin."
        ) from error
    except requests.Timeout as error:
        raise RuntimeError(f"Ollama modeli {model} 300 saniye icinde yanit vermedi.") from error
    except requests.HTTPError as error:
        detail = error.response.text.strip()
        raise RuntimeError(f"Ollama modeli {model} calistirilamadi: {detail}") from error

    output = response.json().get("response", "").strip()
    if not output:
        raise RuntimeError(f"Ollama modeli {model} bos yanit verdi.")
    return output


def analyze_department(department: str, responsibilities: str, metrics: dict) -> dict:
    """Ask Ollama for an actionable Turkish analysis grounded only in the metrics."""
    prompt = f"""Sen Elaia Ceramics'in {department} departman analistisin.
Departman sorumluluklari: {responsibilities}

Guncel metrikler:
{json.dumps(metrics, ensure_ascii=False, indent=2, default=_json_default)}

Yalnizca verilen metriklere dayan. 3 kisa bolum kullan:
1. Durum
2. Riskler veya firsatlar
3. Onerilen aksiyonlar
Sayisal olmayan bilgi uydurma."""
    return {
        "metrikler": metrics,
        "yapay_zeka_analizi": run_llama(prompt),
    }
