def potential_net(total,records):
    """Only explicit compatibility and eligibility can produce potential net cost."""
    from decimal import Decimal
    valid=[r for r in records if r.get('eligible') is True and r.get('compatible') is True and r.get('terms_url') and r.get('amount') is not None]
    if total is None or not valid:return None
    # Do not silently stack separate cashback schemes.
    return str(max(Decimal(0),Decimal(total)-max(Decimal(str(r['amount'])) for r in valid)))
