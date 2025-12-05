from pathlib import Path
from ofxtools.Parser import OFXTree
from .models import TransactionOfx

def parse_ofx_file(path):
    if not str(path).lower().endswith(".ofx"):
        return []  # ignora arquivos que não são OFX

    txs = []
    with open(path, "rb") as f:
        tree = OFXTree()
        tree.parse(f)
        ofx = tree.convert()
    
    txs = []
    for stmt in ofx.statements:
        for trn in stmt.transactions:
            txs.append(
                TransactionOfx(
                    fitid=trn.fitid,
                    date=trn.dtposted.date(),       # ofxtools já converte para datetime
                    description=trn.memo or getattr(trn, "name", ""),
                    amount=float(trn.trnamt),      # pode ser float ou Decimal
                    raw=trn,                         # objeto original ofxtools
                    account_id=stmt.ccacctfrom.acctid
                )
            )

    return txs