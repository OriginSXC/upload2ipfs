
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import argparse, csv, re, time, requests
CHECK_HTTP = "https://check-host.net/check-http"
CHECK_RESULT = "https://check-host.net/check-result/{rid}"
DEFAULT_CID = "bafybeifx7yeb55armcsxwwitkymga5xf53dxiarykms3ygqic223w5sk3m"

def parse_urls(path: str):
    url_regex = re.compile(r'https?://[^\s"\'`]+')
    found_urls = []
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
        found_urls = url_regex.findall(text)
    clean, seen = [], set()
    for u in found_urls:
        u = u.strip().rstrip(',').rstrip(']').rstrip(';')
        if u and u not in seen:
            seen.add(u)
            clean.append(u)
    if not clean: raise RuntimeError(f"No http(s) URLs found in input file: {path}")
    return clean

def build_test_url(base: str, cid: str):
    return ("POST", f"{base}{cid}") if "/api/v0/cat" in base else ("GET", f"{base}{cid}")

def start_check(url: str, max_nodes: int) -> dict:
    r = requests.get(CHECK_HTTP, params={"host": url, "max_nodes": max_nodes},
                     headers={"Accept": "application/json"}, timeout=15)
    r.raise_for_status()
    return r.json()

def poll_result(request_id: str, timeout_s: float = 25.0, interval_s: float = 0.8) -> dict:
    t0 = time.time()
    while True:
        r = requests.get(CHECK_RESULT.format(rid=request_id),
                         headers={"Accept": "application/json"}, timeout=15)
        r.raise_for_status()
        data = r.json()
        if data and all(v is not None for v in data.values()): return data
        if time.time() - t0 > timeout_s: return data or {}
        time.sleep(interval_s)

def summarize(node_results: dict):
    total = ready = ok_nodes = 0
    codes, fastest = [], None
    for _, arr in node_results.items():
        total += 1
        if arr is None or not arr: continue
        ready += 1
        entry = arr[0]
        try: success = int(entry[0])
        except: success = 0
        try: t = float(entry[1]) if entry[1] is not None else None
        except: t = None
        code = str(entry[3]) if len(entry) > 3 and entry[3] is not None else ""
        if code: codes.append(code)
        if code or success == 1:
            ok_nodes += 1
            if t is not None: fastest = t if fastest is None else min(fastest, t)
    return {
        "nodes_total": total, "nodes_ready": ready, "nodes_ok": ok_nodes,
        "codes": "|".join(sorted(set(codes))),
        "fastest_s": "" if fastest is None else f"{fastest:.3f}",
        "exists": 1 if ok_nodes > 0 else 0,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input")
    ap.add_argument("--cid", default=DEFAULT_CID)
    ap.add_argument("--nodes", type=int, default=5)
    ap.add_argument("--csv", default="reports/results_checkhost.csv")
    ap.add_argument("--sleep", type=float, default=0.6)
    ap.add_argument("--online-list", help="Output file for online gateways")
    args = ap.parse_args()

    urls = parse_urls(args.input)
    print(f"Found {len(urls)} URLs; probing with {args.nodes} nodes each...")

    results = []
    with open(args.csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["base","method","test_url","exists","nodes_total","nodes_ready","nodes_ok","codes","fastest_s","permanent_link","request_id"])
        for base in urls:
            method, test_url = build_test_url(base, args.cid)
            summary = {}
            try:
                kickoff = start_check(test_url, args.nodes)
                rid = kickoff.get("request_id", ""); perm = kickoff.get("permanent_link", "")
                node_results = poll_result(rid)
                summary = summarize(node_results)
                w.writerow([base, method, test_url, summary["exists"], summary["nodes_total"], summary["nodes_ready"], summary["nodes_ok"], summary["codes"], summary["fastest_s"], perm, rid])
                print(f"[{ 'ONLINE' if summary.get('exists') else 'OFFLINE' }] {base} ok={summary.get('nodes_ok',0)}/{summary.get('nodes_total',0)} codes={summary.get('codes','')}")
            except Exception as e:
                summary = {"exists": 0}
                w.writerow([base, method, test_url, 0, "", "", "", "", "", "", ""])
                print(f"[ERROR] {base} -> {e}")
            results.append((base, summary))
            time.sleep(args.sleep)

    if args.online_list:
        online_gateways = [base for base, summary in results if summary.get("exists") == 1]
        with open(args.online_list, "w", encoding="utf-8") as f:
            for url in online_gateways:
                f.write(f"{url}\n")
        print(f"Saved {len(online_gateways)} online gateways to {args.online_list}")

    print(f"Done. CSV saved to: {args.csv}")

if __name__ == "__main__":
    main()
