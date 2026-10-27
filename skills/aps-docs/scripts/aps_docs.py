"""Read the Autodesk Platform Services (APS) documentation from its static sources.

The APS portal (aps.autodesk.com) is a JavaScript app. Its content comes from:

- A table of contents (TOC) JSON file for each API:
  https://developer.doc.config.autodesk.com/bPlouYTd/<source_id>.json
- A static HTML file for each page:
  https://developer.doc.autodesk.com/bPlouYTd/<source path from the TOC>

Commands:

  sources                              The source IDs, and which API answers which question.
  sources --match <regex>              Only the rows that match.
  glossary [--match <regex>]           APS terms and acronyms.
  example                              A worked example of the method.
  toc <source_id>                      Top-level sections of an API.
  toc <source_id> --section <url_path> The pages in one section.
  toc <source_id> --match <regex>      The pages whose name or path match.
  toc <source_id> --all                All pages.
  page <source path or URL>            The outline and the text of a page.
  page <...> --headings                Only the outline.
  page <...> --code                    Only the code blocks.
  portal-url <source path or URL>      The portal link for a page.

Uses only the Python standard library (Python 3.9 or later).
"""

import argparse
import html.parser
import json
import os
import re
import sys
import tempfile
import time
import urllib.error
import urllib.request

TOC_BASE = "https://developer.doc.config.autodesk.com/bPlouYTd/"
PAGE_BASE = "https://developer.doc.autodesk.com/bPlouYTd/"
PORTAL_BASE = "https://aps.autodesk.com/en/docs/"
REFERENCES_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
SOURCES_FILE = os.path.join(REFERENCES_DIR, "sources.md")
CACHE_DIR = os.path.join(tempfile.gettempdir(), "aps-docs-cache")
CACHE_SECONDS = 24 * 60 * 60
USER_AGENT = "aps-docs-skill/1.0 (+https://github.com/tylerwarner33/claude-plugin)"


class FetchError(Exception):
    pass


def fetch(url):
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            return response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as error:
        raise FetchError(f"HTTP {error.code} for {url}") from error
    except urllib.error.URLError as error:
        raise FetchError(f"Cannot reach {url}: {error.reason}") from error


def is_missing(error):
    """The doc storage returns 403, not 404, for a file that does not exist."""
    return "HTTP 403" in str(error) or "HTTP 404" in str(error)


# ---------------------------------------------------------------- Sources

def source_rows(text, match=None):
    """Return the lines of references/sources.md to show. With match, return
    only the table rows that match, each under the header of its table."""
    if not match:
        return text.rstrip("\n").splitlines()
    pattern = re.compile(match, re.IGNORECASE)
    result, header, header_shown = [], [], False
    for line in text.splitlines():
        if not line.startswith("|"):
            header, header_shown = [], False
            continue
        if not header or (len(header) == 1 and set(line) <= set("|-: ")):
            header.append(line)  # The header row and the separator row
            continue
        if pattern.search(line):
            if not header_shown:
                result.extend([""] + header if result else header)
                header_shown = True
            result.append(line)
    return result


def read_reference(name):
    """Return the text of a file in references/. The skill reads these files
    through the script, so that the skill's Bash rule covers each read. A Read
    of a file outside the working folder (the plugin cache) can need approval."""
    path = os.path.join(REFERENCES_DIR, name)
    try:
        with open(path, encoding="utf-8") as stream:
            return stream.read()
    except OSError as error:
        raise FetchError(f"Cannot read {path}: {error}") from error


def command_reference(args):
    match = getattr(args, "match", None)
    lines = source_rows(read_reference(args.reference_file), match)
    if match and not lines:
        print(f"No rows match '{match}'. Run {args.command} without --match to see all of them.")
        return
    print("\n".join(lines))


# ---------------------------------------------------------------- TOC

