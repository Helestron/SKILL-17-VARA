#!/usr/bin/env python3
"""Gera dist/skill-17a-lote-minutas-helestron.zip (mesma estrutura do pacote enviado ao Claude)."""
import zipfile
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
NOME = "skill-17a-lote-minutas-helestron"
origem = RAIZ / NOME
destino = RAIZ / "dist" / f"{NOME}.zip"
destino.parent.mkdir(exist_ok=True)
with zipfile.ZipFile(destino, "w", zipfile.ZIP_DEFLATED) as z:
    for arq in sorted(origem.rglob("*")):
        if arq.is_file() and "__pycache__" not in arq.parts and arq.suffix not in (".pyc", ".tmp"):
            z.write(arq, Path(NOME) / arq.relative_to(origem))
print(destino, destino.stat().st_size, "bytes")
