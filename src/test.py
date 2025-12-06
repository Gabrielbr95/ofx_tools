# test_parse.py
from ofx_tools.loader import load_all_txt, load_all_ofx  
from ofx_tools.merger import merge_transactions
from ofx_tools.exporter import export_ofx
from ofx_tools.namer import populate_user
from ofx_tools.splitter import split_transactions
from pathlib import Path
import csv


def export_all_csv(groups, output_path: Path):
    """
    Gera um único CSV com todas as transações de todos os grupos.
    """
    output_file = output_path / "all_transactions.csv"

    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Cabeçalho
        writer.writerow([
            "acctid",
            "cardFlag",
            "user",
            "date",
            "description",
            "amount",
            "fitid"
        ])

        # Conteúdo
        for group in groups:
            for tx in group.txs_ofx:
                writer.writerow([
                    group.account_id,
                    group.card_flag,
                    getattr(tx, "user", "") or "",
                    tx.date.isoformat(),
                    tx.description,
                    tx.amount,
                    tx.fitid
                ])

    print(f"CSV gerado: {output_file}")


# caminho do arquivo txt para testar
data = Path(__file__).parent.parent / "data"
output = Path(__file__).parent.parent / "output"

#txs = parse_txt_file(str(path))

txs = load_all_txt()
ofx = load_all_ofx(data)
populate_user(ofx, txs)
split_transactions(ofx)
export_all_csv(ofx, output)

