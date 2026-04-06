#!/usr/bin/env python3
import json, os, re, time, requests
from pathlib import Path

WORKER_URL  = os.environ["CF_WORKER_URL"]
AUTH_TOKEN  = os.environ["CF_AUTH_TOKEN"]
INPUT_CID   = os.environ.get("INPUT_CID", "").strip()
DEFAULT_CID = "bafybeifx7yeb55armcsxwwitkymga5xf53dxiarykms3ygqic223w5sk3m"
BATCH_SIZE  = 40   # 低于Worker的45上限，留余量
RETRY_DELAY = 3    # 批次间隔秒数

def load_gateways(path: str):
    text = Path(path).read_text(encoding="utf-8", errors="ignore")
    urls = re.findall(r"https?://[^\s\"'`]+", text)
    clean, seen = [], set()
    for u in urls:
        u = u.strip().rstrip(",];")
        if u and u not in seen:
            seen.add(u); clean.append(u)
    return clean

def probe_batch(gateways, cid, session):
    resp = session.post(
        WORKER_URL,
        json={"gateways": gateways, "cid": cid},
        headers={"X-Auth-Token": AUTH_TOKEN},
        timeout=60,
    )
    resp.raise_for_status()
    return resp.json()

def main():
    # 优先用 gateways.txt，没有则用 gateways.js
    list_file = "gateways.txt" if Path("gateways.txt").exists() else "gateways.js"
    gateways = load_gateways(list_file)
    cid = INPUT_CID or DEFAULT_CID
    print(f"Loaded {len(gateways)} gateways from {list_file}, CID={cid}")

    session = requests.Session()
    session.headers["Content-Type"] = "application/json"

    all_results = []
    batches = [gateways[i:i+BATCH_SIZE] for i in range(0, len(gateways), BATCH_SIZE)]

    for idx, batch in enumerate(batches):
        print(f"Batch {idx+1}/{len(batches)} ({len(batch)} gateways)...")
        try:
            results = probe_batch(batch, cid, session)
            all_results.extend(results)
        except Exception as e:
            print(f"[WARN] Batch {idx+1} failed: {e}")
            # 失败的批次标记为 offline
            all_results.extend([{"base": g, "ok": False} for g in batch])
        if idx < len(batches) - 1:
            time.sleep(RETRY_DELAY)

    # 写在线列表和速度数据
    online = [r for r in all_results if r.get("ok")]
    online.sort(key=lambda r: r.get("latency") or 9999)

    Path("online_gateways.txt").write_text(
        "\n".join(r["base"] for r in online) + "\n", encoding="utf-8"
    )
    speeds = {r["base"]: r["latency"] for r in online if r.get("latency")}
    Path("gateway_speeds.json").write_text(json.dumps(speeds, indent=2), encoding="utf-8")

    print(f"Done: {len(online)}/{len(all_results)} online")

if __name__ == "__main__":
    main()
