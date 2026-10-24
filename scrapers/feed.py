"""Explicit public merchant feeds only. Never guess missing fulfillment fields."""
import csv,io,json
from hunter.models import Offer,money

def parse_feed(body,source,query):
    rows=json.loads(body) if source.get('format')=='json' else list(csv.DictReader(io.StringIO(body)))
    out=[]
    for r in rows:
        if query.casefold() not in (str(r.get('model','')).casefold(),str(r.get('ean','')).casefold()):continue
        o=Offer(r['url'],source['merchant'],source['country'],str(r.get('name','')),str(r.get('model','')),str(r.get('ean','')),str(r.get('sku','')))
        o.price=money(r.get('price'));o.currency=r.get('currency','');o.stock=r.get('stock','unknown');o.condition=r.get('condition','unknown')
        o.evidence={'product':{'url':source['url'],'checked_at':o.checked_at,'method':'public merchant feed'}};out.append(o)
    return out
