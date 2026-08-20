from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


FORMULA_CHARS = set("=+-−×⋅*/^_()[]{}∈≤≥≈√πφαΓΘΦΨλβδσμντ|")
INLINE_FORMULA_HINTS = (
    "CST",
    "Erelenv",
    "RI",
    "NMI",
    "Mantel",
    "exp",
    "ln",
    "KL",
    "kavg",
    "Rsw",
    "Gamma",
    "theta",
)
NON_FORMULA_HINTS = (
    "ISBN",
    "CIP",
    "开本",
    "责任编辑",
    "责任校对",
    "责任印制",
    "邮政编码",
    "http://",
    "https://",
)


@dataclass
class PageExtraction:
    page_number: int
    raw_text: str
    normalized_text: str
    formula_candidates: list[tuple[str, str]]


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Extract text from a PDF file and save it as Markdown or plain text."
    )
    parser.add_argument("pdf_path", help="Absolute or relative path to the PDF file")
    parser.add_argument(
        "-o",
        "--output",
        help="Output file path. Defaults to the PDF path with .md extension.",
    )
    parser.add_argument(
        "--format",
        choices=["md", "txt"],
        default="md",
        help="Output format. Default: md",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=None,
        help="Optional maximum number of pages to extract",
    )
    parser.add_argument(
        "--page-breaks",
        action="store_true",
        help="Preserve page-by-page output in Markdown.",
    )
    parser.add_argument(
        "--formula-review",
        action="store_true",
        help="Add a formula review section with normalized candidates.",
    )
    return parser


def _load_reader(pdf_path: Path):
    try:
        from pypdf import PdfReader
    except ImportError:
        print(
            "Missing dependency: pypdf\n"
            "Install it in your current Python environment with:\n"
            "  pip install pypdf",
            file=sys.stderr,
        )
        raise SystemExit(2)

    try:
        return PdfReader(str(pdf_path))
    except Exception as exc:
        print(f"Failed to open PDF: {exc}", file=sys.stderr)
        raise SystemExit(1)


def _normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _looks_like_formula(line: str) -> bool:
    stripped = line.strip()
    if not stripped:
        return False
    if any(hint in stripped for hint in NON_FORMULA_HINTS):
        return False
    if len(stripped) <= 2:
        return True
    symbol_hits = sum(char in FORMULA_CHARS for char in stripped)
    digit_hits = sum(char.isdigit() for char in stripped)
    alpha_hits = sum(char.isalpha() for char in stripped)
    hint_hit = any(hint in stripped for hint in INLINE_FORMULA_HINTS)
    if "=" in stripped or "∈" in stripped or "≈" in stripped:
        return True
    if hint_hit and (symbol_hits > 0 or digit_hits > 0):
        return True
    if symbol_hits >= 2 and alpha_hits <= len(stripped) * 0.7:
        return True
    if stripped.startswith(("(", "[", "{")) and digit_hits > 0:
        return True
    return False


def _should_merge_formula_lines(current: str, nxt: str) -> bool:
    current = current.strip()
    nxt = nxt.strip()
    if not current or not nxt:
        return False
    if any(hint in current for hint in NON_FORMULA_HINTS) or any(hint in nxt for hint in NON_FORMULA_HINTS):
        return False
    if current.endswith(("=", "∈", "{", "(", "[", "/", "·", "+", "-", "−", "≈")):
        return True
    if current.count("{") > current.count("}"):
        return True
    if current.count("(") > current.count(")"):
        return True
    if current.count("[") > current.count("]"):
        return True
    if _looks_like_formula(current) and _looks_like_formula(nxt):
        if len(current) <= 20 or len(nxt) <= 20:
            return True
        if nxt.startswith((")", "]", "}", ",", ".", "·")):
            return True
    return False


