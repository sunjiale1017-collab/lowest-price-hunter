"""Import scoped human/browser observations; not a mechanism to invent facts."""
from datetime import datetime,timezone,timedelta
from hunter.models import money
FIELDS={'delivery_nl','vat_included','shipping','fees','warranty','returns','installation','old_appliance'}
def fresh(stamp,hours=4):
    try:
        d=datetime.fromisoformat(stamp);age=datetime.now(timezone.utc)-d
        return timedelta(0)<=age<=timedelta(hours=hours)
    except (ValueError,TypeError):return False

def apply(offers,records):
    rejected=[]
    for r in records:
        if not r.get('source_url','').startswith('https://') or not r.get('quote') or not fresh(r.get('checked_at','')) or r.get('destination_country')!='NL':
            rejected.append({'reason':'Evidence lacks current source, quote or NL destination','record':r});continue
        matches=[o for o in offers if o.url==r.get('offer_url') and (r.get('model')==o.model) and o.currency=='EUR']
        if not matches:rejected.append({'reason':'No exact offer match','record':r});continue
        for o in matches:
            for key,val in r.get('facts',{}).items():
                if key not in FIELDS:continue
                if key in ('shipping','fees'):val=money(val)
                if key in ('delivery_nl','vat_included') and not isinstance(val,bool):continue
                setattr(o,key,val);o.evidence[key]={k:r[k] for k in ('source_url','quote','checked_at','destination_country')}
    return rejected

def attach_promotions(offers,records,kind):
    """Attach dated, offer-specific observations. Grade A is still checked by engine."""
    rejected=[]
    for r in records:
        if not r.get('source_url','').startswith('https://') or not fresh(r.get('checked_at','')) or not r.get('model'):
            rejected.append({'reason':'Promotion lacks current source/model','kind':kind});continue
        for o in offers:
            if r.get('offer_url')==o.url and r['model']==o.model:
                record=dict(r)
                if kind=='coupons':record['url']=o.url
                getattr(o,kind).append(record)
    return rejected
