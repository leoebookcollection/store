#!/usr/bin/env python3
"""Export the ENGLISH crypto-edition catalog for the separate crypto ebook store.

Reuses export_catalog.py's full pipeline (same bot grouping logic, same
pids) but overrides:
  - pricing: flat $1 USD per set (no MMK)
  - BOT_USERNAME: CRYPTO_EBOOK_BOT_USERNAME placeholder until he creates
    the bot

Output: ../dist/data/  (home.json + sets.json + sets/<pid>.json)
Language-neutral assets (covers.json, cats.json, manual_covers/) must be
copied separately from the main store's dist/data/.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
MAIN_TOOLS = os.path.normpath(os.path.join(
    HERE, "..", "..", "ebook-store", "tools"))
OUT_DIR = os.path.normpath(os.path.join(HERE, "..", "dist", "data"))

sys.path.insert(0, MAIN_TOOLS)
import export_catalog as ec

# flat $1 pricing for the crypto store.
# NOTE: export writes it into the "price" fields of sets.json/home.json
# and the "price_mmk" meta field — here that field means "price in the
# store's main currency unit" (1 USD), not MMK.
ec.PRICE_MMK = 1
# placeholder — replaced with the real crypto-bot username once created
ec.BOT_USERNAME = "CRYPTO_EBOOK_BOT_USERNAME"
ec.OUT_DIR = OUT_DIR

if __name__ == "__main__":
    sys.exit(ec.main())