def _normalize_formula_text(line: str) -> str:
    normalized = line.strip()
    normalized = normalized.replace("Γst", "Γ_st")
    normalized = normalized.replace("θk", "θ_k")
    normalized = normalized.replace("C_S", "CS")
    normalized = normalized.replace("C_T", "CT")
    normalized = re.sub(r"\bCS\b", "CS", normalized)
    normalized = re.sub(r"\bCT\b", "CT", normalized)
    normalized = re.sub(r"CST=CS\s*⋅\s*CT\s*⋅\s*eα\s*⋅\s*Γ_st", "CST = CS · CT · e^(αΓ_st)", normalized)
    normalized = re.sub(r"CST=CS\s*⋅\s*CT\s*⋅\s*eα\s*⋅\s*Γst", "CST = CS · CT · e^(αΓ_st)", normalized)
    normalized = re.sub(r"CST=CS\s*\+\s*CT\s*\+\s*Γ_st", "CST = CS + CT + Γ_st", normalized)
    normalized = re.sub(r"RI=CST/Erelenv", "RI = CST / Erelenv", normalized)
    normalized = re.sub(
        r"I=\s*Θ\(CST−θ_k\)⋅σ\(RI\)",
        "I = Θ(CST - θ_k) · σ(RI)",
        normalized,
    )
    normalized = re.sub(
        r"I=\s*Θ\(CST−θk\)⋅σ\(RI\)",
        "I = Θ(CST - θ_k) · σ(RI)",
        normalized,
    )
    normalized = re.sub(
        r"σ\(RI\)=\s*1\s*/?\s*1\+e−λ\(RI−1\)",
        "σ(RI) = 1 / (1 + e^(-λ(RI-1)))",
        normalized,
    )
    normalized = re.sub(
        r"θ_k∈\s*\{√2\s*/?\s*2\s*,1,φ,e,π,δ,∞\s*\}",
        "θ_k ∈ {√2/2, 1, φ, e, π, δ, ∞}",
        normalized,
    )
    normalized = re.sub(
        r"θ_k∈\s*\{√2\s*2\s*,1,φ,e,π,δ,∞\s*\}",
        "θ_k ∈ {√2/2, 1, φ, e, π, δ, ∞}",
        normalized,
    )
    normalized = re.sub(
        r"θ_k\s*∈\s*\{√2\s*/\s*2\s*,\s*1,\s*φ,\s*e,\s*π,\s*δ,\s*∞\s*\}",
        "θ_k ∈ {√2/2, 1, φ, e, π, δ, ∞}",
        normalized,
    )
    normalized = re.sub(
        r"Γ_st=\s*NMI\(M_S,M_T\)⋅sign\(Mantel\(A,FC\)\)",
        "Γ_st = NMI(M_S, M_T) · sign(Mantel(A, FC))",
        normalized,
    )
    normalized = re.sub(
        r"Γ_st=\s*NM I\(M_S,M_T\)⋅sign\(M antel\(A,FC\)\)",
        "Γ_st = NMI(M_S, M_T) · sign(Mantel(A, FC))",
        normalized,
    )
    normalized = re.sub(
        r"CS\s*=\s*\(C0\.8⋅H1\.2⋅M 1\.0⋅R1\.1sw\)1/4\.1",
        "CS = (C^0.8 · H^1.2 · M^1.0 · R_sw^1.1)^(1/4.1)",
        normalized,
    )
    normalized = re.sub(
        r"CT=\s*\(λ1\.3eff⋅Φ0\.9⋅Ψ1\.0⋅Θ1\.1\)\s*1/4\.3",
        "CT = (λ_eff^1.3 · Φ^0.9 · Ψ^1.0 · Θ^1.1)^(1/4.3)",
        normalized,
    )
    normalized = re.sub(
        r"λeff=\s*exp\(−\s*\(σbranch− 1\)2\s*/\s*2w2\s*\)",
        "λ_eff = exp(- (σ_branch - 1)^2 / (2w^2))",
        normalized,
    )
    normalized = re.sub(
        r"α=dlnR\s*/\s*dΓ_st",
        "α = d(ln R) / dΓ_st",
        normalized,
    )
    normalized = normalized.replace("⋅", " · ")
    normalized = re.sub(r"Γ_st\s*\[\s*−1,1\s*\]", "Γ_st ∈ [−1, 1]", normalized)
    normalized = re.sub(r"Erelenv\(T\|S\)=K\(T\|S\)−I\(S;T\)", "Erelenv(T|S) = K(T|S) − I(S;T)", normalized)
    normalized = re.sub(r"\s{2,}", " ", normalized)
    return normalized.strip()


