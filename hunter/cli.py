import argparse,json,logging
from hunter.http import Client
from scrapers.html_adapter import parse
from scrapers.feed import parse_feed
from hunter.discovery import discover
from hunter.evidence import apply,attach_promotions
from price_engine import rank
from hunter.report import write
from hunter.models import now
from coupons.search import collect

def main():
    p=argparse.ArgumentParser();p.add_argument('--config',default='config/aeg.json');p.add_argument('--out',default='reports/live');a=p.parse_args()
    logging.basicConfig(level=logging.INFO,format='%(levelname)s %(message)s')
    cfg=json.load(open(a.config));client=Client();offers=[];failures=[];leads=[]
    for s in cfg['sources']:
        logging.info('Collecting %s',s['url'])
        try:
            urls=discover(client,s,cfg['model']) if s.get('search_url') else [s['url']]
            if not urls: failures.append({'url':s.get('search_url'),'reason':'No exact-model candidate links; coverage gap'})
            for url in urls:
                item={**s,'url':url}
                result=(parse_feed if s.get('adapter')=='feed' else parse)(client.get(url),item,cfg['model']);offers+=result
            if not urls or not result:failures.append({'url':s['url'],'reason':'No matching nonaggregate JSON-LD offer','checked_at':now()})
        except Exception as e:failures.append({'url':s['url'],'reason':str(e),'checked_at':now()})
    for s in cfg.get('research_sources',[]):
        logging.info('Checking lead %s',s['url'])
        try:
            leads.append(collect(client,s))
        except Exception as e:failures.append({**s,'reason':str(e),'checked_at':now()})
    failures+=apply(offers,cfg.get('evidence',[]))
    failures+=attach_promotions(offers,cfg.get('coupons',[]),'coupons')
    failures+=attach_promotions(offers,cfg.get('cashback',[]),'cashback')
    data=write(rank(offers),failures,leads,a.out)
    print(json.dumps({'offers':len(offers),'verified':len(data['verified_ranking']),'failures':len(failures),'output':a.out}))
if __name__=='__main__':main()
