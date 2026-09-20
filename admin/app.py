"""Area riservata AMEDOO — modifica dei testi del sito.

Serve una piccola interfaccia protetta da password che legge e scrive
`contenuti.json`: il sito (container `web`) serve lo stesso file montato
in sola lettura, quindi le modifiche sono visibili subito al refresh.

Avvio: uvicorn app:app --host 0.0.0.0 --port 8000
"""

from __future__ import annotations

import base64
import html
import json
import os
import secrets
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, PlainTextResponse, RedirectResponse, Response

BASE = Path(__file__).resolve().parent
CONTENUTI = Path(os.environ.get("CONTENUTI_PATH", "/data/contenuti.json"))
CAMPI = Path(os.environ.get("CAMPI_PATH", str(BASE / "campi.json")))
UTENTE = os.environ.get("ADMIN_USER", "amedoo")
PASSWORD = os.environ.get("ADMIN_PASSWORD", "")
# percorso pubblico dell'area riservata (es. /gestione quando è dietro il sito)
PREFISSO = "/" + os.environ.get("BASE_PATH", "").strip("/") if os.environ.get("BASE_PATH", "").strip("/") else ""

app = FastAPI(title="AMEDOO — Area riservata", docs_url=None, redoc_url=None)


def autorizzato(request: Request) -> bool:
    intestazione = request.headers.get("authorization", "")
    if not intestazione.lower().startswith("basic "):
        return False
    try:
        coppia = base64.b64decode(intestazione[6:]).decode("utf-8")
        utente, password = coppia.split(":", 1)
    except Exception:
        return False
    return secrets.compare_digest(utente, UTENTE) and secrets.compare_digest(password, PASSWORD)


def non_autorizzato() -> Response:
    return PlainTextResponse(
        "Autenticazione richiesta",
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="AMEDOO area riservata"'},
    )


def leggi_campi() -> list[dict]:
    return json.loads(CAMPI.read_text(encoding="utf-8"))


def leggi_contenuti() -> dict:
    if not CONTENUTI.exists():
        return {}
    return json.loads(CONTENUTI.read_text(encoding="utf-8"))


def scrivi_in_place(path: Path, testo: str) -> None:
    """Scrive sullo stesso inode: il bind mount del container web vede subito le modifiche."""
    with open(path, "w", encoding="utf-8") as f:
        f.write(testo)
        f.flush()
        os.fsync(f.fileno())


