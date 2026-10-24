from dataclasses import dataclass, field, asdict
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone

def now(): return datetime.now(timezone.utc).isoformat()
def money(value):
    if value is None: return None
    s=str(value).strip().replace('€','').replace(' ','')
    if ',' in s: s=s.replace('.','').replace(',','.') if s.rfind(',')>s.rfind('.') else s.replace(',','')
    try:
        d=Decimal(s)
        return str(d) if d.is_finite() and d>=0 else None
    except InvalidOperation: return None

@dataclass
class Offer:
    url: str
    merchant: str
    country: str
    name: str=''
    model: str=''
    ean: str=''
    sku: str=''
    price: str|None=None
    currency: str=''
    stock: str='unknown'
    condition: str='unknown'
    shipping: str|None=None
    fees: str|None=None
    vat_included: bool|None=None
    delivery_nl: bool|None=None
    warranty: str='unknown'
    returns: str='unknown'
    installation: str='unknown'
    old_appliance: str='unknown'
    checked_at: str=field(default_factory=now)
    evidence: dict=field(default_factory=dict)
    coupons: list=field(default_factory=list)
    cashback: list=field(default_factory=list)
    total: str|None=None
    exclusions: list=field(default_factory=list)
    def dict(self): return asdict(self)
