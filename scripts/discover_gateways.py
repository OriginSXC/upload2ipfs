#!/usr/bin/env python3
import re
from pathlib import Path
from urllib.parse import urlparse
import requests

OUTPUT = Path("gateways.txt")
API_SUFFIX = "/api/v0/cat?arg="
IPFS_SUFFIX = "/ipfs/"
USER_AGENT = "upload2ipfs-gateway-discovery"
# 只用专门的网关列表；从 README/文档网页里正则抓 URL 会把项目官网、GitHub 等普通网站误当成网关
SOURCES = [
    "https://raw.githubusercontent.com/ipfs/public-gateway-checker/main/gateways.json",
    "https://ipfs.github.io/public-gateway-checker/gateways.json",
]
HOST_RE = re.compile(r"^[A-Za-z0-9.-]+(:\d+)?$")

def normalize_gateway(url: str):
    u = url.strip().strip("'\"`),.;")
    if not u.startswith(("http://", "https://")):
        return None
    parsed = urlparse(u)
    if not parsed.netloc or not HOST_RE.match(parsed.netloc):
        return None
    api_idx = u.find(API_SUFFIX)
    if api_idx != -1:
        return u[: api_idx + len(API_SUFFIX)]
    ipfs_idx = u.find(IPFS_SUFFIX)
    if ipfs_idx != -1:
        return u[: ipfs_idx + len(IPFS_SUFFIX)]
    if u.endswith("/ipfs"):
        return f"{u}/"
    if parsed.path in ("", "/"):
        return f"{parsed.scheme}://{parsed.netloc}/ipfs/"
    return None

def extract_gateways(text: str):
    found = set()
    for raw in re.findall(r"https?://[^\s\"'`<>\\]+", text):
        normalized = normalize_gateway(raw)
        if normalized:
            found.add(normalized)
    return found

existing = set()
if OUTPUT.exists():
    for line in OUTPUT.read_text(encoding="utf-8").splitlines():
        normalized = normalize_gateway(line)
        if normalized:
            existing.add(normalized)

discovered = set()
session = requests.Session()
session.headers.update({"User-Agent": USER_AGENT})
for source in SOURCES:
    try:
        resp = session.get(source, timeout=20)
        if resp.ok:
            discovered.update(extract_gateways(resp.text))
        else:
            print(f"[WARN] {source} -> HTTP {resp.status_code}")
    except Exception as exc:
        print(f"[WARN] {source} -> {type(exc).__name__}: {exc}")

merged = sorted(existing | discovered)
OUTPUT.write_text("\n".join(merged) + ("\n" if merged else ""), encoding="utf-8")
print(f"existing={len(existing)} discovered={len(discovered)} merged={len(merged)}")
