from typing import List, Dict
from collections import defaultdict
from .models import TransactionOfx, TransactionText, MergedTransaction
import csv
from pathlib import Path

def merge_transactions(ofx_by_acct: Dict[str, List[TransactionOfx]], txt_txs: List[TransactionText]
):
    merged_by_acct = {}

    # opcional: criar lookup por data para agilizar matching
    txt_by_date = defaultdict(list)
    for tx in txt_txs:
        txt_by_date[tx.date].append(tx)

    for acctid, ofx_txs in ofx_by_acct.items():
        merged_list = []

        for ofx_tx in ofx_txs:
            user = None
            candidates = txt_by_date.get(ofx_tx.date, [])

            # verifica se a transação está em moeda diferente de BRL
            currency = getattr(ofx_tx.raw, "currency", None)
            is_foreign = currency is not None and getattr(currency, "cursym", "BRL") != "BRL"

            for txt_tx in candidates:
                # se não for moeda estrangeira, compara valor
                if not is_foreign and abs(txt_tx.amount) != abs(ofx_tx.amount):
                    continue

                # comparar descrições simplificadas
                desc_ofx = ''.join(ofx_tx.description.upper().split())
                desc_txt = ''.join(txt_tx.description.upper().split())
                if desc_txt in desc_ofx or desc_ofx in desc_txt:
                    user = txt_tx.user
                    break

            merged_list.append(MergedTransaction(tx_ofx=ofx_tx, user=user))
        merged_by_acct[acctid] = merged_list

    return merged_by_acct


def export_merged_csv(merged_by_acct: dict[str, list[MergedTransaction]], output_path: Path):
    """
    Gera um CSV com todas as transações do merged list.
    """
    output_path.mkdir(parents=True, exist_ok=True)

    for acctid, merged_list in merged_by_acct.items():
        #card_name = CARD_MAP.get(acctid, acctid)  # usa bandeira ou o próprio acctid
        card_name = acctid
        output_file = output_path / f"merged_{card_name}.csv"

        with open(output_file, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            # Cabeçalho
            writer.writerow(["date", "description", "amount", "user", "currency", "fitid", "acctid"])

            for mtx in merged_list:
                tx = mtx.tx_ofx
                currency = getattr(tx.raw, "currency", None)
                cursym = getattr(currency, "cursym", "BRL") if currency else "BRL"
                writer.writerow([
                    tx.date,
                    tx.description,
                    tx.amount,
                    mtx.user or "",
                    cursym,
                    tx.fitid,
                    acctid
                ])

    print(f"CSV gerado: {output_file}")