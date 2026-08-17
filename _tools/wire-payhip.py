#!/usr/bin/env python3
"""
Swap the buy buttons on /packs from mailto: to real Payhip checkout.

  1. Create the 14 products in Payhip (see PAYHIP-LISTINGS.md in the skill-packs project)
  2. Put each product's 5 char key into payhip-links.json
  3. python3 _tools/wire-payhip.py            <- wires the site
     python3 _tools/wire-payhip.py --check    <- dry run, changes nothing
     python3 _tools/wire-payhip.py --revert   <- puts the mailto buttons back

Each button becomes a plain link to the product's Payhip page, opened in a new tab so the
buyer does not lose /packs.

OVERLAY is off on purpose. Payhip's payhip.js turns these into an on page overlay checkout,
which is nicer, but on 2026-08-16 it dimmed the page and aborted without rendering when tested
over http://localhost, with nothing in the console. A buy button that silently does nothing is
worse than a redirect. Turn OVERLAY on only after confirming the overlay actually opens on the
live https domain, and test it there before trusting it.
"""

import json
import re
import sys
from pathlib import Path

OVERLAY = False

ROOT = Path(__file__).resolve().parent.parent
PACKS = ROOT / "packs" / "index.html"
LINKS = Path(__file__).resolve().parent / "payhip-links.json"

EMBED = '<script src="https://payhip.com/payhip.js"></script>'

# The Vault button lives inside the pricing card. The other "Get the Vault" buttons on the
# page are anchors that scroll down to that card and must stay anchors.
VAULT_MAILTO = '<div class="ract"><a class="btn btn-fill" href="/packs#get">Get the Vault</a></div>'


def _attrs(key):
    if OVERLAY:
        return f'payhip-buy-button" data-theme="none" data-product="{key}'
    return ""


def vault_buy(key):
    cls = f"btn btn-fill {_attrs(key)}" if OVERLAY else "btn btn-fill"
    return (
        f'<div class="ract"><a class="{cls}" href="https://payhip.com/b/{key}" '
        f'target="_blank" rel="noopener">Get the Vault</a></div>'
    )


def pack_mailto(slug):
    return f'<a class="rbuy" href="mailto:henry@serhant.com?subject=Pack%3A%20{slug}">Get this pack →</a>'


def pack_buy(slug, key):
    cls = f"rbuy {_attrs(key)}" if OVERLAY else "rbuy"
    return (
        f'<a class="{cls}" href="https://payhip.com/b/{key}" '
        f'target="_blank" rel="noopener">Get this pack →</a>'
    )


def load_keys():
    raw = json.loads(LINKS.read_text())
    keys = {k: v for k, v in raw.items() if not k.startswith("_")}
    bad = [
        k
        for k, v in keys.items()
        if str(v).upper() == "PLACEHOLDER" or not re.fullmatch(r"[A-Za-z0-9]{4,10}", str(v))
    ]
    if bad:
        print("These products have no real Payhip key yet:\n  " + "\n  ".join(bad))
        print(f"\nFill them in at {LINKS} and run this again.")
        sys.exit(1)
    return keys


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "wire"
    html = PACKS.read_text()
    before = html

    if mode == "--revert":
        print("The clean undo is git, because the pack slug is not recoverable from a wired button:")
        print("\n  cd ~/Projects/agent-site && git checkout packs/index.html\n")
        sys.exit(0)

    keys = load_keys()

    wired = 0
    missing = []
    for slug, key in keys.items():
        if slug == "the-vault":
            continue
        old, new = pack_mailto(slug), pack_buy(slug, key)
        if old in html:
            html = html.replace(old, new)
            wired += 1
        elif new in html:
            wired += 1  # already wired, idempotent
        else:
            missing.append(slug)

    vault = vault_buy(keys["the-vault"])
    if VAULT_MAILTO in html:
        html = html.replace(VAULT_MAILTO, vault)
        wired += 1
    elif vault in html:
        wired += 1
    else:
        missing.append("the-vault")

    if OVERLAY and EMBED not in html:
        html = html.replace("</body>", EMBED + "\n</body>")

    if missing:
        print("Could not find the buy button for:\n  " + "\n  ".join(missing))
        print("The page markup changed. Fix the pattern in this script before running again.")
        sys.exit(1)

    if mode == "--check":
        print(f"Dry run: {wired} of 14 buttons would be wired. Nothing written.")
        return

    if html == before:
        print("Already wired. Nothing to do.")
        return

    PACKS.write_text(html)
    print(f"Wired {wired} of 14 buy buttons on /packs to Payhip checkout.")
    print("Mode: " + ("overlay (payhip.js)" if OVERLAY else "plain links, new tab"))
    print("\nNext: serve the site and click a button, confirm the Payhip product page opens.")
    print("Then commit. Ask Henry before pushing, a push publishes to the live domain.")


if __name__ == "__main__":
    main()
