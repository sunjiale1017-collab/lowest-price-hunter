"""HTML microdata and merchant-scoped safeguards. No site-wide stock inference."""
from html.parser import HTMLParser
from .structured import parse as structured
class Visible(HTMLParser):
    def __init__(self):super().__init__();self.skip=0;self.text=[]
    def handle_starttag(self,t,a):
        if t in ('script','style'):self.skip+=1
    def handle_endtag(self,t):
        if t in ('script','style'):self.skip=max(0,self.skip-1)
    def handle_data(self,d):
        if not self.skip:self.text.append(d.strip())
def visible(body):
    p=Visible();p.feed(body);return ' '.join(p.text)

def parse(body,source,query):
    offers=structured(body,source,query)
    text=visible(body)
    # Stop at first related-products section: never borrow stock/price from another card.
    markers=['Anderen vonden','Anderen bekeken','Gerelateerde producten','Accessoires']
    start=text.casefold().find(query.casefold())
    scoped=text[start:] if start>=0 else text
    for marker in markers:scoped=scoped.split(marker)[0]
    for o in offers:
        if 'Nooit meer leverbaar' in scoped:o.stock='out_of_stock';o.evidence['stock_override']='Nooit meer leverbaar in main product section'
        if 'Showroommodel' in scoped:o.condition='Showroom';o.evidence['condition_override']='Showroommodel in main product section'
    return offers
