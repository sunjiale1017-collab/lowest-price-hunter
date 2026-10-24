"""Retrieve public promotion clues; extraction never means coupon validity."""
import re
from hunter.models import now
from scrapers.html_adapter import visible
KEYS=re.compile(r'coupon|voucher|gutschein|korting|newsletter|nieuwsbrief|member|student|cashback|gratis|free shipping',re.I)
def collect(client,source):
    text=visible(client.get(source['url']))
    snippets=[]
    for m in KEYS.finditer(text):
        snippet=text[max(0,m.start()-80):m.end()+220]
        if snippet not in snippets:snippets.append(snippet)
        if len(snippets)==12:break
    # Codes in context are candidates, including the word 'verified' on coupon websites.
    codes=[]
    for snippet in snippets:
        for code in re.findall(r'(?:code|kortingscode|gutschein)\s*[:=]\s*([A-Z][A-Z0-9-]{4,24})\b',snippet):
            if code not in codes:codes.append(code)
    return {**source,'checked_at':now(),'status':'public lead only; eligibility/expiry/stack/cart unverified','grade':'B' if source['kind']=='official' else 'C','code_candidates':codes,'matching_lines':snippets,'cart_tested':False}
