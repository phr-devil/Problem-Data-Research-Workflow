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
