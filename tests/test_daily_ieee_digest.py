import unittest
from unittest.mock import patch

from scripts import daily_ieee_digest as digest


class CollectCandidatesTests(unittest.TestCase):
    def test_collect_candidates_filters_non_paper_entries_and_keeps_authored_articles(self):
        config = {
            "include_keywords": ["antenna"],
            "exclude_keywords": [],
            "journals": [
                {
                    "key": "TAP",
                    "title": "IEEE Transactions on Antennas and Propagation",
                    "issn": "0000-0000",
                    "eissn": None,
                    "metrics": {
                        "system": "JCR-JIF",
                        "year": 2024,
                        "quartile": "Q1",
                        "impact_factor": "5.8",
                        "source": "IEEE Title List",
                        "source_url": "https://example.com/metrics",
                    },
                }
            ],
        }
        response = {
            "message": {
                "items": [
                    {
                        "title": ["IEEE Transactions on Antennas and Propagation Publication Information"],
                        "DOI": "10.1109/tap.2026.3696877",
                        "container-title": ["IEEE Transactions on Antennas and Propagation"],
                        "published-online": {"date-parts": [[2026, 6, 1]]},
                        "URL": "https://example.com/publication-information",
                        "author": [],
                        "abstract": "<jats:p>Administrative page.</jats:p>",
                    },
                    {
                        "title": ["W-Band Broadband Antenna for 3-D Integration"],
                        "DOI": "10.1109/tap.2026.3671385",
                        "container-title": ["IEEE Transactions on Antennas and Propagation"],
                        "published-online": {"date-parts": [[2026, 6, 1]]},
                        "URL": "https://example.com/paper",
                        "author": [
                            {"given": "Ada", "family": "Lovelace"},
                            {"given": "Grace", "family": "Hopper"},
                        ],
                        "abstract": "<jats:p>An antenna paper abstract.</jats:p>",
                    },
                ]
            }
        }

        with patch.object(digest, "get_json", return_value=response):
            candidates = digest.collect_candidates(config, days_back=30, rows_per_journal=10)

        self.assertEqual(1, len(candidates))
        self.assertEqual("10.1109/tap.2026.3671385", candidates[0].doi)
        self.assertEqual("Ada Lovelace, Grace Hopper", candidates[0].authors)
        self.assertEqual("An antenna paper abstract.", candidates[0].abstract)


class MetadataHelpersTests(unittest.TestCase):
    def test_extract_authors_formats_names(self):
        item = {
            "author": [
                {"given": "Ada", "family": "Lovelace"},
                {"name": "Grace Hopper"},
                {"family": "Turing"},
            ]
        }

        self.assertEqual(
            "Ada Lovelace, Grace Hopper, Turing",
            digest.extract_authors(item),
        )

    def test_clean_abstract_strips_jats_markup(self):
        raw = "<jats:p>First <b>line</b>.</jats:p><jats:p>Second line.</jats:p>"

        self.assertEqual("First line. Second line.", digest.clean_abstract(raw))


class RenderingTests(unittest.TestCase):
    def test_render_text_and_html_include_authors_and_abstract(self):
        article = digest.Candidate(
            title="Example Antenna Paper",
            journal="IEEE Transactions on Antennas and Propagation",
            journal_key="TAP",
            doi="10.1109/tap.2026.1234567",
            url="https://example.com/paper",
            published="2026-06-01",
            metrics={
                "system": "JCR-JIF",
                "year": 2024,
                "quartile": "Q1",
                "impact_factor": "5.8",
                "source": "IEEE Title List",
                "source_url": "https://example.com/metrics",
            },
            score=2,
            authors="Ada Lovelace, Grace Hopper",
            abstract="This is the abstract.",
        )

        text_body = digest.render_text([article])
        html_body = digest.render_html([article])

        self.assertIn("Authors: Ada Lovelace, Grace Hopper", text_body)
        self.assertIn("Abstract: This is the abstract.", text_body)
        self.assertNotIn("copyright", text_body.lower())
        self.assertIn("Ada Lovelace, Grace Hopper", html_body)
        self.assertIn("This is the abstract.", html_body)


if __name__ == "__main__":
    unittest.main()
