"""Explicit, source-backed metadata search (not a novelty judgement).

Inspired by Research-Workflow-Forge/adapters/literature.py. Network access happens
only when literature_search() is explicitly called, never during normal workflow.
"""
from __future__ import annotations
import json
from datetime import datetime, timezone
from urllib.parse import urlencode
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from core.contracts import ContractError

PROVIDERS = ("openalex", "crossref")
MAX_BYTES = 2_000_000

def _get_json(url: str) -> dict:
    req = Request(url, headers={"Accept":"application/json", "User-Agent":"PD-RW/1.5 (research metadata; contact repository maintainer)"})
    try:
        with urlopen(req, timeout=15) as response:
            payload = response.read(MAX_BYTES + 1)
        if len(payload) > MAX_BYTES:
            raise ContractError("metadata response exceeds 2 MB")
        data = json.loads(payload.decode("utf-8"))
        if not isinstance(data, dict):
            raise ContractError("metadata response is not a JSON object")
        return data
    except (HTTPError, URLError, TimeoutError, UnicodeError, json.JSONDecodeError) as exc:
        raise ContractError("metadata provider unavailable: " + type(exc).__name__) from exc

def _doi(raw: object) -> str | None:
    if not isinstance(raw, str):
        return None
    doi=raw.strip().lower()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if doi.startswith(prefix):
            doi=doi[len(prefix):]
    return doi if doi.startswith("10.") and "/" in doi else None

def normalize(provider: str, response: dict) -> list[dict]:
    if provider=="openalex":
        records=response.get("results")
        if not isinstance(records,list):
            raise ContractError("OpenAlex results unavailable")
        rows=[{"title":x.get("title"),"doi":x.get("doi"),"year":x.get("publication_year"),
               "id":x.get("id")} for x in records if isinstance(x,dict)]
    elif provider=="crossref":
        records=response.get("message",{}).get("items")
        if not isinstance(records,list):
            raise ContractError("Crossref items unavailable")
        rows=[{"title":(x.get("title") or [None])[0],
               "doi":x.get("DOI"),
               "year":(x.get("published",{}).get("date-parts") or [[None]])[0][0],
               "id":x.get("DOI")} for x in records if isinstance(x,dict)]
    else:
        raise ContractError("unknown metadata source")
    out=[]
    for row in rows:
        title=row["title"]
        if not isinstance(title,str) or not title.strip():
            continue
        out.append({"title":title.strip()[:500],"doi":_doi(row["doi"]),
                    "year":row["year"] if isinstance(row["year"],int) else None,
                    "provider":provider,"source_id":row["id"] if isinstance(row["id"],str) else None})
    return out

def literature_search(query: str, limit: int=5, *, fetch=_get_json) -> dict:
    """Return cited metadata without fabricating failures. Actual citations need paper verification."""
    if not isinstance(query,str) or not query.strip() or len(query)>400:
        raise ContractError("query must be 1-400 characters")
    if not isinstance(limit,int) or not 1<=limit<=10:
        raise ContractError("limit must be between 1 and 10")
    urls={
        "openalex":"https://api.openalex.org/works?"+urlencode({"search":query,"per_page":limit,
                       "select":"id,title,doi,publication_year"}),
        "crossref":"https://api.crossref.org/works?"+urlencode({"query.bibliographic":query,"rows":limit,
                       "select":"DOI,title,published"})
    }
    all_rows=[];failures={}
    for provider in PROVIDERS:
        try:
            all_rows.extend(normalize(provider, fetch(urls[provider])))
        except (ContractError,KeyError,TypeError,IndexError,ValueError) as exc:
            failures[provider]=type(exc).__name__
    seen=set(); unique=[]
    for row in all_rows:
        key=row["doi"] or row["title"].casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(row)
    return {"status":("SOURCE_METADATA_PARTIAL" if failures else "SOURCE_METADATA_ONLY") if unique else "NO_VERIFIED_RESULTS",
            "query":query, "searched_at_utc":datetime.now(timezone.utc).isoformat(),
            "providers":list(PROVIDERS), "results":unique[:limit],
            "provider_failures":failures,
            "limits":"Metadata is not full text; neither absence nor similarity of titles proves novelty. Verify strongest neighboring papers."}


# Exact DOI verification is separate from fuzzy literature_search; do not treat
# metadata matching as verification of any cited scientific claim.
import re as _re
import unicodedata as _unicode
from urllib.parse import quote as _quote


def _plain(value: object) -> str:
    if not isinstance(value, str):
        return ""
    return "".join(c for c in _unicode.normalize("NFKC", value).casefold() if c.isalnum())


