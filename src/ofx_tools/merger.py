from typing import List
from collections import defaultdict
from .models import TransactionOfx, TransactionText, MergedTransaction

def merge_transactions(ofx_txs: List[TransactionOfx], txt_txs: List[TransactionText]):
    merged = []

    # opcional: criar lookup por data para agilizar matching
    txt_by_date = defaultdict(list)
    for tx in txt_txs:
        txt_by_date[tx.date].append(tx)

    for ofx_tx in ofx_txs:
        user = None
        candidates = txt_by_date.get(ofx_tx.date, [])

        for txt_tx in candidates:
            # comparar valor absoluto e descrição simplificada
            if abs(txt_tx.amount) == abs(ofx_tx.amount):
                desc_ofx = ''.join(ofx_tx.description.upper().split())
                desc_txt = ''.join(txt_tx.description.upper().split())
                if desc_txt in desc_ofx or desc_ofx in desc_txt:
                    user = txt_tx.user
                    break
        
        merged.append(MergedTransaction(tx_ofx=ofx_tx, user=user))
    
    return merged