def pagina(campi: list[dict], contenuti: dict, salvato: bool) -> str:
    gruppi: dict[str, list[dict]] = {}
    for campo in campi:
        gruppi.setdefault(campo.get("gruppo", "Altro"), []).append(campo)

    aggiornato = datetime.fromtimestamp(CONTENUTI.stat().st_mtime).strftime("%d/%m/%Y alle %H:%M") if CONTENUTI.exists() else "—"

    sezioni = []
    for gruppo, elenco in gruppi.items():
        righe = []
        for campo in elenco:
            chiave = campo["key"]
            valore = html.escape(contenuti.get(chiave, ""))
            altezza = max(1, int(campo.get("righe", 2)))
            righe.append(
                f"""
                <label class="campo">
                  <span class="etichetta">{html.escape(campo["label"])}</span>
                  <span class="chiave">{html.escape(chiave)}</span>
                  <textarea name="{html.escape(chiave)}" rows="{altezza}">{valore}</textarea>
                </label>"""
            )
        sezioni.append(
            f"""
            <section class="gruppo">
              <h2>{html.escape(gruppo)}</h2>
              {''.join(righe)}
            </section>"""
        )

    avviso = '<div class="ok">Modifiche salvate: ricarica il sito per vederle.</div>' if salvato else ""

    return f"""<!DOCTYPE html>
<html lang="it">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>AMEDOO — Area riservata</title>
<style>
  :root {{ --oliva: #3f4a2a; --oro: #b08d2f; --carta: #f7f5f0; }}
  * {{ box-sizing: border-box; }}
  body {{ margin: 0; font-family: system-ui, -apple-system, "Segoe UI", sans-serif; background: var(--carta); color: #22271c; }}
  header {{ position: sticky; top: 0; z-index: 10; background: var(--oliva); color: #f3f1e7; padding: 14px 20px; display: flex; flex-wrap: wrap; gap: 10px; align-items: center; justify-content: space-between; }}
  header h1 {{ font-size: 17px; margin: 0; letter-spacing: .3px; }}
  header .info {{ font-size: 12px; opacity: .8; }}
  main {{ max-width: 900px; margin: 0 auto; padding: 20px 16px 120px; }}
  .ok {{ background: #e6f4e6; border: 1px solid #9cc79c; color: #20521f; padding: 10px 14px; border-radius: 10px; margin-bottom: 18px; font-size: 14px; }}
  .gruppo {{ background: #fff; border: 1px solid #e3dfd3; border-radius: 14px; padding: 18px; margin-bottom: 18px; }}
  .gruppo h2 {{ font-size: 15px; margin: 0 0 14px; color: var(--oliva); border-bottom: 1px solid #eee7d8; padding-bottom: 8px; }}
  .campo {{ display: block; margin-bottom: 16px; }}
  .etichetta {{ display: block; font-size: 13px; font-weight: 600; margin-bottom: 2px; }}
  .chiave {{ display: block; font-size: 11px; color: #8a8577; font-family: ui-monospace, monospace; margin-bottom: 5px; }}
  textarea {{ width: 100%; padding: 9px 11px; border: 1px solid #d8d3c4; border-radius: 9px; font: inherit; font-size: 14px; line-height: 1.45; background: #fdfcf9; resize: vertical; }}
  textarea:focus {{ outline: 2px solid var(--oro); border-color: var(--oro); }}
  .barra {{ position: fixed; bottom: 0; left: 0; right: 0; background: #fff; border-top: 1px solid #e3dfd3; padding: 12px 20px; display: flex; justify-content: space-between; align-items: center; gap: 12px; }}
  .barra small {{ color: #8a8577; font-size: 12px; }}
  button {{ background: var(--oliva); color: #fff; border: 0; border-radius: 999px; padding: 12px 26px; font-size: 14px; font-weight: 600; cursor: pointer; }}
  button:hover {{ background: #55643a; }}
  a.sito {{ color: var(--oliva); font-size: 13px; }}
</style>
</head>
<body>
<header>
  <h1>AMEDOO · Area riservata ai testi</h1>
  <span class="info">Ultima modifica: {aggiornato}</span>
</header>
<main>
  {avviso}
  <p style="font-size:14px;color:#5c5a4e;margin-top:0">
    Modifica i testi e premi <strong>Salva</strong>: le modifiche sono online subito.
    I campi vuoti restano invariati. Per interruzioni di layout o nuove sezioni scrivi allo sviluppatore.
    <a class="sito" href="https://associazioneamedoo.it" target="_blank" rel="noopener">Apri il sito →</a>
  </p>
  <form method="post" action="{PREFISSO}/salva">
    {''.join(sezioni)}
    <div class="barra">
      <small>Le modifiche sono immediatamente visibili sul sito pubblico.</small>
      <button type="submit">Salva</button>
    </div>
  </form>
</main>
</body>
</html>"""


@app.get("/healthz", response_class=PlainTextResponse)
def healthz() -> str:
    return "ok"


@app.get("/", response_class=HTMLResponse)
def home(request: Request, ok: int = 0):
    if not autorizzato(request):
        return non_autorizzato()
    return pagina(leggi_campi(), leggi_contenuti(), bool(ok))


@app.post("/salva")
async def salva(request: Request):
    if not autorizzato(request):
        return non_autorizzato()
    modulo = await request.form()
    contenuti = leggi_contenuti()
    for campo in leggi_campi():
        chiave = campo["key"]
        if chiave in modulo:
            valore = str(modulo[chiave]).strip()
            if valore:
                contenuti[chiave] = valore
    scrivi_in_place(CONTENUTI, json.dumps(contenuti, ensure_ascii=False, indent=2) + "\n")
    return RedirectResponse(f"{PREFISSO}/?ok=1", status_code=303)


if not PASSWORD:
    raise RuntimeError("ADMIN_PASSWORD non impostata: definiscila nel file .env del docker-compose")
if CONTENUTI.is_dir():
    raise RuntimeError(
        f"{CONTENUTI} è una cartella, non un file: sul VPS esegui "
        "'cp contenuti.esempio.json contenuti.json' prima di avviare i container"
    )
