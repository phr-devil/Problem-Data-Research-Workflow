"""No network in tests; only deterministic provider normalization and failure modes."""
import unittest
from core.contracts import ContractError
from core.literature import literature_search, normalize

def fake_fetch(url):
    if "openalex" in url:
        return {"results":[{"id":"https://openalex.org/W1","title":"A credible study",
                            "doi":"https://doi.org/10.1234/ABC","publication_year":2026},
                           {"id":"https://openalex.org/W2","title":"Different paper",
                            "doi":None,"publication_year":2024}]}
    return {"message":{"items":[{"DOI":"10.1234/abc","title":["A credible study"],
                                 "published":{"date-parts":[[2026,1,1]]}},
                                {"DOI":"10.9999/xyz","title":["Third paper"],
                                 "published":{"date-parts":[[2023]]}}]}}

class LiteratureTests(unittest.TestCase):
    def test_normalize_dedup_doi(self):
        data=literature_search("cross-device sensor adaptation",limit=8,fetch=fake_fetch)
        self.assertEqual(data["status"],"SOURCE_METADATA_ONLY")
        self.assertEqual(len(data["results"]),3)
        self.assertEqual(data["results"][0]["doi"],"10.1234/abc")
        self.assertIn("searched_at_utc",data)

    def test_one_source_failure_is_disclosed(self):
        def partial(url):
            if "crossref" in url:
                raise ContractError("unavailable")
            return fake_fetch(url)
        data=literature_search("query",fetch=partial)
        self.assertEqual(data["status"],"SOURCE_METADATA_PARTIAL")
        self.assertIn("crossref",data["provider_failures"])

    def test_no_results_never_means_novel(self):
        def fail(_):
            raise ContractError("unavailable")
        data=literature_search("query",fetch=fail)
        self.assertEqual(data["status"],"NO_VERIFIED_RESULTS")
        self.assertEqual(data["results"],[])

    def test_bounded_query(self):
        with self.assertRaises(ContractError):
            literature_search("a"*401,fetch=fake_fetch)
        with self.assertRaises(ContractError):
            literature_search("query",limit=100,fetch=fake_fetch)

if __name__=="__main__":
    unittest.main()
