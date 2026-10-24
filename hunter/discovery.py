from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,quote
class Links(HTMLParser):
    def __init__(self):super().__init__();self.urls=[]
    def handle_starttag(self,t,a):
        if t=='a' and dict(a).get('href'):self.urls.append(dict(a)['href'])
def discover(client,source,model):
    url=source['search_url'].replace('{query}',quote(model));body=client.get(url);p=Links();p.feed(body)
    links=[];host=urlsplit(url).hostname
    for u in p.urls:
        full=urljoin(url,u)
        if urlsplit(full).hostname==host and model.casefold() in full.casefold() and full!=url and full not in links:links.append(full)
    return links[:3]
