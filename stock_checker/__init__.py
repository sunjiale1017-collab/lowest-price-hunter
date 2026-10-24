def eligible(offer):
    reasons=[]
    if offer.stock!='in_stock':reasons.append('Stock not confirmed in stock')
    if offer.delivery_nl is not True:reasons.append('NL delivery unverified')
    if offer.shipping is None:reasons.append('Shipping unknown')
    if offer.fees is None:reasons.append('Mandatory fees unknown')
    if offer.vat_included is not True:reasons.append('Destination VAT unverified')
    if offer.currency!='EUR':reasons.append('Not EUR')
    if offer.price is None:reasons.append('Price missing')
    if offer.condition=='unknown':reasons.append('Condition unknown')
    return reasons
