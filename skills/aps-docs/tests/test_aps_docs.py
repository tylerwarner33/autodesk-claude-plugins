"""Tests for scripts/aps_docs.py. They use no network.

Run from the skill folder: python -m unittest discover -s tests
"""

import io
import os
import sys
import unittest
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

import aps_docs  # noqa: E402

SLUG = "A360-platform-viewing-docs-master-1064"

TOC = {
    "api_name": "Model Derivative API",
    "doc_version": "v2",
    "url_path": "model-derivative",
    "children": [
        {
            "url_path": "developers_guide",
            "display_name": "Developer's Guide",
            "children": [
                {"url_path": "overview", "display_name": "Overview",
                 "source": f"{SLUG}/model-derivative/v2/overview.html"},
                {"url_path": "basics", "display_name": "Basics", "children": [
                    {"url_path": "geometry_extraction", "display_name": "Extract Geometry",
                     "source": f"{SLUG}/model-derivative/v2/overview/api_basics/geometry_extraction.html"},
                ]},
            ],
        },
        {
            "url_path": "reference",
            "display_name": "Reference Guide",
            "children": [
                {"url_path": "http", "display_name": "API Reference", "children": [
                    {"url_path": "", "display_name": "Group without a path", "children": [
                        {"url_path": "formats-GET", "display_name": "GET formats",
                         "source": f"{SLUG}/model-derivative/v2/reference/http/model-derivative/formats-GET.html"},
                    ]},
                ]},
            ],
        },
    ],
}


class SourcePathTests(unittest.TestCase):
    def test_full_url_becomes_source_path(self):
        url = f"https://developer.doc.autodesk.com/bPlouYTd/{SLUG}/model-derivative/v2/overview.html?x=1#top"
        self.assertEqual(aps_docs.source_path(url), f"{SLUG}/model-derivative/v2/overview.html")

    def test_source_path_is_unchanged(self):
        self.assertEqual(aps_docs.source_path(f"{SLUG}/a/v1/b.html"), f"{SLUG}/a/v1/b.html")

    def test_guess_source_id(self):
        self.assertEqual(aps_docs.guess_source_id(f"{SLUG}/model-derivative/v2/overview.html"), "model-derivative_v2")
        self.assertIsNone(aps_docs.guess_source_id("model-derivative/v2/overview.html"))


class PortalUrlTests(unittest.TestCase):
    def test_pages_use_the_toc_url_path_chain(self):
        found = {p["name"]: p["portal"] for p in aps_docs.pages(TOC)}
        base = "https://aps.autodesk.com/en/docs/model-derivative/v2/"
        self.assertEqual(found["Overview"], base + "developers_guide/overview/")
        self.assertEqual(found["Extract Geometry"], base + "developers_guide/basics/geometry_extraction/")
        self.assertEqual(found["GET formats"], base + "reference/http/formats-GET/")

    def test_a_url_path_that_repeats_its_parent_is_left_out(self):
        toc = {"url_path": "oauth", "doc_version": "v2", "children": [
            {"url_path": "tutorials", "children": [
                {"url_path": "get-3-legged-token-pkce", "source": None, "children": [
                    {"display_name": "Public", "url_path": "get-3-legged-token-pkce", "source": "s/oauth/v2/a.html"},
                    {"display_name": "Private", "url_path": "get-3-legged-token-pkce-private", "source": "s/oauth/v2/b.html"},
                ]},
            ]},
        ]}
        found = {p["name"]: p["portal"] for p in aps_docs.pages(toc)}
        base = "https://aps.autodesk.com/en/docs/oauth/v2/tutorials/get-3-legged-token-pkce/"
        self.assertEqual(found["Public"], base)
        self.assertEqual(found["Private"], base + "get-3-legged-token-pkce-private/")

    def test_portal_url_is_exact_when_the_page_is_in_the_toc(self):
        with mock.patch.object(aps_docs, "load_toc", return_value=TOC):
            url, exact = aps_docs.portal_url(f"{SLUG}/model-derivative/v2/overview.html")
        self.assertTrue(exact)
        self.assertEqual(url, "https://aps.autodesk.com/en/docs/model-derivative/v2/developers_guide/overview/")

    def test_portal_url_falls_back_to_the_path_rule(self):
        with mock.patch.object(aps_docs, "load_toc", side_effect=aps_docs.FetchError("HTTP 403")):
            url, exact = aps_docs.portal_url(
                "design-automation-docs-master-636116/design-automation/v3/reference/http/design-automation/activities-GET.html")
        self.assertFalse(exact)
        self.assertEqual(url, "https://aps.autodesk.com/en/docs/design-automation/v3/reference/http/activities-GET/")

    def test_path_rule_without_duplicate_folder(self):
        self.assertEqual(
            aps_docs.portal_url_from_path("aecdm-docs-master-633590/aecdatamodel/v1/developers_guide/overview.html"),
            "https://aps.autodesk.com/en/docs/aecdatamodel/v1/developers_guide/overview/")

    def test_path_rule_needs_api_version_and_page(self):
        self.assertIsNone(aps_docs.portal_url_from_path("only/two"))


