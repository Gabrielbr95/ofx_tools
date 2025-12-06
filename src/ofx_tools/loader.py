from pathlib import Path
from .parser_txt import parse_txt_file
from .parser_ofx import parse_ofx_file
from .models import TransactionGroup, TransactionOfx
from ofxtools.Parser import OFXTree
from typing import List, Dict

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


CARD_FLAG_MAP = {
    "4984000000005460": "visa",
    "6550000000007799": "elo",
}

def load_all_ofx(folder: Path) -> List[TransactionGroup]:
    """
    Lê todos os arquivos OFX no diretório e retorna uma lista de TransactionList,
    agrupando as transações por acctid.
    """

    groups: Dict[str, TransactionGroup] = {}

    # percorre arquivos OFX
    for file_path in sorted(folder.glob("*.ofx")):
        txs = parse_ofx_file(file_path)
        if not txs:
            continue

        # acctid obtido da primeira transação (todas no arquivo têm o mesmo)
        acctid = txs[0].account_id

        # obtém bandeira do cartão
        card_flag = CARD_FLAG_MAP.get(acctid, "UNKNOWN")

        # cria grupo caso ainda não exista
        if acctid not in groups:
            groups[acctid] = TransactionGroup(
                user="",             # será definido depois
                account_id=acctid,
                card_flag=card_flag,
                txs_ofx=[],              # inicia vazio; vamos estender
                base_ofx=file_path
            )

        # adiciona transações ao grupo existente
        groups[acctid].txs_ofx.extend(txs)

    return list(groups.values())