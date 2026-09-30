#!/usr/bin/env python3
"""Sync the crypto store's catalog from the Burmese store's exported data.

WHY THIS EXISTS: export_en.py reuses export_catalog.py, which imports the
live ebook-bot module — and that module takes an fcntl singleton lock at
import time. While the live bot is running, export_en.py cannot run
("another ebook-bot is already running"). Rather than stopping the
money-handling bot, this script copies the Burmese store's already-exported
dist/data (exported when the bot was down) and rewrites only what differs
for the crypto edition:

  - price: 3000 MMK -> 1 (flat $1 USD per set)
  - buy_url / meta bot: musebookfinder_bot -> leoebookcollection_bot
  - meta price_mmk -> 1 (in this store the field means the main currency
    unit, i.e. USD)

Everything else — set ids (pids), names, series, components, file lists,
sizes, cats.json, covers.json, manual_covers/ — is copied verbatim, so the
catalog is identical to the Burmese store.

Usage: python3 sync_from_mm.py
"""
import json
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
MM_DATA = os.path.normpath(os.path.join(HERE, "..", "..", "ebook-store",
                                        "dist", "data"))
OUT_DATA = os.path.normpath(os.path.join(HERE, "..", "dist", "data"))

BOT_USERNAME = "leoebookcollection_bot"


def buy_url(pid):
    return "https://t.me/" + BOT_USERNAME + "?start=buy_" + pid


def main():
    os.makedirs(os.path.join(OUT_DATA, "sets"), exist_ok=True)

    # --- sets.json (compact list) ---
    with open(os.path.join(MM_DATA, "sets.json"), encoding="utf-8") as f:
        sets_doc = json.load(f)
    for s in sets_doc.get("sets", []):
        s["price"] = 1
    sets_doc["meta"]["price_mmk"] = 1
    sets_doc["meta"]["bot"] = BOT_USERNAME
    with open(os.path.join(OUT_DATA, "sets.json"), "w",
              encoding="utf-8") as f:
        json.dump(sets_doc, f, ensure_ascii=False)

    # --- home.json (series rows + new arrivals) ---
    with open(os.path.join(MM_DATA, "home.json"), encoding="utf-8") as f:
        home_doc = json.load(f)
    for row in home_doc.get("series", []):
        for s in row.get("sets", []):
            s["price"] = 1
    for s in home_doc.get("new", []):
        s["price"] = 1
    home_doc["meta"]["price_mmk"] = 1
    home_doc["meta"]["bot"] = BOT_USERNAME
    with open(os.path.join(OUT_DATA, "home.json"), "w",
              encoding="utf-8") as f:
        json.dump(home_doc, f, ensure_ascii=False)

    # --- per-set detail files ---
    src_sets = os.path.join(MM_DATA, "sets")
    dst_sets = os.path.join(OUT_DATA, "sets")
    n = 0
    for fn in os.listdir(src_sets):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(src_sets, fn), encoding="utf-8") as f:
            d = json.load(f)
        d["price"] = 1
        d["buy_url"] = buy_url(d["id"])
        with open(os.path.join(dst_sets, fn), "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False)
        n += 1

    # --- language-neutral assets, copied verbatim ---
    for name in ("cats.json", "covers.json"):
        shutil.copy2(os.path.join(MM_DATA, name),
                     os.path.join(OUT_DATA, name))
    for dname in ("manual_covers", "manual_covers_clean"):
        src, dst = os.path.join(MM_DATA, dname), os.path.join(OUT_DATA, dname)
        if os.path.isdir(src):
            shutil.rmtree(dst, ignore_errors=True)
            shutil.copytree(src, dst)

    print(f"synced {len(sets_doc.get('sets', []))} sets, {n} detail files, "
          "cats/covers/manual_covers from the Burmese export")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
