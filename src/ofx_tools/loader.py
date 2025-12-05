from pathlib import Path
from .parser_txt import parse_txt_file
from .parser_ofx import parse_ofx_file

def load_all_txt(data_dir=None):
    """
    Percorre todos os arquivos .txt da pasta data e retorna uma lista de todas as transações.
    """
    if data_dir is None:
        data_dir = Path(__file__).parent.parent.parent / "data"
    
    all_txs = []
    for file_path in data_dir.glob("*.txt"):
        txs = parse_txt_file(file_path)
        all_txs.extend(txs)

    return all_txs

def load_all_ofx(data_dir=None):
    if data_dir is None:
        data_dir = Path(__file__).parent.parent.parent / "data"
    
    all_txs = []
    acctid_map = {}
    for file_path in data_dir.glob("*.ofx"):
        txs = parse_ofx_file(file_path)
        all_txs.extend(txs)
    
        # registra path de base usando apenas o ACCTID da primeira transação
        first_tx = txs[0]
        acctid = first_tx.account_id
        if acctid not in acctid_map:
            acctid_map[acctid] = file_path

    return all_txs, acctid_map