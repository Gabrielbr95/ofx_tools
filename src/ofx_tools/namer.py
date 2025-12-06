from collections import defaultdict
from typing import List
from .models import TransactionGroup, TransactionText


def populate_user(groups: List[TransactionGroup], txt_txs: List[TransactionText]):
    # indexa TXT por data para agilizar
    txt_by_date = defaultdict(list)
    for tx in txt_txs:
        txt_by_date[tx.date].append(tx)

    for group in groups:
        for ofx_tx in group.txs_ofx:
            ofx_tx_user = None
            candidates = txt_by_date.get(ofx_tx.date, [])

            # verifica moeda estrangeira
            currency = getattr(ofx_tx.raw, "currency", None)
            is_foreign = currency is not None and getattr(currency, "cursym", "BRL") != "BRL"

            for txt_tx in candidates:
                if not is_foreign and abs(txt_tx.amount) != abs(ofx_tx.amount):
                    continue

                desc_ofx = ''.join(ofx_tx.description.upper().split())
                desc_txt = ''.join(txt_tx.description.upper().split())
                if desc_txt in desc_ofx or desc_ofx in desc_txt:
                    ofx_tx_user = txt_tx.user
                    break

            # popula TransactionOfx.user
            ofx_tx.user = ofx_tx_user
