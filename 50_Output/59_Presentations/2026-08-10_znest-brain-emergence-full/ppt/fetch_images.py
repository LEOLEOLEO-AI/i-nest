#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Fetch openly licensed Commons images for the iNEST full deck."""
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

API = "https://commons.wikimedia.org/w/api.php"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) CodexPPTFetcher/1.0"
OUT_DIR = Path(__file__).resolve().parent / "images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# page number -> (slug, [search queries in fallback order])
MAPPING = {
    1: ("brain-emergence", ["human brain neurons microscopy", "neural network brain abstract"]),
    3: ("data-center-energy", ["data center server room", "supercomputer data center"]),
    9: ("first-principles-brain", ["neuron network microscopy", "brain neurons microscope"]),
    17: ("brain-connectome", ["brain synapse connection", "neuron synapse"]),
    19: ("interconnect-world", ["network topology nodes", "graph nodes edges network"]),
    20: ("water-hydrogen-bond", ["hydrogen bonding water", "liquid water hydrogen bond"]),
    22: ("diamond-graphite", ["diamond and graphite", "graphite diamond crystal"]),
    24: ("connectome-nematode", ["Caenorhabditis elegans nervous system", "nematode connectome"]),
    31: ("nonlinear-forbidden", ["strange attractor chaos", "nonlinear dynamics attractor"]),
    36: ("nonlinear-optics", ["laser experiment optics", "nonlinear optics laser"]),
    43: ("measurement-scale", ["complex network visualization", "network graph visualization"]),
    57: ("intelligence-ratio", ["human brain intelligence", "brain mind concept"]),
    62: ("six-constants", ["golden ratio spiral", "fibonacci spiral"]),
    69: ("sdde-time", ["oscilloscope waveform", "signal waveform oscilloscope"]),
    73: ("delay-as-resource", ["echo waveform signal", "signal delay oscilloscope"]),
    79: ("four-rules", ["self-organized criticality sandpile", "avalanche sandpile"]),
    85: ("criticality-sandpile", ["sandpile cellular automaton", "self-organized criticality"]),
    91: ("sdi-control", ["control panel circuit board", "network control nodes"]),
    96: ("network-control", ["complex network graph", "network nodes edges"]),
    99: ("topology-center", ["silicon wafer macro", "semiconductor wafer close up"]),
    102: ("mesoscale-wafer", ["silicon wafer fabrication", "semiconductor wafer"]),
    105: ("sd-sow", ["system on wafer semiconductor", "integrated circuit wafer"]),
    106: ("packaging-law", ["semiconductor packaging chip", "chip package"]),
    109: ("formula-to-chip", ["integrated circuit wafer", "chip semiconductor close up"]),
    111: ("zbrain-one", ["silicon wafer chip", "wafer semiconductor"]),
    113: ("zbrain-two", ["multi chip module", "advanced semiconductor packaging"]),
    115: ("zbrain-three", ["brain neural network", "human brain network"]),
    121: ("five-party", ["scientific collaboration team", "research laboratory team"]),
    126: ("four-channels", ["research laboratory funding", "science laboratory"]),
    128: ("brain-research", ["neuroscience laboratory", "brain research"]),
    139: ("industry-map", ["humanoid robot", "industrial robot automation"]),
    140: ("embodied-scene", ["industrial robot factory", "autonomous robot"]),
    141: ("complexity-service", ["industrial automation factory", "manufacturing plant"]),
    146: ("closing-emergence", ["brain network glow", "neural network art"]),
}


def api_search(query: str, limit: int = 8):
    params = {
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrsearch": query,
        "gsrnamespace": "6",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime",
        "iiurlwidth": "1000",
    }
    url = API + "?" + urllib.parse.urlencode(params)
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=25) as resp:
                data = json.load(resp)
            return list((data.get("query") or {}).get("pages", {}).values())
        except urllib.error.HTTPError as exc:
            if exc.code == 429 and attempt < 3:
                time.sleep(1.5 * (attempt + 2))
                continue
            raise
    return []


def pick(pages):
    for page in pages:
        info = (page.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        if mime not in ("image/jpeg", "image/png"):
            continue
        width = info.get("width") or 0
        if width and width < 700:
            continue
        url = info.get("thumburl") or info.get("url")
        title = page.get("title", "")
        if url and title.startswith("File:"):
            return title, url
    return None


def file_page_url(title: str) -> str:
    return "https://commons.wikimedia.org/wiki/" + urllib.parse.quote(title.replace(" ", "_"), safe=":/()%")


def ext_from_url(url: str, mime: str) -> str:
    clean = url.split("?")[0].lower()
    if clean.endswith(".jpg") or clean.endswith(".jpeg"):
        return "jpg"
    if clean.endswith(".png"):
        return "png"
    return "jpg" if mime == "image/jpeg" else "png"


def fetch_one(item):
    page_no, (slug, queries) = item
    for query in queries:
        time.sleep(0.6)
        try:
            pages = api_search(query)
        except Exception as exc:
            print(f"  page {page_no}: search error ({query}): {exc}")
            continue
        hit = pick(pages)
        if not hit:
            continue
        title, url = hit
        clean_url = re.sub(r"[?&]utm_(source|campaign|content)=[^&]+", "", url)
        try:
            req = urllib.request.Request(clean_url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=40) as resp:
                data = resp.read()
                mime = resp.headers.get("Content-Type", "")
        except urllib.error.HTTPError as exc:
            print(f"  page {page_no}: download error 429? {exc}")
            if exc.code == 429:
                time.sleep(3)
                try:
                    req = urllib.request.Request(clean_url, headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=40) as resp:
                        data = resp.read()
                        mime = resp.headers.get("Content-Type", "")
                except Exception as exc2:
                    print(f"  page {page_no}: retry failed: {exc2}")
                    continue
            else:
                continue
        except Exception as exc:
            print(f"  page {page_no}: download error ({query}): {exc}")
            continue
        if len(data) < 10_000:
            continue
        ext = ext_from_url(clean_url, mime)
        name = f"{page_no:03d}-{slug}.{ext}"
        local = OUT_DIR / name
        local.write_bytes(data)
        print(f"  page {page_no}: {name} <- {title}")
        return {
            "page": page_no,
            "slug": slug,
            "local": name,
            "title": title,
            "page_url": file_page_url(title),
        }
    print(f"  page {page_no}: no suitable image found")
    return None


def main():
    results = {}
    for item in sorted(MAPPING.items()):
        result = fetch_one(item)
        if result:
            results[str(result["page"])] = result
    manifest_path = OUT_DIR / "manifest.json"
    manifest_path.write_text(
        json.dumps({"source": "Wikimedia Commons", "items": results}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Done: {len(results)} images -> {manifest_path}")


if __name__ == "__main__":
    main()