def _crossref_record(data: dict) -> dict:
    row = data.get("message", {})
    if not isinstance(row, dict) or not row.get("DOI"):
        raise ContractError("not an exact Crossref DOI record")
    title = row.get("title") or []
    container = row.get("container-title") or []
    date = row.get("published") or row.get("published-print") or row.get("published-online") or {}
    parts = date.get("date-parts", []) if isinstance(date, dict) else []
    authors = row.get("author") or []
    return {"doi": _doi(row.get("DOI")), "title": title[0] if title else None,
            "year": parts[0][0] if parts and parts[0] else None,
            "first_author": authors[0].get("family") if authors else None,
            "container_title": container[0] if container else None,
            "volume": row.get("volume"), "issue": row.get("issue"),
            "pages": row.get("page"), "article_number": row.get("article-number"),
            "update_signals": {k: row.get(k) for k in ("update-to", "update-policy", "relation")
                               if row.get(k)}}


def _datacite_record(data: dict) -> dict:
    row = data.get("data", {}).get("attributes", {})
    if not isinstance(row, dict) or not row.get("doi"):
        raise ContractError("not an exact DataCite DOI record")
    titles = row.get("titles") or []
    creators = row.get("creators") or []
    surname = creators[0].get("familyName") or (creators[0].get("name") or "").split(",")[0] if creators else None
    year = row.get("publicationYear")
    return {"doi": _doi(row.get("doi")), "title": titles[0].get("title") if titles else None,
            "year": year if isinstance(year, int) else None,
            "first_author": surname, "container_title": None, "volume": None,
            "issue": None, "pages": None, "article_number": None,
            "update_signals": {k: row.get(k) for k in ("relatedIdentifiers",) if row.get(k)}}


def verify_reference_metadata(reference: dict, *, fetch=_get_json) -> dict:
    """Verify exact DOI record and supplied bibliographic fields (NO full-text support test).

    Call explicitly for references that are authorized for public DOI metadata queries.
    fetch is injectable; offline tests use fixtures and never access the network.
    """
    if not isinstance(reference, dict):
        raise ContractError("reference must be a dictionary")
    doi = _doi(reference.get("doi"))
    if doi is None or not _re.fullmatch(r"10\.\d{4,9}/[^\s]+", doi):
        return {"status": "NO_VALID_DOI_MANUAL_CHECK", "doi": None, "provider": None,
                "checks": {}, "source_claim_support": "NOT_CHECKED"}
    urls = {
        "crossref": "https://api.crossref.org/works/" + _quote(doi, safe=""),
        "datacite": "https://api.datacite.org/dois/" + _quote(doi, safe=""),
    }
    failures = {}
    record = None
    used = None
    for provider, parse in (("crossref", _crossref_record), ("datacite", _datacite_record)):
        try:
            candidate = parse(fetch(urls[provider]))
            if candidate["doi"] != doi:
                failures[provider] = "DOI_MISMATCH"
                continue
            record, used = candidate, provider
            break
        except (ContractError, KeyError, IndexError, TypeError, ValueError, AttributeError) as exc:
            failures[provider] = type(exc).__name__
    if record is None:
        return {"status": "METADATA_UNAVAILABLE", "doi": doi, "provider": None,
                "checks": {}, "provider_failures": failures,
                "source_claim_support": "NOT_CHECKED"}
    checks = {}
    for field in ("title", "year", "first_author", "container_title",
                  "volume", "issue", "pages", "article_number"):
        supplied = reference.get(field)
        actual = record.get(field)
        if supplied is None or supplied == "":
            checks[field] = "NOT_PROVIDED"
        elif actual is None or actual == "":
            checks[field] = "METADATA_MISSING"
        elif field == "year":
            checks[field] = "MATCH" if str(supplied) == str(actual) else "MISMATCH"
        elif field == "first_author":
            # A surname or "Surname, First" is accepted; never compare initials alone.
            surname = str(supplied).split(",")[0].split()[-1]
            checks[field] = "MATCH" if _plain(surname) == _plain(actual) else "MISMATCH"
        else:
            checks[field] = "MATCH" if _plain(str(supplied)) == _plain(str(actual)) else "MISMATCH"
    critical = ("title", "year", "first_author")
    if "MISMATCH" in checks.values():
        status = "METADATA_MISMATCH"
    elif all(checks[k] == "MATCH" for k in critical):
        status = "METADATA_MATCH"
    else:
        status = "METADATA_PARTIAL"
    return {"status": status, "doi": doi, "provider": used, "checks": checks,
            "metadata": record, "provider_failures": failures,
            "checked_at_utc": datetime.now(timezone.utc).isoformat(),
            "publication_update_signals": record["update_signals"],
            "publication_status": "CHECK_OFFICIAL_PUBLISHER",
            "source_claim_support": "NOT_CHECKED",
            "limits": "DOI metadata does not establish full-text support, absence of retraction, or reference coverage."}
