#!/usr/bin/env python3
"""Download attributed animal photos from Wikimedia Commons for the demo UI."""
from __future__ import annotations

import json
import time
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "frontend" / "public" / "images" / "animals"
DATASET = ROOT / "data" / "dataset"
ANIMALS = {
    "TCV-AN-001": "hippopotamus animal",
    "TCV-AN-002": "black-shanked douc langur",
    "TCV-AN-003": "white rhinoceros animal",
    "TCV-AN-004": "yellow-cheeked gibbon",
    "TCV-AN-005": "Asian elephant",
    "TCV-AN-006": "Rheinardia ocellata",
    "TCV-AN-007": "hog deer Axis porcinus",
    "TCV-AN-008": "Asian golden cat Catopuma temminckii",
    "TCV-AN-009": "wreathed hornbill",
    "TCV-AN-010": "clouded leopard wild Kaeng Krachan National Park Thailand",
    "TCV-AN-011": "giraffe",
}
HEADERS = {"User-Agent": "SaigonZooGuideClassroomDemo/1.0 (educational project; Wikimedia Commons attribution saved)"}


def fetch_json(url: str) -> dict:
    with urlopen(Request(url, headers=HEADERS), timeout=30) as response:
        return json.loads(response.read())


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    credits_file = DATASET / "demo_image_credits.json"
    credits = json.loads(credits_file.read_text(encoding="utf-8")) if credits_file.exists() else {}
    for code, term in ANIMALS.items():
        params = urlencode({
            "action": "query", "generator": "search", "gsrsearch": f"filetype:bitmap {term}",
            "gsrnamespace": 6, "gsrlimit": 20, "prop": "imageinfo", "iiprop": "url|extmetadata",
            "iiurlwidth": 1000, "format": "json",
        })
        if credits.get(code, {}).get("filename"):
            params = urlencode({"action": "query", "titles": credits[code]["filename"], "prop": "imageinfo", "iiprop": "url|extmetadata", "iiurlwidth": 1280, "format": "json"})
        pages = fetch_json("https://commons.wikimedia.org/w/api.php?" + params).get("query", {}).get("pages", {})
        choices = sorted(pages.values(), key=lambda page: page.get("index", 999))
        choice = next((page for page in choices if page.get("imageinfo") and page["imageinfo"][0].get("thumburl")), None)
        if not choice:
            raise RuntimeError(f"No Commons image found for {code}: {term}")
        info = choice["imageinfo"][0]
        destination = OUTPUT / Path(credits.get(code, {}).get("local_path", f"{code.lower()}.jpg")).name
        with urlopen(Request(info["thumburl"], headers=HEADERS), timeout=60) as response:
            content = response.read()
        if len(content) < 10000:
            raise RuntimeError(f"Commons image download too small for {code}")
        destination.write_bytes(content)
        metadata = info.get("extmetadata", {})
        credits[code] = {
            "search_term": term,
            "filename": choice.get("title"),
            "file_page": info.get("descriptionurl"),
            "source_url": info.get("url"),
            "license": metadata.get("LicenseShortName", {}).get("value"),
            "license_url": metadata.get("LicenseUrl", {}).get("value"),
            "artist_html": metadata.get("Artist", {}).get("value"),
            "local_path": f"/images/animals/{destination.name}",
            "bytes": len(content),
        }
        print(f"{code}: {len(content)} bytes · {choice.get('title')}")
        time.sleep(0.25)
    (DATASET / "demo_image_credits.json").write_text(json.dumps(credits, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
