# Trustpilot Scraper

[![ci](https://github.com/quantumproxies/trustpilot-scraper/actions/workflows/ci.yml/badge.svg)](https://github.com/quantumproxies/trustpilot-scraper/actions/workflows/ci.yml) ![python](https://img.shields.io/badge/python-3.9%2B-blue) ![license](https://img.shields.io/badge/license-MIT-green) ![dependencies](https://img.shields.io/badge/dependencies-none-brightgreen)

Scrape Trustpilot reviews from Python or the command line: the public reviews of any company by its domain, newest first or in Trustpilot's order, with star rating, title, full text, publish and experience dates, verification label, reviewer country and the company's reply, plus the company's TrustScore and total review count, as JSON or CSV. The code is free and open source (MIT). It runs on the QuanticData Data API, so there are no proxies to rotate and no headless browser to keep alive: sign in once and run a command.

```bash
pip install git+https://github.com/quantumproxies/trustpilot-scraper
trustpilot-scraper login
trustpilot-scraper reviews booking.com --sort recency --max-results 100 -o booking_reviews.csv
```

`login` opens the QuanticData sign-in page in your browser. New accounts get $2 of free usage every month, no card required: [create one](https://app.quanticdata.io/register?utm_source=github&utm_medium=readme&utm_campaign=trustpilot-scraper).

## What it scrapes

| Command | Input | Returns | Per run |
|---|---|---|---|
| `trustpilot-scraper reviews` | company domain | Rating, text, dates, verification and the company reply, 25 fields per row ([fields and price](https://quanticdata.io/collectors/trustpilot-scraper-api/?utm_source=github&utm_medium=readme&utm_campaign=trustpilot-scraper)) | up to 100 |

Pass the company's domain (`wise.com`, `booking.com`), not the Trustpilot URL. `--sort recency` (the default) gives the newest reviews first and `--sort relevance` Trustpilot's own order; `--stars 1` to `--stars 5` keeps one rating only. Every row also carries the company's name, TrustScore and total review count at collection time.

## Sample output

A real row from `trustpilot-scraper reviews booking.com --sort relevance --max-results 3` (2026-10-23):

```json
{
  "id": "6adab3b6d81099acab7d1fd5",
  "url": "https://www.trustpilot.com/reviews/6adab3b6d81099acab7d1fd5",
  "date": "2026-10-23T03:09:10.000Z",
  "page": 1,
  "rank": 3,
  "text": "Absolutely terrible. Paid for a flexible flight ticket...",
  "likes": 0,
  "reply": null,
  "title": "Absolutely terrible.",
  "rating": 1,
  "source": "Organic",
  "company": "Booking.com",
  "language": "en",
  "reviewer": "Lee",
  "verified": false,
  "reply_date": null,
  "updated_date": null,
  "company_reviews": 129196,
  "experience_date": "2026-10-22T00:00:00.000Z",
  "reviewer_country": "ES",
  "reviewer_reviews": 1,
  "reply_updated_date": null,
  "verification_level": "not-verified",
  "company_trust_score": 1.4,
  "reviewer_reviews_same_company": 1
}
```

## Python

```python
from quanticdata_trustpilot_scraper import TrustpilotScraper

trustpilot = TrustpilotScraper()  # saved login, or QUANTICDATA_API_KEY

latest = trustpilot.reviews("wise.com", sort="recency", max_results=100)
print(latest.rows[0]["company"], latest.rows[0]["company_trust_score"], latest.rows[0]["company_reviews"])
for r in latest:
    print((r["date"] or "")[:10], r["rating"], r["verification_level"], r["title"])
latest.to_csv("wise_reviews.csv")

one_star = trustpilot.reviews("wise.com", stars=1, max_results=50)
replied = sum(1 for r in one_star if r["reply"])
print(f"{replied} of {len(one_star)} one-star reviews have a company reply")
```

Each call returns a `Run`: iterate it for the rows (plain dicts), take `len()`, or save it with `to_csv()`, `to_json()`, `to_jsonl()` or `to_dataframe()` (pandas). Errors are specific: `InsufficientCredit`, `RateLimited`, `InvalidInput`, `JobFailed`, `AuthError`.

## Examples

- **Review monitoring**: Read the newest reviews of a list of companies every day and append only the ones you have not seen yet to a CSV, with rating, date and reply. See [`examples/review_monitor.py`](examples/review_monitor.py).
- **Rating breakdown**: For each company, the share of each star rating in its latest reviews, the share marked verified and the share with a company reply, next to its TrustScore. See [`examples/rating_breakdown.py`](examples/rating_breakdown.py).
- **Unanswered negative reviews**: List the one- and two-star reviews of your company that have no reply yet, oldest first, so a support team can work through them. See [`examples/unanswered_negative.py`](examples/unanswered_negative.py).

## Command line

Results print as a table; `-o file.csv`, `-o file.json` or `-o file.jsonl` writes a file. List inputs take `a b c`, `a,b,c`, `@file.txt` (one per line) or `-` (stdin). `--no-wait` starts a long run in the background and prints its id; `trustpilot-scraper run <id> -o out.csv` collects it later.

### `trustpilot-scraper reviews`

Public Trustpilot reviews of any company — rating, text, dates, verification and the company reply.

```
trustpilot-scraper reviews DOMAIN [options]
```

| Option | Type | Default | Description |
|---|---|---|---|
| `DOMAIN` | string |  | The reviewed company's domain, e.g. wise.com (not the Trustpilot URL). |
| `--sort` | recency / relevance | `recency` | Review order (default recency). |
| `--stars` | integer |  | Only reviews with this star rating (1–5). Omit for all. |
| `--country` | string |  | Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...). |
| `--max-results` | integer | `20` | How many reviews to deliver at most (1–100). You pay only for delivered reviews. |

## Output fields

<details><summary><code>trustpilot-scraper reviews</code>: 25 fields</summary>

| Field | Type | Description |
|---|---|---|
| `rank` | integer | 1-based position in the requested order. |
| `page` | integer | Profile page the review came from. |
| `id` | string or null | Trustpilot review id. |
| `title` | string or null | Review title. |
| `text` | string or null | Full review text. |
| `rating` | integer or null | Star rating (1–5). |
| `date` | string or null | Publish date (ISO 8601). |
| `experience_date` | string or null | Date of the reviewed experience (ISO 8601). |
| `reviewer` | string or null | Reviewer display name. |
| `reviewer_country` | string or null | Reviewer country code. |
| `reviewer_reviews` | integer or null | How many reviews the reviewer has written. |
| `verified` | boolean | True when Trustpilot marks the review as verified. |
| `likes` | integer | Useful votes on the review. |
| `reply` | string or null | Company reply text, when present. |
| `reply_date` | string or null | Company reply date (ISO 8601). |
| `url` | string or null | Direct link to the review. |
| `language` | string or null | Language of the review (ISO code). |
| `source` | string or null | How the review was collected, as Trustpilot labels it (Organic, Invited…). |
| `verification_level` | string or null | Trustpilot's verification label for the review (verified, invited, not-verified…). |
| `updated_date` | string or null | When the reviewer last edited the review (ISO 8601), null when never. |
| `reply_updated_date` | string or null | When the company last edited its reply (ISO 8601). |
| `reviewer_reviews_same_company` | integer or null | How many reviews this reviewer has written about the same company. |
| `company` | string or null | Reviewed company as Trustpilot names it. |
| `company_trust_score` | number or null | The company's TrustScore at collection time. |
| `company_reviews` | integer or null | Total reviews on the company's profile at collection time. |

</details>

## Sign-in and API keys

- `trustpilot-scraper login` signs you in with OAuth 2.1 and PKCE in the browser. The token is stored in `~/.config/quanticdata/credentials.json` (readable only by you) and refreshed automatically. One login serves every QuanticData tool on the machine.
- No browser on the machine (SSH, Docker, Colab): run `trustpilot-scraper login --no-browser`, open the link anywhere, then paste back the address the browser ends on.
- Scripts and CI: set `QUANTICDATA_API_KEY` to a key from the dashboard, or store one with `trustpilot-scraper login --api-key`.
- `trustpilot-scraper logout` revokes the token. The connection is listed under API keys in the dashboard as "API · QuanticData CLI"; deleting that key disconnects every machine that uses it.

## Pricing

The code is free and MIT-licensed. Runs are billed to your QuanticData account per delivered row, at the price shown on each collector page linked above; $2 of usage is free every month and failed runs are never billed. Plans with higher limits: [pricing](https://quanticdata.io/pricing/?utm_source=github&utm_medium=readme&utm_campaign=trustpilot-scraper).

## Other ways to call it

The same data over plain HTTP:

```bash
curl -X POST https://api.quanticdata.io/v1/scraper/collectors/trustpilot_reviews/run \
  -H "Authorization: Bearer $QUANTICDATA_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"input": {"domain": "booking.com", "sort": "relevance", "max_results": 3}}'
```

- [API reference](https://quanticdata.io/docs/?utm_source=github&utm_medium=readme&utm_campaign=trustpilot-scraper) with Python, Node, PHP and curl examples.
- [MCP server](https://quanticdata.io/mcp-server/?utm_source=github&utm_medium=readme&utm_campaign=trustpilot-scraper) to give Claude, Cursor or any MCP client the same tools.
- [n8n node](https://github.com/quantumproxies/n8n-nodes-quanticdata) for no-code workflows.

## FAQ

**Is this Trustpilot scraper free?**

The code is free and MIT-licensed. Scraping runs on your QuanticData account: $2 of usage is free every month with no card, then you pay per delivered row at the price shown on each collector page. Failed runs are never billed.

**Do I need proxies or a headless browser?**

No. You send a company's domain and get rows back; the requests run on QuanticData's side.

**Does it need a Trustpilot account?**

No. It reads public reviews only, the ones anyone can open without signing in. Reviews carry the reviewer's display name: you are responsible for respecting Trustpilot's terms and the data-protection rules that apply to how you use the data.

**How many reviews can one run return?**

Up to 100 reviews per run; ask for fewer with --max-results and you pay only for what is delivered. --stars and --sort pick which reviews those are.

**Can I export to CSV or Excel?**

Add -o reviews.csv (or .json, .jsonl). Every field is a plain value, so the CSV opens cleanly in Excel or Google Sheets.

**Can I run it on a schedule?**

Yes. Set QUANTICDATA_API_KEY in the environment and call the CLI or examples/review_monitor.py from cron, GitHub Actions or any scheduler.

## Related scrapers

- [Google Maps Scraper](https://github.com/quantumproxies/google-maps-scraper): Google Maps scraper for Python and the command line.
- [Reddit Scraper](https://github.com/quantumproxies/reddit-scraper): Reddit scraper for Python and the command line.

## License

MIT. Built and maintained by [QuanticData](https://quanticdata.io/?utm_source=github&utm_medium=readme&utm_campaign=trustpilot-scraper).
