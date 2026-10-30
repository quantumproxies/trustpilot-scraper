"""Row types of each command, for editors and type checkers (rows are plain dicts)."""

from typing import Any, Dict, List, Optional

try:  # Python 3.8+
    from typing import TypedDict
except ImportError:  # pragma: no cover
    from typing_extensions import TypedDict  # type: ignore


class TrustpilotReviewsRow(TypedDict, total=False):
    """One row of `trustpilot-scraper reviews` (trustpilot_reviews v1.2.2)."""

    rank: int
    """1-based position in the requested order."""
    page: int
    """Profile page the review came from."""
    id: Optional[str]
    """Trustpilot review id."""
    title: Optional[str]
    """Review title."""
    text: Optional[str]
    """Full review text."""
    rating: Optional[int]
    """Star rating (1–5)."""
    date: Optional[str]
    """Publish date (ISO 8601)."""
    experience_date: Optional[str]
    """Date of the reviewed experience (ISO 8601)."""
    reviewer: Optional[str]
    """Reviewer display name."""
    reviewer_country: Optional[str]
    """Reviewer country code."""
    reviewer_reviews: Optional[int]
    """How many reviews the reviewer has written."""
    verified: bool
    """True when Trustpilot marks the review as verified."""
    likes: int
    """Useful votes on the review."""
    reply: Optional[str]
    """Company reply text, when present."""
    reply_date: Optional[str]
    """Company reply date (ISO 8601)."""
    url: Optional[str]
    """Direct link to the review."""
    language: Optional[str]
    """Language of the review (ISO code)."""
    source: Optional[str]
    """How the review was collected, as Trustpilot labels it (Organic, Invited…)."""
    verification_level: Optional[str]
    """Trustpilot's verification label for the review (verified, invited, not-verified…)."""
    updated_date: Optional[str]
    """When the reviewer last edited the review (ISO 8601), null when never."""
    reply_updated_date: Optional[str]
    """When the company last edited its reply (ISO 8601)."""
    reviewer_reviews_same_company: Optional[int]
    """How many reviews this reviewer has written about the same company."""
    company: Optional[str]
    """Reviewed company as Trustpilot names it."""
    company_trust_score: Optional[float]
    """The company's TrustScore at collection time."""
    company_reviews: Optional[int]
    """Total reviews on the company's profile at collection time."""
