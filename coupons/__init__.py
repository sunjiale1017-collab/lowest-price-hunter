def verified_discount(coupon,offer):
    """A record is accepted only with matching offer and actual cart amounts."""
    from decimal import Decimal, InvalidOperation
    from hunter.evidence import fresh
    if coupon.get('grade')!='A' or coupon.get('url')!=offer.url or not coupon.get('cart_evidence') or not fresh(coupon.get('checked_at','')):return Decimal(0)
    if not coupon.get('eligibility_confirmed') or coupon.get('currency')!=offer.currency:return Decimal(0)
    try:
        before=Decimal(str(coupon['before']));after=Decimal(str(coupon['after']))
        expected=Decimal(offer.price)+Decimal(offer.shipping)+Decimal(offer.fees)
        if not before.is_finite() or not after.is_finite() or before!=expected:return Decimal(0)
    except (KeyError,ValueError,TypeError,InvalidOperation):return Decimal(0)
    return max(Decimal(0),before-after) if before>=after>=0 else Decimal(0)
