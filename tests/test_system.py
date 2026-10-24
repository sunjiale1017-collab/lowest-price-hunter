import unittest,json,tempfile,sqlite3
from pathlib import Path
from unittest.mock import patch
from decimal import Decimal
from hunter.models import Offer,money,now
from hunter.http import Client,Blocked
from hunter.evidence import apply
from scrapers import parse
from scrapers.html_adapter import parse as htmlparse
from scrapers.feed import parse_feed
from price_engine import rank
from hunter.report import write
from cashback import potential_net
S={'url':'https://example.com/dryer','merchant':'Fixture merchant','country':'NL'}
def page(**kw):
    p={'@type':'Product','name':'AEG TEST123','model':'TEST123','gtin13':'1234567890123','offers':{'@type':'Offer','price':'599.99','priceCurrency':'EUR','availability':'https://schema.org/InStock','itemCondition':'https://schema.org/NewCondition'}};p.update(kw)
    return '<script type="application/ld+json">'+json.dumps(p)+'</script>'
def ready():
    return Offer(**S,name='TEST123',model='TEST123',price='600',currency='EUR',stock='in_stock',condition='NewCondition',shipping='20',fees='0',vat_included=True,delivery_nl=True)
class Tests(unittest.TestCase):
    def test_price_locales(self):
        self.assertEqual(money('1.234,56'),'1234.56');self.assertEqual(money('1234.56'),'1234.56');self.assertIsNone(money('NaN'));self.assertIsNone(money('-2'))
    def test_product_identity(self):
        o=parse(page(),S,'TEST123')[0];self.assertEqual(o.ean,'1234567890123');self.assertEqual(o.price,'599.99')
    def test_variant_rejected(self):self.assertEqual(parse(page(name='TEST123-X',model='TEST123-X'),S,'TEST123'),[])
    def test_aggregate_rejected(self):self.assertEqual(parse(page(offers={'@type':'AggregateOffer','lowPrice':'1'}),S,'TEST123'),[])
    def test_unknown_cost_excluded(self):
        o=ready();o.shipping=None;self.assertIsNone(rank([o])[0].total)
    def test_crossborder_not_assumed(self):
        o=ready();o.country='DE';o.delivery_nl=None;self.assertIsNone(rank([o])[0].total)
    def test_stock_excluded(self):
        for v in ('unknown','out_of_stock','preorder','store_only'):
            o=ready();o.stock=v;self.assertIsNone(rank([o])[0].total)
    def test_coupon_unverified_not_deducted(self):
        o=ready();o.coupons=[{'grade':'B','amount':'100'}];self.assertEqual(rank([o])[0].total,'620')
    def test_coupon_cart_required(self):
        o=ready();o.coupons=[{'grade':'A','url':o.url,'cart_evidence':'record','checked_at':now(),'currency':'EUR','eligibility_confirmed':True,'before':'620','after':'600'}];self.assertEqual(rank([o])[0].total,'600')
    def test_cashback_separate(self):
        o=ready();o.cashback=[{'amount':'100','eligible':True,'compatible':True,'terms_url':'https://example.com/terms'}];self.assertEqual(rank([o])[0].total,'620');self.assertEqual(potential_net(o.total,o.cashback),'520')
    def test_dedup(self):self.assertEqual(len(rank([ready(),ready()])),1)
    def test_html_stock_scope(self):
        o=htmlparse(page()+'<h1>Nooit meer leverbaar</h1><h2>Accessoires</h2><p>Op voorraad</p>',S,'TEST123')[0];self.assertEqual(o.stock,'out_of_stock')
    def test_showroom(self):self.assertEqual(htmlparse(page()+'<p>Showroommodel</p>',S,'TEST123')[0].condition,'Showroom')
    def test_feed(self):self.assertEqual(len(parse_feed(json.dumps([{'url':S['url'],'model':'TEST123','price':'12'}]),{**S,'format':'json'},'TEST123')),1)
    def test_stale_evidence(self):
        o=ready();self.assertTrue(apply([o],[{'source_url':S['url'],'quote':'x','checked_at':'2020-01-01T00:00:00+00:00','destination_country':'NL'}]))
    def test_evidence_applies(self):
        o=ready();o.shipping=None;self.assertEqual(apply([o],[{'source_url':S['url'],'offer_url':o.url,'model':o.model,'quote':'Shipping 20 EUR to NL','checked_at':now(),'destination_country':'NL','facts':{'shipping':'20'}}]),[]);self.assertEqual(o.shipping,'20')
    def test_reports_and_history(self):
        with tempfile.TemporaryDirectory() as d:
            data=write(rank([ready()]),[],[],d);self.assertEqual(len(data['verified_ranking']),1)
            for f in ('report.json','report.csv','report.html','history.sqlite'):self.assertTrue((Path(d)/f).exists())
            with sqlite3.connect(Path(d)/'history.sqlite') as db:self.assertEqual(db.execute('select count(*) from prices').fetchone()[0],1)
    def test_private_url_rejected(self):
        for u in ('http://example.com','https://127.0.0.1/','https://localhost/','https://user:pass@example.com'):
            with self.assertRaises(Blocked):Client().safe(u)
    def test_robots_denied(self):
        c=Client()
        with patch.object(c,'raw',return_value='User-agent: *\nDisallow: /'):
            with self.assertRaises(Blocked):c.get(S['url'])
    def test_challenge_stops(self):
        c=Client()
        with patch.object(c,'raw',side_effect=['User-agent: *\nAllow: /','verify you are human']):
            with self.assertRaises(Blocked):c.get(S['url'])
    def test_bad_coupon_amount_rejected(self):
        o=ready();o.coupons=[{'grade':'A','url':o.url,'cart_evidence':'record','checked_at':now(),'currency':'EUR','eligibility_confirmed':True,'before':'bad','after':'1'}];self.assertEqual(rank([o])[0].total,'620')
    def test_old_coupon_rejected(self):
        o=ready();o.coupons=[{'grade':'A','url':o.url,'cart_evidence':'record','checked_at':'2020-01-01T00:00:00+00:00','currency':'EUR','eligibility_confirmed':True,'before':'620','after':'1'}];self.assertEqual(rank([o])[0].total,'620')
    def test_coupon_wrong_cart_base_rejected(self):
        o=ready();o.coupons=[{'grade':'A','url':o.url,'cart_evidence':'record','checked_at':now(),'currency':'EUR','eligibility_confirmed':True,'before':'999','after':'1'}];self.assertEqual(rank([o])[0].total,'620')
    def test_rank_by_final_not_sticker(self):
        a=ready();b=ready();b.url+='2';b.price='590';b.shipping='50';self.assertEqual(rank([b,a])[0].total,'620')
    def test_cashback_requires_compatibility(self):
        self.assertIsNone(potential_net('620',[{'amount':'100','eligible':True,'terms_url':'https://example.com/terms'}]))
if __name__=='__main__':unittest.main()
