"""New Trustpilot reviews of a list of companies, appended to one CSV.

Reads domains.txt (one company domain per line, e.g. wise.com), reads the
newest reviews of each company and appends only the reviews whose id is not in
the CSV yet. Run it daily from cron:

    0 8 * * *  cd /path/to/here && python review_monitor.py --domains domains.txt

Needs a login (`trustpilot-scraper login`) or QUANTICDATA_API_KEY in the environment.
"""

import argparse
import csv
import os
from datetime import datetime, timezone

from quanticdata_trustpilot_scraper import TrustpilotScraper

FIELDS = ["checked_at", "domain", "company", "id", "date", "rating", "title", "text", "verification_level",
          "reviewer_country", "language", "reply", "reply_date", "url"]


def seen_ids(path):
    if not os.path.exists(path):
        return set()
    with open(path, newline="", encoding="utf-8") as fh:
        return {row["id"] for row in csv.DictReader(fh) if row.get("id")}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--domains", default="domains.txt", help="file with one company domain per line")
    parser.add_argument("--per-company", type=int, default=50, help="newest reviews to read per company (max 100)")
    parser.add_argument("--out", default="trustpilot_reviews.csv")
    args = parser.parse_args()

    with open(args.domains, encoding="utf-8") as fh:
        domains = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

    trustpilot = TrustpilotScraper()
    seen = seen_ids(args.out)
    checked_at = datetime.now(timezone.utc).isoformat(timespec="seconds")
    new_file = not os.path.exists(args.out)
    added = 0
    with open(args.out, "a", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=FIELDS, extrasaction="ignore")
        if new_file:
            writer.writeheader()
        for domain in domains:
            run = trustpilot.reviews(domain, sort="recency", max_results=args.per_company)
            fresh = [r for r in run if r.get("id") and r["id"] not in seen]
            for review in fresh:
                writer.writerow({"checked_at": checked_at, "domain": domain, **review})
                seen.add(review["id"])
            low = sum(1 for r in fresh if r.get("rating") is not None and r["rating"] <= 2)
            print(f"{domain}: {len(fresh)} new reviews, {low} of them at 1 or 2 stars")
            added += len(fresh)
    print(f"{added} new reviews appended to {args.out}")


if __name__ == "__main__":
    main()
