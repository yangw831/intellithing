#!/usr/bin/env python3
"""Validate the static IntelliThing blog before publication."""

import json
import sys
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parent.parent
BLOG = ROOT / "blog"
PUBLIC_PAGES = [
    BLOG / "index.html",
    BLOG / "merchant-account-managers-qbr-preparation.html",
    BLOG / "usdt-usdc-market-fitness.html",
    BLOG / "ai-driven-commerce-card-issuers-payment-providers.html",
    ROOT / "contact.html",
]
ARTICLE_PAGES = PUBLIC_PAGES[1:4]
PUBLIC_URLS = {
    "https://www.intellithing.com/blog/",
    "https://www.intellithing.com/blog/merchant-account-managers-qbr-preparation.html",
    "https://www.intellithing.com/blog/usdt-usdc-market-fitness.html",
    "https://www.intellithing.com/blog/ai-driven-commerce-card-issuers-payment-providers.html",
    "https://www.intellithing.com/contact.html",
}
ARTICLE_URLS = PUBLIC_URLS - {
    "https://www.intellithing.com/blog/",
    "https://www.intellithing.com/contact.html",
}


def normalize(value):
    return " ".join(value.split())


class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = []
        self.ids = set()
        self.hrefs = []
        self.robots = []
        self.json_ld = []
        self._json_parts = None
        self._faq_depth = 0
        self._faq_tag = None
        self._faq_parts = []
        self._faq_current = {}
        self.faqs = []

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)
        classes = set(attributes.get("class", "").split())

        if "id" in attributes:
            self.ids.add(attributes["id"])
        if tag == "a" and "href" in attributes:
            self.hrefs.append(attributes["href"])
        if tag == "link" and attributes.get("rel") == "canonical":
            self.canonical.append(attributes.get("href"))
        if tag == "meta" and attributes.get("name") == "robots":
            self.robots.append(attributes.get("content", ""))
        if tag == "script" and attributes.get("type") == "application/ld+json":
            self._json_parts = []

        if "faq-item" in classes:
            self._faq_depth = 1
            self._faq_current = {}
        elif self._faq_depth:
            self._faq_depth += 1
            if tag in {"h3", "p"}:
                self._faq_tag = tag
                self._faq_parts = []

    def handle_endtag(self, tag):
        if tag == "script" and self._json_parts is not None:
            self.json_ld.append(json.loads("".join(self._json_parts)))
            self._json_parts = None

        if self._faq_depth:
            if tag == self._faq_tag:
                self._faq_current[self._faq_tag] = normalize("".join(self._faq_parts))
                self._faq_tag = None
                self._faq_parts = []
            self._faq_depth -= 1
            if self._faq_depth == 0:
                self.faqs.append(self._faq_current)
                self._faq_current = {}

    def handle_data(self, data):
        if self._json_parts is not None:
            self._json_parts.append(data)
        if self._faq_tag:
            self._faq_parts.append(data)


def parse_page(path):
    parser = PageParser()
    parser.feed(path.read_text(encoding="utf-8"))
    return parser


def graph_items(doc):
    if "@graph" in doc:
        return doc["@graph"]
    return [doc]


def resolve_local_link(page, href):
    parsed = urlparse(href)
    if parsed.scheme or href.startswith(("#", "mailto:", "tel:")):
        return None
    target = (page.parent / parsed.path).resolve()
    if parsed.path.endswith("/") or target.is_dir():
        target = target / "index.html"
    return target


def main():
    errors = []

    for page in PUBLIC_PAGES:
        parsed = parse_page(page)

        if len(parsed.canonical) != 1:
            errors.append(f"{page}: expected exactly one canonical URL")
        if any("noindex" in value.lower() for value in parsed.robots):
            errors.append(f"{page}: public page contains noindex")
        if not parsed.json_ld:
            errors.append(f"{page}: missing JSON-LD")

        for href in parsed.hrefs:
            if href.startswith("#") and href[1:] not in parsed.ids:
                errors.append(f"{page}: broken fragment {href}")
            target = resolve_local_link(page, href)
            if target and not target.exists():
                errors.append(f"{page}: missing local target for {href}")

    for page in ARTICLE_PAGES:
        parsed = parse_page(page)
        items = [item for doc in parsed.json_ld for item in graph_items(doc)]
        types = {item.get("@type") for item in items}

        for required in {"Person", "Organization", "BlogPosting", "BreadcrumbList", "FAQPage"}:
            if required not in types:
                errors.append(f"{page}: missing {required} structured data")

        faq_pages = [item for item in items if item.get("@type") == "FAQPage"]
        if faq_pages:
            schema_faqs = [
                {
                    "h3": normalize(item["name"]),
                    "p": normalize(item["acceptedAnswer"]["text"]),
                }
                for item in faq_pages[0].get("mainEntity", [])
            ]
            if schema_faqs != parsed.faqs:
                errors.append(f"{page}: visible FAQs do not match FAQPage schema")

    template = parse_page(BLOG / "article-template.html")
    if not any("noindex" in value.lower() for value in template.robots):
        errors.append("article-template.html: reusable template must remain noindex")

    sitemap = ET.parse(ROOT / "sitemap.xml")
    sitemap_urls = {
        node.text
        for node in sitemap.findall("{http://www.sitemaps.org/schemas/sitemap/0.9}url/"
                                     "{http://www.sitemaps.org/schemas/sitemap/0.9}loc")
    }
    missing_sitemap = PUBLIC_URLS - sitemap_urls
    if missing_sitemap:
        errors.append(f"sitemap.xml: missing {sorted(missing_sitemap)}")

    feed = ET.parse(BLOG / "feed.xml")
    feed_links = {node.text for node in feed.findall("./channel/item/link")}
    if feed_links != ARTICLE_URLS:
        errors.append("feed.xml: item links do not exactly match published articles")

    if errors:
        for error in errors:
            print(f"ERROR: {error}")
        return 1

    print("Site validation passed: 5 public pages, 3 articles, contact page, sitemap, RSS, schema, FAQs, and links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