class TocTests(unittest.TestCase):
    def test_find_section(self):
        self.assertEqual(aps_docs.find_section(TOC, "basics")["display_name"], "Basics")
        self.assertIsNone(aps_docs.find_section(TOC, "missing"))

    def test_pages_lists_only_nodes_with_a_source(self):
        self.assertEqual(len(list(aps_docs.pages(TOC))), 3)

    def test_missing_file_errors(self):
        self.assertTrue(aps_docs.is_missing(aps_docs.FetchError("HTTP 403 for x")))
        self.assertTrue(aps_docs.is_missing(aps_docs.FetchError("HTTP 404 for x")))
        self.assertFalse(aps_docs.is_missing(aps_docs.FetchError("HTTP 500 for x")))


class SourcesTests(unittest.TestCase):
    TEXT = """# Sources

| Source ID | API title |
|---|---|
| `data_v2` | Data Management API |
| `oauth_v2` | Authentication (OAuth) |

## Which API

| The question is about | Start with |
|---|---|
| Tokens, scopes, PKCE | `oauth_v2` |
| Files and folders | `data_v2` |
"""

    def test_without_match_shows_the_whole_file(self):
        self.assertEqual(aps_docs.source_rows(self.TEXT)[0], "# Sources")

    def test_match_shows_rows_under_their_headers(self):
        self.assertEqual(aps_docs.source_rows(self.TEXT, "oauth"), [
            "| Source ID | API title |",
            "|---|---|",
            "| `oauth_v2` | Authentication (OAuth) |",
            "",
            "| The question is about | Start with |",
            "|---|---|",
            "| Tokens, scopes, PKCE | `oauth_v2` |",
        ])

    def test_header_rows_do_not_count_as_matches(self):
        self.assertEqual(aps_docs.source_rows(self.TEXT, "source id"), [])

    def test_the_real_sources_file_has_every_listed_id(self):
        with open(aps_docs.SOURCES_FILE, encoding="utf-8") as stream:
            rows = aps_docs.source_rows(stream.read(), r"^\| `[a-z0-9._-]+` \|")
        self.assertGreaterEqual(len([r for r in rows if r.startswith("| `")]), 26)


class ReferenceCommandTests(unittest.TestCase):
    def run_main(self, argv):
        with mock.patch("sys.stdout", new_callable=io.StringIO) as out:
            code = aps_docs.main(argv)
        return code, out.getvalue()

    def test_each_reference_file_is_readable(self):
        for argv in (["sources"], ["glossary"], ["example"]):
            code, out = self.run_main(argv)
            self.assertEqual(code, 0, argv)
            self.assertTrue(out.startswith("# "), argv)

    def test_glossary_match(self):
        code, out = self.run_main(["glossary", "--match", "aecdm"])
        self.assertEqual(code, 0)
        self.assertIn("AEC Data Model", out)
        self.assertNotIn("| ACC |", out)

    def test_no_match_message(self):
        code, out = self.run_main(["glossary", "--match", "zzz-none"])
        self.assertEqual(code, 0)
        self.assertIn("No rows match", out)


class ArgumentTests(unittest.TestCase):
    def test_refresh_before_or_after_the_command(self):
        parser = aps_docs.build_parser()
        self.assertTrue(parser.parse_args(["--refresh", "toc", "data_v2"]).refresh)
        self.assertTrue(parser.parse_args(["toc", "data_v2", "--refresh"]).refresh)
        self.assertFalse(parser.parse_args(["toc", "data_v2"]).refresh)


class ExtractTests(unittest.TestCase):
    HTML = """
    <html><head><style>.x{}</style><script>var a = 1;</script></head><body>
      <h1>Title</h1>
      <p>First   paragraph
         text.</p>
      <h2>Parameters</h2>
      <table>
        <tr><th>Name</th><th>Type</th></tr>
        <tr><td><span><b>urn</b></span></td><td>string</td></tr>
      </table>
      <ul><li>One</li><li>Two</li></ul>
      <pre>curl -X GET \\
  https://example.test</pre>
      <noscript>Enable JavaScript</noscript>
    </body></html>
    """

    def setUp(self):
        self.parsed = aps_docs.extract(self.HTML)

    def test_headings(self):
        self.assertEqual(self.parsed.headings, [(1, "Title"), (2, "Parameters")])

    def test_text_lines(self):
        lines = self.parsed.lines
        self.assertIn("# Title", lines)
        self.assertIn("First paragraph text.", lines)
        self.assertIn("- One", lines)

    def test_table_cells_are_not_repeated(self):
        self.assertIn("Name | Type", self.parsed.lines)
        self.assertIn("urn | string", self.parsed.lines)
        self.assertEqual(sum("urn" in line for line in self.parsed.lines), 1)

    def test_code_keeps_line_breaks(self):
        self.assertEqual(self.parsed.code_blocks, ["curl -X GET \\\n  https://example.test"])

    def test_script_style_and_noscript_are_removed(self):
        text = "\n".join(self.parsed.lines)
        self.assertNotIn("var a", text)
        self.assertNotIn(".x{}", text)
        self.assertNotIn("Enable JavaScript", text)


if __name__ == "__main__":
    unittest.main()
