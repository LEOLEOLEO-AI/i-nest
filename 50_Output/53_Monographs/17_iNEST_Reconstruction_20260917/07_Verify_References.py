"""Record Crossref metadata; existence is not verification of claim support."""

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
from pathlib import Path
from urllib.parse import quote
from urllib.request import Request, urlopen


DOIS = [
    "10.1038/srep00514", "10.1103/PhysRevResearch.5.043044",
    "10.1162/NECO_a_00411", "10.1088/0034-4885/75/12/126001",
    "10.1103/PhysRevLett.109.120604", "10.1147/rd.53.0183",
    "10.1103/PhysRevLett.80.2109", "10.1038/s41467-021-24260-z",
    "10.1016/j.neunet.2019.03.005", "10.1038/s41586-021-04223-6",
    "10.3389/fncom.2017.00024", "10.1038/nrn2787",
    "10.1023/A:1010388907793", "10.1073/pnas.1314922110",
    "10.1103/PhysRevE.86.011909", "10.1088/1751-8121/ad8f06",
]


def fetch(doi):
    try:
        request = Request("https://api.crossref.org/works/" + quote(doi, safe=""),
                          headers={"User-Agent": "iNEST-Evidence-Audit/1.0"})
        with urlopen(request, timeout=25) as response:
            record = json.load(response)["message"]
        title = " ".join(record.get("title", []))
        authors = "; ".join((a.get("given", "") + " " + a.get("family", "")).strip()
                            for a in record.get("author", []))
        year = record.get("issued", {}).get("date-parts", [[None]])[0][0]
        updates = record.get("update-to", [])
        return f"| {doi} | FOUND | {title} | {authors} | {year} | {json.dumps(updates, ensure_ascii=False)} |"
    except Exception as exc:
        return f"| {doi} | UNVERIFIED | {type(exc).__name__}: {str(exc)[:160]} | | | |"


def main():
    with ThreadPoolExecutor(max_workers=4) as pool:
        rows = list(pool.map(fetch, DOIS))
    output = Path(__file__).with_name("10_Reference_Metadata.md")
    lines = ["# Reference Metadata", "", f"Retrieved UTC: {datetime.now(timezone.utc).isoformat()}",
             "FOUND means a DOI resolves in Crossref. It does not mean the manuscript's attributed claim is supported.",
             "Empty update metadata does not guarantee absence of corrections or retractions.", "",
             "| DOI | Status | Registered title | Registered authors | Year | Update metadata |",
             "|---|---|---|---|---|---|"] + rows
    output.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(rows))


if __name__ == "__main__":
    main()
