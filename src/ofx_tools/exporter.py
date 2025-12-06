from pathlib import Path
from ofxtools.Parser import OFXTree
from ofxtools.models import OFX
from .models import MergedTransaction
from datetime import datetime
import xml.etree.ElementTree as ET

# Mapeamento manual de ACCTID → bandeira
CARD_MAP = {
    "4984000000005460": "visa",
    "6550000000007799": "elo",
}

def export_ofx(merged_list: list[MergedTransaction], data_dir: Path, output_dir: Path, acctid_map: dict):
    """
    Gera arquivos OFX separados por usuário (Gabriel, Carol e sem usuário).
    Usa o primeiro arquivo OFX encontrado em data_dir como base.
    """
    # Agrupa transações por usuário
    user_groups = {}
    for mtx in merged_list:
        card = mtx.tx_ofx.account_id
        user = mtx.user or "sem_usuario"
        user_groups.setdefault(card, {}).setdefault(user, []).append(mtx.tx_ofx)

    # Para cada grupo de usuário, gera um novo arquivo
    for card, user_dict in user_groups.items():
        # Pega arquivo base a partir do dicionário
        base_ofx_path = acctid_map.get(card)
        if not base_ofx_path:
            print(f"Base OFX não encontrada para cartão {card}, pulando...")
            continue
        
        # Lê OFX base
        with open(base_ofx_path, "rb") as f:
            tree = OFXTree()
            tree.parse(f)
            base_ofx = tree.convert()


        for user, txs in user_dict.items():
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
            card_name = CARD_MAP.get(card, "desconhecido")
            # Gera nome do arquivo
            filename = f"{card_name}_{user}.ofx"
            output_file = output_dir / filename

            root = new_ofx.to_etree()

            # Opção 1: escrever como bytes diretamente
            tree = ET.ElementTree(root)
            tree.write(output_file, encoding="utf-8", xml_declaration=True)

            print(f"Arquivo gerado: {output_file}")