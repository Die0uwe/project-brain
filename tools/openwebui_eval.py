#!/usr/bin/env python3
"""Controleert of de lokale AI de brain-collectie echt gebruikt (alleen standaardbibliotheek).

Stelt vaste vragen via Open WebUI met de collectie als bron en kijkt of het antwoord de verwachte
feiten bevat. De feiten komen uit project-brain; als de brain verandert, pas dan QUESTIONS aan.

Instellingen: dezelfde als openwebui_sync.py (OPENWEBUI_URL, OPENWEBUI_API_KEY, OPENWEBUI_KNOWLEDGE)
plus OPENWEBUI_MODEL (de modelnaam in Open WebUI, bijvoorbeeld qwen3:4b of je eigen Modelfile-naam).

Gebruik: python tools/openwebui_eval.py [--model NAAM] [--timeout 300]
Exitcode 0 = alle vragen goed, 1 = een of meer vragen fout, 2 = instellingen ontbreken.
"""
from __future__ import annotations

import argparse
import os
import re
import sys
import time

import openwebui_sync as sync

# (vraag, [alle woorden die in het antwoord moeten voorkomen])
QUESTIONS = [
    ("Welke versie van Blueprint CMS staat er nu op main?", ["1.34.0"]),
    ("Welke databasetabel hoort bij wachtwoord herstellen in Blueprint CMS?", ["cf_password_resets"]),
    ("Hoe lang is een wachtwoord-herstel-token geldig in Blueprint CMS?", ["60 minuten"]),
    ("Wat is het currency ID van de Veteran Dawncrest?", ["3341"]),
    ("Wat moet ik gebruiken in plaats van OptionsSliderTemplate in een Midnight-addon?", ["custom"]),
    ("Welke wiskundige functie zit in de kompasformule van DelveTracker?", ["atan2"]),
    ("Welke versie heeft ScriptSpace CMS volgens de manifest?", ["0.25.0"]),
    # Geen verzinsel: dit staat in de brain als onbekend
    ("Op welke hosting draait dieouwe.nl en wat is de stack?", ["onbekend"]),
]


def strip_think(text: str) -> str:
    return re.sub(r"<think>.*?</think>", "", text, flags=re.S).strip()


def ask(client: "sync.OpenWebUI", model: str, kid: str, question: str) -> tuple[str, bool]:
    data = client.json("POST", "/api/chat/completions", {
        "model": model,
        "stream": False,
        "messages": [{"role": "user", "content": question}],
        "files": [{"type": "collection", "id": kid}],
    })
    try:
        # 'sources' is informatief: Open WebUI toont daarmee welke bestanden het antwoord voedden
        return strip_think(data["choices"][0]["message"]["content"] or ""), bool(data.get("sources"))
    except (KeyError, IndexError, TypeError):
        raise sync.ApiError(200, "onverwacht antwoordformaat van /api/chat/completions") from None


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description="Test de brain-collectie in Open WebUI met vaste vragen.")
    p.add_argument("--model", help="modelnaam in Open WebUI (anders OPENWEBUI_MODEL)")
    p.add_argument("--timeout", type=int, default=300, help="seconden per vraag (een klein model op CPU is traag)")
    args = p.parse_args(argv)

    sync.load_env_files()
    url_raw, key = os.environ.get("OPENWEBUI_URL", ""), os.environ.get("OPENWEBUI_API_KEY", "")
    model = args.model or os.environ.get("OPENWEBUI_MODEL", "")
    if not (url_raw and key and model):
        print("Zet OPENWEBUI_URL, OPENWEBUI_API_KEY en OPENWEBUI_MODEL (of geef --model mee).")
        return 2
    try:
        client = sync.OpenWebUI(sync.check_url(url_raw), key, args.timeout)
    except ValueError as exc:
        print(f"Instelling onjuist: {exc}")
        return 2

    name = os.environ.get("OPENWEBUI_KNOWLEDGE") or sync.DEFAULT_KNOWLEDGE
    try:
        found = [k for k in client.list_knowledge() if k.get("name") == name]
    except sync.ApiError as exc:
        print(f"Kan Open WebUI niet bevragen: {exc}")
        return 1
    if not found:
        print(f"Collectie '{name}' bestaat niet: draai eerst tools/openwebui_sync.py.")
        return 1

    failed = 0
    for question, expected in QUESTIONS:
        started = time.monotonic()
        try:
            answer, cited = ask(client, model, found[0]["id"], question)
        except sync.ApiError as exc:
            print(f"FOUT  {question}\n      {exc}")
            failed += 1
            continue
        missing = [w for w in expected if w.lower() not in answer.lower()]
        seconds = time.monotonic() - started
        if missing:
            failed += 1
            print(f"FOUT  ({seconds:.0f}s) {question}\n      mist: {', '.join(missing)}\n      antwoord: {answer[:200]!r}")
        else:
            print(f"OK    ({seconds:.0f}s, bronnen: {'ja' if cited else 'niet gemeld'}) {question}")
    print(f"\n{len(QUESTIONS) - failed}/{len(QUESTIONS)} goed.")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    sys.exit(main())
