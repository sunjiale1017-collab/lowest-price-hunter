import json,re
from html.parser import HTMLParser
from hunter.models import Offer,money
class LDParser(HTMLParser):
    def __init__(self): super().__init__();self.active=False;self.parts=[];self.current=''
    def handle_starttag(self,tag,attrs):
        if tag=='script' and dict(attrs).get('type','').lower()=='application/ld+json':self.active=True;self.current=''
    def handle_data(self,data):
        if self.active:self.current+=data
    def handle_endtag(self,tag):
        if tag=='script' and self.active:self.parts.append(self.current);self.active=False

def nodes(obj):
    if isinstance(obj,dict):
        yield obj
        for val in obj.values():yield from nodes(val)
    elif isinstance(obj,list):
        for val in obj:yield from nodes(val)

def parse(body,source,query):
    parser=LDParser();parser.feed(body);out=[]
    for block in parser.parts:
        try: data=json.loads(block)
        except ValueError:continue
        for p in nodes(data):
            types=p.get('@type',[]);types=[types] if isinstance(types,str) else types
            if 'Product' not in types:continue
            name=str(p.get('name',''));model=str(p.get('model') or p.get('mpn') or '')
            ean=str(p.get('gtin13') or p.get('gtin') or '');sku=str(p.get('sku') or '')
            # Token boundary prevents TR738AT2B matching TR738AT2B-variant.
            exact=(query.casefold()==model.casefold() or query==ean or re.search(r'(?<![\w-])'+re.escape(query)+r'(?![\w-])',name,re.I))
            if not exact:continue
            offers=p.get('offers',[]);offers=offers if isinstance(offers,list) else [offers]
            for v in offers:
                if not isinstance(v,dict) or v.get('@type')=='AggregateOffer':continue
                o=Offer(source['url'],source['merchant'],source['country'],name,model or query,ean,sku)
                o.price=money(v.get('price'));o.currency=v.get('priceCurrency','')
                status=str(v.get('availability','')).split('/')[-1]
                o.stock={'InStock':'in_stock','OutOfStock':'out_of_stock','PreOrder':'preorder','InStoreOnly':'store_only','SoldOut':'out_of_stock','Discontinued':'out_of_stock'}.get(status,'unknown')
                o.condition=str(v.get('itemCondition') or p.get('itemCondition') or 'unknown').split('/')[-1]
                o.evidence={'product':{'url':source['url'],'checked_at':o.checked_at,'method':'JSON-LD Product/Offer','availability':status},'identity':{'name':name,'model':model,'ean':ean,'sku':sku}}
                # Shipping/VAT/service facts require separately reviewed evidence, never country inference.
                out.append(o)
    return out
