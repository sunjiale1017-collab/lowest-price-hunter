from decimal import Decimal
from coupons import verified_discount
from stock_checker import eligible

def rank(offers):
    unique={}
    for o in offers:
        key=(o.merchant,o.url,o.sku,o.ean,o.condition)
        unique[key]=o
    out=list(unique.values())
    for o in out:
        o.exclusions=eligible(o)
        if not o.exclusions:
            # Only one coupon unless a single cart evidence demonstrates full stack.
            discount=max([verified_discount(c,o) for c in o.coupons] or [Decimal(0)])
            o.total=str(max(Decimal(0),Decimal(o.price)+Decimal(o.shipping)+Decimal(o.fees)-discount))
        else:o.total=None
    return sorted(out,key=lambda o:(o.total is None,Decimal(o.total or 'Infinity'),o.url))
