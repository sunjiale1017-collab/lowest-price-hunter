import json,csv,html,sqlite3
from pathlib import Path
from hunter.models import now
from cashback import potential_net

def write(offers,failures,leads,directory,requested_model=None):
    path=Path(directory);path.mkdir(parents=True,exist_ok=True)
    serialize=lambda o: {**o.dict(),'potential_net_if_cashback_approved':potential_net(o.total,o.cashback)}
    data={'generated_at':now(),'requested_model':requested_model,'verified_ranking':[serialize(o) for o in offers if o.total is not None][:10],'unverified_offers':[serialize(o) for o in offers if o.total is None],'failures':failures,'leads':leads,'monitoring_deployed':False}
    (path/'report.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
    with (path/'report.csv').open('w',newline='') as f:
        fields=['model','ean','sku','merchant','country','condition','stock','price','currency','shipping','total','url','checked_at','exclusions'];w=csv.DictWriter(f,fieldnames=fields,extrasaction='ignore');w.writeheader();w.writerows(o.dict() for o in offers)
    esc=lambda x:html.escape(str(x))
    rows=''.join('<tr>'+''.join('<td>'+esc(x)+'</td>' for x in [o.merchant,o.model,o.price,o.stock,o.shipping,o.total or 'UNVERIFIED','; '.join(o.exclusions),o.url])+'</tr>' for o in offers)
    (path/'report.html').write_text('<!doctype html><meta charset="utf-8"><title>Lowest Price Hunter</title><style>body{font:16px system-ui;margin:32px;background:#f6f8fa}td,th{padding:12px;border-bottom:1px solid #ddd}table{background:white}pre{white-space:pre-wrap}</style><h1>Lowest Price Hunter</h1><p>'+esc(data['generated_at'])+' · EUR · NL destination · Cashback excluded</p><h2>Verified lowest price: '+(esc(offers[0].total) if offers and offers[0].total is not None else 'NO VERIFIED DATA')+'</h2><table><tr><th>Merchant<th>Model<th>Price<th>Stock<th>Shipping<th>Total<th>Missing evidence<th>Source</tr>'+rows+'</table><h2>Failures and leads</h2><pre>'+esc(json.dumps({'failures':failures,'leads':leads},ensure_ascii=False,indent=2))+'</pre>')
    with sqlite3.connect(path/'history.sqlite') as db:
        db.execute('CREATE TABLE IF NOT EXISTS runs (generated_at TEXT,offers INTEGER,verified INTEGER,failures TEXT)')
        db.execute('INSERT INTO runs VALUES (?,?,?,?)',(data['generated_at'],len(offers),len(data['verified_ranking']),json.dumps(failures)))
        db.execute('CREATE TABLE IF NOT EXISTS prices (checked_at TEXT,url TEXT,model TEXT,price TEXT,total TEXT,currency TEXT,stock TEXT)')
        db.executemany('INSERT INTO prices VALUES (?,?,?,?,?,?,?)',[(o.checked_at,o.url,o.model,o.price,o.total,o.currency,o.stock) for o in offers])
    return data
