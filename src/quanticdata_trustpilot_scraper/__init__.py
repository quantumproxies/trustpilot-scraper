"""Trustpilot Scraper: Trustpilot scraper for Python and the command line: public reviews of any company by its domain, with rating, title, text, dates, verification label, reviewer country and the company reply, plus TrustScore and review count, as JSON or CSV. Free and open source; sign in with your QuanticData account, no proxies or headless browser to run.

    from quanticdata_trustpilot_scraper import TrustpilotScraper

    scraper = TrustpilotScraper()   # saved login (`trustpilot-scraper login`) or QUANTICDATA_API_KEY
    run = scraper.reviews(...)   # public Trustpilot reviews of a company
"""

from typing import Any, Dict, Optional, Sequence, Union

from ._qd.client import Client, Run
from ._qd.errors import (APIError, AuthError, InsufficientCredit, InvalidInput, JobFailed, JobTimeout,
                         QuanticDataError, RateLimited)
from ._qd.output import write

__version__ = "0.1.0"
__all__ = ["TrustpilotScraper", "Run", "write", "APIError", "AuthError", "InsufficientCredit", "InvalidInput",
           "JobFailed", "JobTimeout", "QuanticDataError", "RateLimited", "__version__"]


def _as_list(value: Any) -> Any:
    if value is None or isinstance(value, (list, tuple)):
        return list(value) if value is not None else None
    return [value]


class TrustpilotScraper:
    """Trustpilot Scraper on the QuanticData Data API.

    Every method runs one collector and returns a :class:`Run`: iterate it for the
    rows (plain dicts, typed in ``types``), or save it with ``to_csv()``,
    ``to_json()``, ``to_jsonl()`` or ``to_dataframe()``.
    """

    def __init__(self, api_key: Optional[str] = None, *, timeout: float = 180.0) -> None:
        self.client = Client(api_key, user_agent="trustpilot-scraper/0.1.0 (+https://github.com/quantumproxies/trustpilot-scraper)", timeout=timeout)

    def reviews(
        self, domain: str,
        *,
        sort: Optional[str] = None,
        stars: Optional[int] = None,
        country: Optional[str] = None,
        max_results: Optional[int] = None,
        wait: bool = True,
        timeout: float = 900.0,
    ) -> Run:
        """Public Trustpilot reviews of any company — rating, text, dates, verification and the company reply.

        Args:
            domain: The reviewed company's domain, e.g. wise.com (not the Trustpilot URL).
            sort: Review order (default recency). One of: recency, relevance.
            stars: Only reviews with this star rating (1–5). Omit for all.
            country: Country to run the request from, as an ISO 3166-1 alpha-2 code (us, gb, de...).
            max_results: How many reviews to deliver at most (1–100). You pay only for delivered reviews.
            wait: False starts the run in the background and returns its id at once.
            timeout: seconds to wait for a background run before giving up.

        Returns up to 100 rows, one per review: see ``types.TrustpilotReviewsRow``.
        """
        payload = {
            "domain": domain,
            "sort": sort,
            "stars": stars,
            "country": country,
            "max_results": max_results,
        }
        return self.client.run_collector("trustpilot_reviews", payload, wait=wait, timeout=timeout)
