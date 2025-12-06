from datetime import date
from collections import defaultdict
from datetime import date
from copy import deepcopy
from .models import TransactionOfx


def is_previous_month(ref_date: date, test_date: date) -> bool:
    if ref_date.year == test_date.year:
        return test_date.month == ref_date.month - 1
    # caso ref seja janeiro
    return ref_date.month == 1 and test_date.year == ref_date.year - 1 and test_date.month == 12

def clone_tx(tx):
    """Clona uma TransactionOfx sem copiar o raw (ofxtools)."""
    return TransactionOfx(
        fitid=tx.fitid,
        date=tx.date,
        description=tx.description,
        amount=tx.amount,
        raw=tx.raw,              # mesma referência, mas não causa problema
        account_id=tx.account_id,
        user=tx.user
    )

def split_transactions(groups):
    for group in groups:
        txs = group.txs_ofx

        # 1. Coletar todas as transações DEBITO CONTA
        debit_txs = [
            tx for tx in txs
            if "DEBITO CONTA" in tx.description.upper()
        ]
        print (debit_txs)
        if not debit_txs:
            print ("no debit")
            continue

        # 2. Para cada DEBITO CONTA encontrado
        for debit_tx in debit_txs:
            ref_date = debit_tx.date

            # Somatório de gastos do mês anterior por usuário
            totals = defaultdict(float)

            for tx in txs:
                user = getattr(tx, "user", None)

                # considerar None como um usuário válido
                # ignorar somente Gabriel (ele será ajustado no final)
                if user == "Gabriel":
                    continue

                if is_previous_month(ref_date, tx.date) and tx.amount < 0:
                    totals[user] += tx.amount

            if not totals:
                continue

            # 3. Criar novas transações por usuário
            new_txs = []
            for user, total in totals.items():

                # criar clone da transação
                new_tx = clone_tx(debit_tx)
                new_tx.user = user
                new_tx.amount = total  # negativo
                new_tx.description = debit_tx.description + f" ({user})"
                new_tx.fitid = debit_tx.fitid + f"_{user}"

                new_txs.append(new_tx)

            # 4. Ajustar valor do débito original do Gabriel
            total_all = sum(totals.values())  # soma negativa
            debit_tx.amount -= total_all      # remove a parte dos outros usuários

            # 5. Adicionar as novas transações ao grupo
            txs.extend(new_txs)