def _normalize_text(text: str) -> tuple[str, list[tuple[str, str]]]:
    normalized_lines: list[str] = []
    candidates: list[tuple[str, str]] = []
    buffer_line = ""
    raw_lines = [line.strip() for line in _normalize_whitespace(text).splitlines()]
    i = 0
    while i < len(raw_lines):
        line = raw_lines[i]
        if not line:
            if buffer_line:
                normalized_lines.append(buffer_line)
                buffer_line = ""
            normalized_lines.append("")
            i += 1
            continue

        while i + 1 < len(raw_lines) and _should_merge_formula_lines(line, raw_lines[i + 1]):
            line = f"{line} {raw_lines[i + 1].strip()}".strip()
            i += 1

        if _looks_like_formula(line):
            if buffer_line:
                normalized_lines.append(buffer_line)
                buffer_line = ""
            normalized = _normalize_formula_text(line)
            normalized_lines.append(normalized)
            if normalized != line:
                candidates.append((line, normalized))
            elif any(char in FORMULA_CHARS for char in line):
                candidates.append((line, normalized))
            i += 1
            continue

        if buffer_line:
            if buffer_line.endswith("-"):
                buffer_line = buffer_line[:-1] + line
            else:
                buffer_line = f"{buffer_line} {line}"
        else:
            buffer_line = line
        i += 1

    if buffer_line:
        normalized_lines.append(buffer_line)

    normalized_text = "\n".join(normalized_lines).strip()
    return normalized_text, candidates


def _extract_pages(pdf_path: Path, max_pages: int | None) -> tuple[list[PageExtraction], int]:
    reader = _load_reader(pdf_path)
    total_pages = len(reader.pages)
    page_limit = total_pages if max_pages is None else min(max_pages, total_pages)

    pages: list[PageExtraction] = []
    for index in range(page_limit):
        page = reader.pages[index]
        raw_text = (page.extract_text() or "").strip()
        normalized_text, candidates = _normalize_text(raw_text)
        pages.append(
            PageExtraction(
                page_number=index + 1,
                raw_text=raw_text,
                normalized_text=normalized_text,
                formula_candidates=candidates,
            )
        )

    return pages, page_limit


def _render_formula_review(pages: list[PageExtraction]) -> list[str]:
    lines = ["## Formula Review", ""]
    found = False
    for page in pages:
        if not page.formula_candidates:
            continue
        found = True
        lines.append(f"### Page {page.page_number}")
        lines.append("")
        for raw, normalized in page.formula_candidates:
            lines.append("- Raw:")
            lines.append(f"  ```text\n  {raw}\n  ```")
            lines.append("- Normalized candidate:")
            lines.append(f"  ```text\n  {normalized}\n  ```")
        lines.append("")
    if not found:
        lines.append("No formula-like lines were detected.")
        lines.append("")
    return lines


def _to_markdown(
    pages: list[PageExtraction],
    pdf_path: Path,
    extracted_pages: int,
    page_breaks: bool,
    formula_review: bool,
) -> str:
    title = pdf_path.stem
    lines = [
        f"# {title}",
        "",
        f"- Source: `{pdf_path}`",
        f"- Extracted pages: {extracted_pages}",
        f"- Page-structured extraction: {'yes' if page_breaks else 'no'}",
        f"- Formula review: {'yes' if formula_review else 'no'}",
        "",
        "## Notes",
        "",
        "- This Markdown keeps normalized text to reduce formula ambiguity.",
        "- Formula-like lines may still require manual comparison against the original PDF.",
        "",
    ]

    if formula_review:
        lines.extend(_render_formula_review(pages))

    lines.append("## Extracted Text")
    lines.append("")

    if not pages:
        lines.append("No extractable text was found in the PDF.")
        lines.append("")
        return "\n".join(lines)

    if page_breaks:
        for page in pages:
            lines.append(f"### Page {page.page_number}")
            lines.append("")
            lines.append(page.normalized_text or "No extractable text was found on this page.")
            lines.append("")
    else:
        combined = "\n\n".join(page.normalized_text for page in pages if page.normalized_text).strip()
        lines.append(combined if combined else "No extractable text was found in the PDF.")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    pdf_path = Path(args.pdf_path).expanduser().resolve()
    if not pdf_path.exists():
        print(f"PDF file not found: {pdf_path}", file=sys.stderr)
        return 1
    if pdf_path.suffix.lower() != ".pdf":
        print(f"Input is not a PDF file: {pdf_path}", file=sys.stderr)
        return 1

    output_path = (
        Path(args.output).expanduser().resolve()
        if args.output
        else pdf_path.with_suffix(f".{args.format}")
    )

    pages, extracted_pages = _extract_pages(pdf_path, args.max_pages)

    if args.format == "md":
        content = _to_markdown(
            pages,
            pdf_path,
            extracted_pages,
            page_breaks=args.page_breaks,
            formula_review=args.formula_review,
        )
    else:
        content = "\n\n".join(page.normalized_text for page in pages if page.normalized_text).strip()
        if not content:
            content = "No extractable text was found in the PDF.\n"

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(content, encoding="utf-8")

    print(f"Saved extracted content to: {output_path}")
    print(f"Pages extracted: {extracted_pages}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
