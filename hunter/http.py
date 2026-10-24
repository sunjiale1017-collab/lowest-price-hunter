import urllib.request, urllib.error, urllib.robotparser, urllib.parse, time, logging, ipaddress, socket
UA='LowestPriceHunter/0.1 (+public price research; no purchases)'
class Blocked(Exception): pass
class Client:
    def __init__(self,delay=2,retries=2):
        self.delay=max(2,delay);self.retries=min(3,retries);self.last={};self.robots={}
    def safe(self,url):
        p=urllib.parse.urlsplit(url)
        if p.scheme!='https' or not p.hostname or p.username or p.password: raise Blocked('Only public HTTPS without credentials allowed')
        if p.hostname in ('localhost',) or p.hostname.endswith(('.local','.internal')): raise Blocked('Nonpublic destination')
        try:
            if not ipaddress.ip_address(p.hostname).is_global: raise Blocked('Nonpublic destination')
        except ValueError: pass
        # DNS may be resolved by the environment HTTP proxy. This CLI is not a public URL-fetch service.
        return p
    def raw(self,url):
        self.safe(url)
        # Redirects must be explicit so every destination gets a robots check.
        class NoRedirect(urllib.request.HTTPRedirectHandler):
            def redirect_request(self,*args): return None
        opener=urllib.request.build_opener(NoRedirect)
        req=urllib.request.Request(url,headers={'User-Agent':UA,'Accept':'text/html,application/json,application/xml'})
        with opener.open(req,timeout=12) as r:
            data=r.read(5_000_001)
            if len(data)>5_000_000: raise Blocked('Response too large')
            return data.decode(r.headers.get_content_charset() or 'utf-8',errors='replace')
    def get(self,url):
        p=self.safe(url); origin=f'{p.scheme}://{p.netloc}'
        if origin not in self.robots:
            rp=urllib.robotparser.RobotFileParser()
            try: rp.parse(self.raw(origin+'/robots.txt').splitlines())
            except urllib.error.HTTPError as e:
                if e.code==404: rp.parse([])
                else: raise Blocked('robots unavailable: '+str(e.code))
            except Exception as e: raise Blocked('robots unavailable: '+str(e))
            self.robots[origin]=rp
        rp=self.robots[origin]
        if not rp.can_fetch(UA,url): raise Blocked('robots disallow')
        delay=max(self.delay,rp.crawl_delay(UA) or 0)
        for attempt in range(self.retries+1):
            time.sleep(max(0,delay-(time.monotonic()-self.last.get(origin,0))))
            self.last[origin]=time.monotonic()
            try:
                body=self.raw(url)
                if any(x in body.lower() for x in ['verify you are human','cf-chl-','g-recaptcha','access denied','captcha challenge']): raise Blocked('Access challenge; source stopped')
                return body
            except urllib.error.HTTPError as e:
                if e.code<500 or attempt==self.retries: raise Blocked('HTTP '+str(e.code))
            except (TimeoutError,OSError) as e:
                if attempt==self.retries: raise Blocked(str(e))
            logging.warning('Retry %s attempt %s',url,attempt+1)
