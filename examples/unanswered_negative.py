"""One- and two-star Trustpilot reviews of a company that have no reply yet.

    python unanswered_negative.py yourcompany.com --per-rating 100

Reads the newest one-star and two-star reviews of the company and writes the
ones without a company reply, oldest first, with date, rating, title, text,
reviewer country and the review link: a work queue for a support team.
"""

import argparse

from quanticdata_trustpilot_scraper import TrustpilotScraper, write

FIELDS = ["date", "rating", "title", "text", "reviewer_country", "language", "verification_level", "url"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domain", help="your company's domain, e.g. yourcompany.com")
    parser.add_argument("--per-rating", type=int, default=100, help="newest reviews to read per star rating (max 100)")
    parser.add_argument("--out", default="unanswered_negative.csv")
    args = parser.parse_args()

    trustpilot = TrustpilotScraper()
    queue = []
    for stars in (1, 2):
        run = trustpilot.reviews(args.domain, stars=stars, sort="recency", max_results=args.per_rating)
        open_ones = [r for r in run if not r.get("reply")]
        print(f"{stars}-star: {len(run)} read, {len(open_ones)} without a reply")
        queue.extend(open_ones)

    queue.sort(key=lambda r: r.get("date") or "")
    write([{k: r.get(k) for k in FIELDS} for r in queue], args.out)
    print(f"{len(queue)} reviews written to {args.out}")


if __name__ == "__main__":
    main()
