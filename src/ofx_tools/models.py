from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import List, Optional

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
    account_id: str
    user: Optional[str] = None

@dataclass
class MergedTransaction:
    tx_ofx: TransactionOfx
    user: str 

@dataclass
class TransactionGroup:
    account_id: str 
    card_flag: str 
    base_ofx: Path
    txs_ofx: List[TransactionOfx]
    user: Optional[str] = None     # default por último