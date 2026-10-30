"""Star-rating breakdown of the latest Trustpilot reviews of several companies.

    python rating_breakdown.py wise.com booking.com --reviews 100

For each company it reads the newest --reviews reviews and writes the share of
each star rating, the share marked verified, the share with a company reply
and the average rating of that window, next to the TrustScore and total review
count shown on the company's profile.
"""

import argparse

from quanticdata_trustpilot_scraper import TrustpilotScraper, write


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("domains", nargs="+", help="company domains, e.g. wise.com")
    parser.add_argument("--reviews", type=int, default=100, help="newest reviews to read per company (max 100)")
    parser.add_argument("--out", default="rating_breakdown.csv")
    args = parser.parse_args()

    trustpilot = TrustpilotScraper()
    rows = []
    for domain in args.domains:
        run = trustpilot.reviews(domain, sort="recency", max_results=args.reviews)
        rated = [r for r in run if r.get("rating")]
        if not rated:
            print(f"{domain}: no reviews returned")
            continue
        n = len(rated)
        row = {
            "domain": domain,
            "company": (rated[0].get("company") or "").strip(),
            "trust_score": rated[0].get("company_trust_score"),
            "total_reviews": rated[0].get("company_reviews"),
            "window": n,
            "first_date": min((r.get("date") or "")[:10] for r in rated),
            "average_rating": round(sum(r["rating"] for r in rated) / n, 2),
        }
        for star in range(5, 0, -1):
            row[f"share_{star}_star"] = round(sum(1 for r in rated if r["rating"] == star) / n, 3)
        row["share_verified"] = round(sum(1 for r in rated if r.get("verified")) / n, 3)
        row["share_replied"] = round(sum(1 for r in rated if r.get("reply")) / n, 3)
        rows.append(row)
        print(f"{domain}: TrustScore {row['trust_score']}, last {n} reviews average {row['average_rating']}, "
              f"{row['share_1_star']:.0%} one-star, {row['share_replied']:.0%} replied")

    write(rows, args.out)
    print(f"{len(rows)} companies written to {args.out}")


if __name__ == "__main__":
    main()
