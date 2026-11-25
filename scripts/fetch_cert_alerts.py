#!/usr/bin/env python3
"""Fetch the official CERT-FR alerts RSS feed and emit a safe static JSON snapshot."""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import html
import json
import re
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

FEED_URL = "https://cert.cyber.gouv.fr/alerte/feed/"
CVE_RE = re.compile(r"\\bCVE-20\\d{2}-\\d{4,8}\\b", re.I)
HTML_RE = re.compile(r"<[^>]+>")
TAG_RE = re.compile(r"<(script|style)\\b[^>]*>.*?</\\1>", re.I | re.S)
EXPLOIT_RE = re.compile(r"exploitation active|activement exploité|actively exploited|exploited in the wild", re.I)
MONTHS = {
    "janvier": 1, "février": 2, "fevrier": 2, "mars": 3, "avril": 4,
    "mai": 5, "juin": 6, "juillet": 7, "août": 8, "aout": 8,
    "septembre": 9, "octobre": 10, "novembre": 11, "décembre": 12, "decembre": 12,
}

def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1].lower()

def child_text(node: ET.Element, wanted: str) -> str:
    for child in node:
        if local_name(child.tag) == wanted.lower():
            if wanted.lower() == "link" and child.attrib.get("href"):
                return child.attrib["href"]
            return "".join(child.itertext()).strip()
    return ""

def clean_text(value: str) -> str:
    value = html.unescape(value or "")
    value = TAG_RE.sub(" ", value)
    value = HTML_RE.sub(" ", value)
    return re.sub(r"\\s+", " ", value).strip()

def iso_date(raw_date: str, title: str) -> str:
    if raw_date:
        try:
            parsed = email.utils.parsedate_to_datetime(raw_date)
            if parsed:
                return parsed.date().isoformat()
        except (TypeError, ValueError, OverflowError):
            try:
                return dt.datetime.fromisoformat(raw_date.replace("Z", "+00:00")).date().isoformat()
            except ValueError:
                pass
    match = re.search(r"\\((\\d{1,2})\\s+([A-Za-zÀ-ÿ]+)\\s+(20\\d{2})\\)", title)
    if match:
        month = MONTHS.get(match.group(2).lower())
        if month:
            return dt.date(int(match.group(3)), month, int(match.group(1))).isoformat()
    return dt.datetime.now(dt.timezone.utc).date().isoformat()

def item_record(node: ET.Element) -> dict:
    title = clean_text(child_text(node, "title")) or "Alerte CERT-FR"
    link = child_text(node, "link").strip()
    description = clean_text(child_text(node, "description") or child_text(node, "summary"))
    published = child_text(node, "pubdate") or child_text(node, "published") or child_text(node, "updated")
    date = iso_date(published, title)
    cves = sorted(set(x.upper() for x in CVE_RE.findall(title + " " + description)))
    exploited = bool(EXPLOIT_RE.search(title + " " + description))
    priority = "P1" if exploited else "P2"
    identifier = re.sub(r"[^a-zA-Z0-9]+", "", link or (title + date))[-40:]
    return {
        "id": "certfr-" + identifier.lower(),
        "date": date,
        "product": title,
        "cve": " / ".join(cves) if cves else "Alerte CERT-FR",
        "cvss": "Non fourni par le flux",
        "priority": priority,
        "status": "Exploitation active signalée" if exploited else "À qualifier",
        "kev": False,
        "checkedSI": False,
        "summary": description or "Consulter l’avis CERT-FR pour le détail de l’alerte.",
        "affected": "À confirmer dans l’avis CERT-FR : produit, versions et conditions d’exposition.",
        "action": "Vérifier si le produit est présent dans le SI, consulter l’avis lié, puis appliquer les mesures de l’éditeur si le périmètre est concerné.",
        "source": link if link.startswith("https://") else FEED_URL,
        "sourceLabel": "CERT-FR · Flux RSS des alertes",
        "confidence": "Source officielle · détails à confirmer dans l’avis",
        "note": "Alerte importée automatiquement. La priorité affichée est indicative ; valider les versions, l’exposition et le risque métier avant toute décision.",
        "owner": "",
        "dueDate": "",
        "followUpStatus": "À faire",
        "followUpComment": "",
        "result": "",
        "evidence": "",
        "sourceType": "CERT-FR RSS",
    }

def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", default="alerts.json")
    args = parser.parse_args()
    request = urllib.request.Request(FEED_URL, headers={"User-Agent": "CyberWatch-CERTFR-RSS/1.0"})
    with urllib.request.urlopen(request, timeout=30) as response:
        raw = response.read()
    root = ET.fromstring(raw)
    nodes = [node for node in root.iter() if local_name(node.tag) == "item"]
    if not nodes:
        nodes = [node for node in root.iter() if local_name(node.tag) == "entry"]
    items = [item_record(node) for node in nodes]
    items = [item for item in items if item["id"] != "certfr-"]
    if not items:
        raise RuntimeError("Le flux CERT-FR a répondu sans alerte exploitable ; publication annulée.")
    items.sort(key=lambda item: (item["date"], item["id"]), reverse=True)
    payload = {
        "version": 1,
        "source": "CERT-FR",
        "sourceUrl": FEED_URL,
        "generatedAt": dt.datetime.now(dt.timezone.utc).isoformat(),
        "items": items[:100],
    }
    Path(args.output).write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\\n", encoding="utf-8")

if __name__ == "__main__":
    main()