def load_toc(source_id, refresh=False):
    """Return the TOC of one API. A cached copy is used for 24 hours."""
    source_id = source_id[:-5] if source_id.endswith(".json") else source_id
    cache_file = os.path.join(CACHE_DIR, f"{source_id}.json")
    if not refresh and os.path.isfile(cache_file):
        if time.time() - os.path.getmtime(cache_file) < CACHE_SECONDS:
            with open(cache_file, encoding="utf-8") as stream:
                return json.load(stream)
    try:
        text = fetch(f"{TOC_BASE}{source_id}.json")
    except FetchError as error:
        if is_missing(error):
            raise FetchError(
                f"No TOC for source ID '{source_id}'. Run the sources command to "
                "list the IDs. IDs are case-sensitive and include the version "
                "(ex. data_v2)."
            ) from error
        raise
    toc = json.loads(text)
    try:
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(cache_file, "w", encoding="utf-8") as stream:
            stream.write(text)
    except OSError:
        pass  # The cache is optional.
    return toc


def walk(node, chain=()):
    """Yield (node, url_path chain) for each node under node. The portal leaves out
    an empty url_path, and a url_path that repeats its parent's (ex. the page
    get-3-legged-token-pkce under the group get-3-legged-token-pkce)."""
    for child in node.get("children", []) or []:
        part = child.get("url_path") or ""
        keep = part and (not chain or chain[-1] != part)
        child_chain = chain + ((part,) if keep else ())
        yield child, child_chain
        yield from walk(child, child_chain)


def portal_url_from_chain(toc, chain):
    parts = [toc.get("url_path", ""), toc.get("doc_version", "")] + list(chain)
    return PORTAL_BASE + "/".join(p for p in parts if p) + "/"


def pages(toc):
    """Yield a dict for each node that has a page (a 'source')."""
    for node, chain in walk(toc):
        if node.get("source"):
            yield {
                "name": node.get("display_name", ""),
                "source": node["source"],
                "portal": portal_url_from_chain(toc, chain),
            }


def find_section(toc, url_path):
    for node, _ in walk(toc):
        if node.get("url_path") == url_path:
            return node
    return None


def format_page(page):
    return f"- {page['name']}\n  source: {page['source']}\n  portal: {page['portal']}"


def command_toc(args):
    toc = load_toc(args.source_id, refresh=args.refresh)
    print(f"# {toc.get('api_name', args.source_id)} ({toc.get('doc_version', '')})")
    if args.match or args.all:
        pattern = re.compile(args.match or ".", re.IGNORECASE)
        found = [p for p in pages(toc) if pattern.search(p["name"]) or pattern.search(p["source"])]
        for page in found[: args.limit]:
            print(format_page(page))
        print(f"\n{len(found)} pages match." + (f" Showing {args.limit}." if len(found) > args.limit else ""))
        return
    root = toc
    if args.section:
        root = find_section(toc, args.section)
        if root is None:
            raise FetchError(f"No section with url_path '{args.section}'. Run toc without --section to list them.")
    for child in root.get("children", []) or []:
        count = sum(1 for _ in walk(child))
        line = f"- {child.get('display_name', '')} [url_path: {child.get('url_path', '')}]"
        if child.get("source"):
            line += f"\n  source: {child['source']}"
        if count:
            line += f"\n  ({count} items below)"
        print(line)


# ---------------------------------------------------------------- Pages

def source_path(value):
    """Accept a source path or a full CDN URL, and return the source path."""
    marker = "bPlouYTd/"
    if marker in value:
        value = value.split(marker, 1)[1]
    return value.split("?", 1)[0].split("#", 1)[0].lstrip("/")


def guess_source_id(path):
    """Guess the TOC source ID from a source path (ex. data/v2/... -> data_v2)."""
    segments = path.split("/")
    if len(segments) >= 3 and re.search(r"-\d+$", segments[0]):
        return f"{segments[1]}_{segments[2]}"
    return None


