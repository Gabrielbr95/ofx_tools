import re
from .models import TransactionText
from datetime import datetime

USER_MAP = {
    "1": "gabriel",
    "2": "carol"
}

def parse_txt_file(path):
    if not str(path).lower().endswith(".txt"):
        return []  # ignora silenciosamente
    
    user = None
    txs = []

    with open(path, "r", encoding="latin1") as f:
        lines = f.readlines()

    for line in lines:
        line = line.strip()

        # detecta cabeçalho de número de usuário
        m_user = re.match(r"^(\d) - ", line)
        if m_user:
            user = USER_MAP.get(m_user.group(1))
            continue

        # detecta transações (exemplo genérico)
        m_tx = re.match(r"(\d{2}\.\d{2}\.\d{4})(.+?)\s+(-?\d[\d\.]*,\d{2})", line)
        if m_tx and user:
            date, desc, value = m_tx.groups()
            value = float(value.replace(".", "").replace(",", "."))
            date_obj = datetime.strptime(date, "%d.%m.%Y").date()
            txs.append(TransactionText(date_obj, desc, value, user))

    return txs