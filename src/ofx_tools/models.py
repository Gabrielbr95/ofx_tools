from dataclasses import dataclass
from datetime import date

@dataclass
class TransactionText:
    date: date
    description: str
    amount: float
    user: str

@dataclass
class TransactionOfx:
    fitid: str
    date: date
    description: str
    amount: float
    raw: any  # aponta para o objeto ofxtools original
    account_id: any

@dataclass
class MergedTransaction:
    tx_ofx: TransactionOfx
    user: str | None
