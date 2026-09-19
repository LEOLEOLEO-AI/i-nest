"""Fetch targeted primary-source pages with structured HTML parsing."""

from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import quote
import json
import re
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
SOURCES = [
    ("R38", "https://www.nature.com/articles/s41586-025-09384-2"),
    ("R39", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1038/nature13665&format=json&resultType=core"),
    ("R40", "https://api.crossref.org/works/10.1126/science.adi8474"),
    ("R41", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1038/s41467-022-33476-6&format=json&resultType=core"),
    ("R42", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1016/j.cell.2015.09.034&format=json&resultType=core"),
    ("R43", "https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=DOI:10.1038/s41467-025-63831-2&format=json&resultType=core"),
]


def main():
    lines = ["# Additional Source Access Records", "", "Date: 2026-09-18. Primary-source targeted retrieval; not an exhaustive review.", ""]
    for key, url in SOURCES:
        lines += [f"## {key}", "", f"Source: {url}", ""]
        try:
            req = Request(url, headers={"User-Agent": "iNEST-Research/1.0"})
            with urlopen(req, timeout=25) as response:
                raw, status = response.read().decode("utf-8"), response.status
            if "europepmc" in url:
                records = json.loads(raw).get("resultList", {}).get("result", [])
                if not records:
                    raise ValueError("No matching DOI record")
                record = records[0]
                abstract = BeautifulSoup(record.get("abstractText", ""), "html.parser").get_text(" ", strip=True)
                lines += [f"HTTP: {status}", f"Title: {record.get('title')}",
                          f"DOI: {record.get('doi')}", f"Year: {record.get('pubYear')}",
                          f"Authors: {record.get('authorString')}", abstract[:900], ""]
            elif "api.crossref.org" in url:
                record = json.loads(raw)["message"]
                lines += [f"HTTP: {status}", f"Title: {' '.join(record.get('title', []))}",
                          f"DOI: {record.get('DOI')}", f"Publication: {record.get('published')}",
                          f"First author: {record.get('author', [{}])[0].get('family')}", ""]
                abstract = BeautifulSoup(record.get("abstract", ""), "html.parser").get_text(" ", strip=True)
                lines += ["Abstract available: " + str(bool(abstract)), abstract[:900], ""]
            else:
                soup = BeautifulSoup(raw, "html.parser")
                title = soup.find("meta", attrs={"name": "citation_title"})
                lines += [f"HTTP: {status}", "Title: " + (title.get("content", "") if title else soup.title.get_text()), ""]
                for section in soup.find_all("section"):
                    heading = section.find(["h2", "h3"])
                    if heading and re.search(r"Abstract", heading.get_text(), re.I):
                        text = section.get_text(" ", strip=True)
                        lines += [text[:900], ""]
                        break
                metadata = {node.get("name"): node.get("content") for node in soup.find_all("meta")
                            if (node.get("name") or "").startswith("citation_")}
                lines += [json.dumps(metadata, ensure_ascii=False), ""]
            print(key, status, url)
        except Exception as exc:
            lines += [f"Access failure: {type(exc).__name__}: {exc}", ""]
            print(key, type(exc).__name__, str(exc)[:120])
    (ROOT / "11_Additional_Source_Records.md").write_text("\n".join(lines), encoding="utf-8")


if __name__ == "__main__":
    main()