def portal_url_from_path(path):
    """Build a portal URL from the source path only. This is a guess: the portal
    path can differ from the source path (ex. a page under 'overview/' that the
    portal shows under 'developers_guide/'). Prefer portal_url()."""
    segments = path.split("/")
    if segments and re.search(r"-\d+$", segments[0]):
        segments = segments[1:]  # The repo slug, ex. A360-platform-viewing-docs-master-1064
    if len(segments) < 3:
        return None
    api, version, rest = segments[0], segments[1], segments[2:]
    folders, page = rest[:-1], rest[-1]
    if api in folders:
        folders.remove(api)  # A duplicate api-name folder, ex. reference/http/model-derivative/
    page = re.sub(r"\.html?$", "", page)
    return PORTAL_BASE + "/".join([api, version] + folders + [page]) + "/"


def portal_url(path, source_id=None, refresh=False):
    """Return (url, exact). exact is True when the URL comes from the TOC."""
    source_id = source_id or guess_source_id(path)
    if source_id:
        try:
            toc = load_toc(source_id, refresh=refresh)
        except FetchError:
            toc = None
        if toc:
            for page in pages(toc):
                if page["source"] == path:
                    return page["portal"], True
    return portal_url_from_path(path), False


class TextExtractor(html.parser.HTMLParser):
    """Turn a documentation page into plain text with a small set of markers:
    '#' for headings, '- ' for list items, ' | ' between table cells, and fenced
    blocks for <pre>. Each block is one line, so table cells are not repeated."""

    SKIP = {"script", "style", "noscript", "svg"}
    BLOCKS = {"p", "div", "section", "article", "li", "tr", "dt", "dd", "blockquote",
              "h1", "h2", "h3", "h4", "h5", "h6", "pre", "table", "ul", "ol", "br", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.lines = []
        self.headings = []
        self.code_blocks = []
        self.buffer = []
        self.skip_depth = 0
        self.pre_depth = 0
        self.prefix = ""
        self.heading_level = 0

    def flush(self):
        text = "".join(self.buffer)
        self.buffer = []
        if self.pre_depth:
            return
        text = re.sub(r"\s+", " ", text).strip(" |")
        if not text:
            self.prefix = ""
            return
        line = self.prefix + text
        if self.heading_level:
            self.headings.append((self.heading_level, text))
        if not self.lines or self.lines[-1] != line:
            self.lines.append(line)
        self.prefix = ""

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip_depth += 1
            return
        if self.skip_depth:
            return
        if tag == "pre":
            self.flush()
            self.pre_depth += 1
            return
        if tag in self.BLOCKS:
            self.flush()
            if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                self.heading_level = int(tag[1])
                self.prefix = "#" * self.heading_level + " "
            elif tag == "li":
                self.prefix = "- "
        elif tag in {"td", "th"} and self.buffer:
            self.buffer.append(" | ")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip_depth = max(0, self.skip_depth - 1)
            return
        if self.skip_depth:
            return
        if tag == "pre" and self.pre_depth:
            self.pre_depth -= 1
            code = "".join(self.buffer).strip("\n")
            self.buffer = []
            if code.strip():
                self.code_blocks.append(code)
                self.lines.append("```\n" + code + "\n```")
            return
        if tag in self.BLOCKS:
            self.flush()
            if tag in {"h1", "h2", "h3", "h4", "h5", "h6"}:
                self.heading_level = 0

    def handle_data(self, data):
        if not self.skip_depth:
            self.buffer.append(data)

    def close(self):
        super().close()
        self.flush()


def extract(html_text):
    parser = TextExtractor()
    parser.feed(html_text)
    parser.close()
    return parser


def command_page(args):
    path = source_path(args.path)
    url = PAGE_BASE + path
    try:
        html_text = fetch(url)
    except FetchError as error:
        if is_missing(error):
            raise FetchError(
                f"Page not found: {url}. The docs were probably deployed again, and the "
                "repo slug in the path changed. Run the toc command again to get the current path."
            ) from error
        raise
    parsed = extract(html_text)
    link, exact = portal_url(path, args.source_id, refresh=args.refresh)
    print(f"Source: {url}")
    if link:
        print(f"Portal: {link}" + ("" if exact else " (guessed from the source path, not found in the TOC)"))
    print()
    if args.code:
        for block in parsed.code_blocks:
            print("```\n" + block + "\n```\n")
        if not parsed.code_blocks:
            print("No code blocks on this page.")
        return
    print("## Outline")
    for level, text in parsed.headings:
        print("  " * max(0, level - 1) + "- " + text)
    if args.headings:
        return
    print("\n## Text")
    text = "\n".join(parsed.lines)
    if len(text) > args.max_chars:
        text = text[: args.max_chars] + f"\n\n[Cut at {args.max_chars} characters. Use --max-chars for more, or --code for the code blocks.]"
    print(text)


def command_portal_url(args):
    path = source_path(args.path)
    link, exact = portal_url(path, args.source_id, refresh=args.refresh)
    if not link:
        raise FetchError(f"Cannot build a portal URL from '{path}'.")
    print(link + ("" if exact else "  (guessed from the source path, not found in the TOC)"))


# ---------------------------------------------------------------- Main

def build_parser():
    parser = argparse.ArgumentParser(description="Read the APS documentation from its static sources.")
    parser.add_argument("--refresh", action="store_true", help="Ignore the cached TOC files.")
    # Also accept --refresh after the command. SUPPRESS keeps a value given before it.
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--refresh", action="store_true", default=argparse.SUPPRESS, help="Ignore the cached TOC files.")
    commands = parser.add_subparsers(dest="command", required=True)

    sources = commands.add_parser("sources", help="List the source IDs, and which API answers which question.")
    sources.add_argument("--match", help="Show only the table rows that match this regex (case-insensitive).")
    sources.set_defaults(func=command_reference, reference_file="sources.md")

    glossary = commands.add_parser("glossary", help="List APS terms and acronyms.")
    glossary.add_argument("--match", help="Show only the table rows that match this regex (case-insensitive).")
    glossary.set_defaults(func=command_reference, reference_file="glossary.md")

    example = commands.add_parser("example", help="Show a worked example of the method.")
    example.set_defaults(func=command_reference, reference_file="worked-example.md")

    toc = commands.add_parser("toc", parents=[common], help="Read the table of contents of an API.")
    toc.add_argument("source_id", help="A source ID from references/sources.md (ex. data_v2).")
    toc.add_argument("--section", help="Show the children of the node with this url_path.")
    toc.add_argument("--match", help="Show all pages whose name or source path match this regex.")
    toc.add_argument("--all", action="store_true", help="Show all pages.")
    toc.add_argument("--limit", type=int, default=100, help="The most pages to show (default 100).")
    toc.set_defaults(func=command_toc)

    page = commands.add_parser("page", parents=[common], help="Read a documentation page.")
    page.add_argument("path", help="A source path from the TOC, or a full CDN URL.")
    page.add_argument("--headings", action="store_true", help="Show only the outline.")
    page.add_argument("--code", action="store_true", help="Show only the code blocks.")
    page.add_argument("--source-id", help="The TOC source ID, when the guess from the path is wrong.")
    page.add_argument("--max-chars", type=int, default=30000, help="The most text characters (default 30000).")
    page.set_defaults(func=command_page)

    portal = commands.add_parser("portal-url", parents=[common], help="Get the portal link for a page.")
    portal.add_argument("path", help="A source path from the TOC, or a full CDN URL.")
    portal.add_argument("--source-id", help="The TOC source ID, when the guess from the path is wrong.")
    portal.set_defaults(func=command_portal_url)
    return parser


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    try:
        args.func(args)
    except FetchError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
