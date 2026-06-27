# IntelliThing Insights workspace

This directory contains the published IntelliThing Insights pages, shared styling,
research notes, RSS feed, and reusable article template. Published pages are listed
in `sitemap.xml`; only the reusable template remains marked `noindex`.

## Files

- `index.html`: Published Insights landing page
- `blog.css`: Shared index and article styles
- `article-template.html`: Copy this file when starting an article
- `feed.xml`: RSS feed containing published articles only

## Publishing checklist

1. Replace the title, description, canonical URL, topic, headline, dek, and byline.
2. Put a self-contained 40–60-word answer directly below the article header.
3. Add anchored contents using descriptive section titles.
4. Add Open Graph and social-card metadata.
5. Add visible breadcrumbs and matching `BlogPosting`, `BreadcrumbList`, author,
   and—only when supported by visible content—`FAQPage` structured data.
6. Support quantitative claims with dated sources or a transparent methodology note.
7. Include concise visible FAQs that match the structured data exactly.
8. Include the author card and update credentials when the subject requires it.
9. Use a specific URL such as `merchant-account-manager-qbr-challenges.html`.
10. Remove `noindex` only after editorial review.
11. Add the published article to `index.html`, `sitemap.xml`, and the RSS feed.
12. Add contextual links to and from the relevant product page.
13. Verify desktop and mobile layout, metadata, links, and schema.

## Initial account-manager pain inventory

The audience is an account manager at a credit card issuer—not a merchant's
internal operations team.

- Portfolio scale: several merchant reviews compete for the same preparation window.
- Fragmented inputs: volume, authorization, disputes, chargebacks, and commercial
  context may live in different exports or systems.
- KPI reconciliation: definitions, periods, currencies, and comparison baselines
  need to be made consistent.
- Diagnosis: the account manager must distinguish meaningful changes from noise.
- Executive narrative: raw metrics must become a concise explanation of what
  happened, why it matters, and what should happen next.
- Merchant-specific context: a standard template must still reflect the merchant's
  business model, priorities, and recent events.
- Deck production: formatting tables, charts, commentary, and slides consumes time
  without necessarily improving the underlying analysis.
- Review and governance: sensitive merchant data and externally presented claims
  need human verification.
- Follow-through: agreed actions can become detached from the next quarter's review.

## Initial stablecoin thesis

Avoid framing USDT versus USDC as a single scoreboard. Evaluate fitness by job:

- Distribution and market access
- Trading liquidity and settlement availability
- Geographic reach
- Institutional and enterprise adoption
- Regulatory and reserve expectations
- Banking, wallet, exchange, and developer integrations
- Suitability for payments, treasury, trading, remittance, and agentic commerce

The working argument is that USDT and USDC demonstrate different kinds of market
fitness. Claims and figures must be sourced and dated during article research.
