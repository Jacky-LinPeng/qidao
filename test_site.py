"""Check the publishable static site's internal links and basic accessibility metadata."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import re

ROOT = Path(__file__).resolve().parent


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__(convert_charrefs=True)
        self.path = path
        self.links = []
        self.ids = set()
        self.h1 = 0
        self.main = 0
        self.title = 0
        self.lang = False
        self.viewport = False
        self.wallpaper_count = 0
        self.stack = []
        self.feed(path.read_text(encoding="utf-8"))
        assert not self.stack, f"Unclosed tags: {path.name}: {self.stack}"

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "figure" and "wallpaper" in attrs.get("class", "").split():
            self.wallpaper_count += 1
        if tag not in {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "param", "source", "track", "wbr"}:
            self.stack.append(tag)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f"Duplicate ID: {self.path.name} #{attrs['id']}"
            self.ids.add(attrs["id"])
        self.h1 += tag == "h1"
        self.main += tag == "main"
        self.title += tag == "title"
        if tag == "html":
            self.lang = attrs.get("lang") == "zh-CN"
        if tag == "meta" and attrs.get("name") == "viewport":
            self.viewport = "width=device-width" in attrs.get("content", "")
        if tag == "img":
            assert "alt" in attrs, f"Missing image alt: {self.path.name}"
            assert "width" in attrs and "height" in attrs, f"Missing image dimensions: {self.path.name}"
        for attr in ("href", "src"):
            if attr in attrs:
                self.links.append(attrs[attr])
        assert tag not in {"script", "iframe", "form"}, f"Unexpected active content: {self.path.name}"

    def handle_endtag(self, tag):
        assert self.stack and self.stack.pop() == tag, f"Mismatched closing tag: {self.path.name}: {tag}"


def check():
    pages = {p.resolve(): Page(p) for p in ROOT.glob("*.html")}
    assert len(pages) == 3, "Expected marketing, privacy and support pages"
    assert pages[ROOT / "index.html"].wallpaper_count == 9, "Expected nine category previews"
    checked = 0
    external = set()
    for path, page in pages.items():
        assert (page.h1, page.main, page.title) == (1, 1, 1), f"Invalid landmarks/title: {path.name}"
        assert page.lang and page.viewport, f"Missing language/viewport: {path.name}"
        for link in page.links:
            url = urlsplit(link)
            if url.scheme or url.netloc:
                assert url.scheme in {"https", "mailto"}, f"Unexpected URL scheme: {link}"
                external.add(link)
                continue
            target = (path.parent / unquote(url.path)).resolve() if url.path else path
            assert target.is_relative_to(ROOT), f"Link escapes publish root: {link}"
            assert target.is_file(), f"Missing target: {path.name} -> {link}"
            if url.fragment:
                assert target in pages and unquote(url.fragment) in pages[target].ids, f"Missing anchor: {link}"
            checked += 1
    css = (ROOT / "styles.css").read_text(encoding="utf-8")
    assert "prefers-reduced-motion" in css and ":focus-visible" in css
    assert not re.search(r"@import|url\(\s*['\"]?https?://", css), "External CSS request"
    assert (ROOT / ".nojekyll").exists()
    image_bytes = sum(p.stat().st_size for p in (ROOT / "assets").glob("*"))
    print(f"PASS: {len(pages)} pages; {checked} local references; {len(external)} distinct external/mail links")
    print(f"PASS: headings, landmarks, image alt/dimensions, reduced motion, keyboard focus")
    print("PASS: nine wallpaper category previews")
    print(f"PASS: no script/iframe/form or external CSS dependencies; image assets {image_bytes:,} bytes")


if __name__ == "__main__":
    check()
