# test_parse.py
from ofx_tools.loader import load_all_txt, load_all_ofx  
from ofx_tools.merger import merge_transactions
from ofx_tools.exporter import export_ofx
from pathlib import Path

# caminho do arquivo txt para testar
data = Path(__file__).parent.parent / "data"
output = Path(__file__).parent.parent / "output"

#txs = parse_txt_file(str(path))

txs = load_all_txt()
ofx = load_all_ofx()
mrg = merge_transactions (ofx, txs)
"""
for t in txs:
    print(f"Usuário: {t.user}, Data: {t.date}, Desc: {t.description}, Valor: {t.amount}")

for t in ofx:
    print(f"ID: {t.fitid}, Data: {t.date}, Desc: {t.description}, Valor: {t.amount}")
"""

"""
for t in mrg:
    print(f"User: {t.user}, ID: {t.tx_ofx.fitid}, Data: {t.tx_ofx.date}, Desc: {t.tx_ofx.description}, Valor: {t.tx_ofx.amount}")
"""

export_ofx(mrg, data, output)