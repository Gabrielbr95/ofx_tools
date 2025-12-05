from pathlib import Path
from ofxtools.Parser import OFXTree
from ofxtools.models import OFX
from .models import MergedTransaction
from datetime import datetime
import xml.etree.ElementTree as ET

def export_ofx(merged_list: list[MergedTransaction], data_dir: Path, output_dir: Path):
    """
    Gera arquivos OFX separados por usuário (Gabriel, Carol e sem usuário).
    Usa o primeiro arquivo OFX encontrado em data_dir como base.
    """
    # Agrupa transações por usuário
    user_groups = {}
    for mtx in merged_list:
        key = mtx.user or "sem_usuario"
        user_groups.setdefault(key, []).append(mtx.tx_ofx)

    # Pega o primeiro OFX como base
    base_ofx_path = next(data_dir.glob("*.ofx"), None)
    if not base_ofx_path:
        raise FileNotFoundError("Nenhum arquivo OFX encontrado em data_dir")

    # Lê o OFX base
    with open(base_ofx_path, "rb") as f:
        tree = OFXTree()
        tree.parse(f)
        base_ofx = tree.convert()

    # Para cada grupo de usuário, gera um novo arquivo
    for user, txs in user_groups.items():
        if not txs:
            continue  # ignora grupo vazio

        # Cria cópia do OFX base
        new_ofx = base_ofx

        # Limpa todas as transações existentes
        for stmt in new_ofx.statements:
            stmt.transactions.clear()

        # Popula com novas transações
        stmt = new_ofx.statements[0]  # assume 1 statement por conta
        for tx in txs:
            stmt.transactions.append(
                tx.raw
            )

        # Gera nome do arquivo
        filename = f"{user}.ofx"
        output_file = output_dir / filename

        root = new_ofx.to_etree()

        # Opção 1: escrever como bytes diretamente
        tree = ET.ElementTree(root)
        output_file = output_dir / f"{user}.ofx"
        tree.write(output_file, encoding="utf-8", xml_declaration=True)

        print(f"Arquivo gerado: {output_file}")