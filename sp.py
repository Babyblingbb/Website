#!/usr/bin/env python3
"""Baby Bling Shopify helper. Mints a 24h Admin token via client-credentials
and caches it, so no token ever has to be pasted by hand again."""
import json, os, time, urllib.request, urllib.parse, sys

SHOP      = "ws0twk-ww.myshopify.com"
CLIENT_ID = "6ee2a57fe749e56dd8b7c76105470ef5"
SECRET    = "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"
API       = "2025-01"
CACHE     = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".shopify_token.json")

def token():
    if os.path.exists(CACHE):
        c = json.load(open(CACHE))
        if c.get("expires_at", 0) - 60 > time.time():
            return c["access_token"]
    body = urllib.parse.urlencode({
        "grant_type": "client_credentials",
        "client_id": CLIENT_ID, "client_secret": SECRET}).encode()
    req = urllib.request.Request(f"https://{SHOP}/admin/oauth/access_token", data=body,
        headers={"Content-Type": "application/x-www-form-urlencoded"})
    try:
        d = json.loads(urllib.request.urlopen(req, timeout=30).read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", "ignore")
        msg = "app_not_installed" if "app_not_installed" in body else body[:200]
        raise SystemExit(f"token request failed ({e.code}): {msg}")
    d["expires_at"] = time.time() + d.get("expires_in", 86399)
    json.dump(d, open(CACHE, "w"))
    return d["access_token"]

def call(method, path, payload=None, api=None):
    url = f"https://{SHOP}/admin/api/{api or API}/{path.lstrip('/')}"
    data = json.dumps(payload).encode() if payload is not None else None
    req = urllib.request.Request(url, data=data, method=method,
        headers={"X-Shopify-Access-Token": token(), "Content-Type": "application/json"})
    try:
        r = urllib.request.urlopen(req, timeout=60)
        return json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:
        return {"_error": e.code, "_body": e.read().decode("utf-8", "ignore")[:400]}

def gql(query, variables=None):
    return call("POST", "graphql.json", {"query": query, "variables": variables or {}})

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "scopes":
        t = token()
        req = urllib.request.Request(f"https://{SHOP}/admin/oauth/access_scopes.json",
            headers={"X-Shopify-Access-Token": t})
        d = json.loads(urllib.request.urlopen(req, timeout=30).read())
        s = sorted(x["handle"] for x in d["access_scopes"])
        print(f"token ok ({len(s)} scopes):")
        for x in s: print("  ", x)
    else:
        print(json.dumps(call("GET", "shop.json"), indent=1)[:400])
