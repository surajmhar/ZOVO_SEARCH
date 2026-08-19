import ipaddress
import re
import socket
import time
from urllib.parse import urljoin, urlparse

import requests
from bs4 import BeautifulSoup


REQUEST_TIMEOUT = 10

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (compatible; ZOVOSearchBot/1.0; "
        "+https://zovosearch.com)"
    )
}


class SEOAnalyzerError(Exception):
    """Custom exception for SEO analyzer errors."""
    pass


def normalize_url(url):
    """
    Normalize user URL.
    Example:
        google.com -> https://google.com
    """

    if not url:
        raise SEOAnalyzerError("Please enter a website URL.")

    url = url.strip()

    if not url.startswith(("http://", "https://")):
        url = f"https://{url}"

    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https"):
        raise SEOAnalyzerError("Only HTTP and HTTPS URLs are supported.")

    if not parsed.hostname:
        raise SEOAnalyzerError("Invalid website URL.")

    return url


def is_safe_public_url(url):
    """
    Prevent requests to localhost/private/internal IP addresses.
    This is important because analyzer accepts user-provided URLs.
    """

    parsed = urlparse(url)
    hostname = parsed.hostname

    if not hostname:
        return False

    blocked_hosts = {
        "localhost",
        "localhost.localdomain",
    }

    if hostname.lower() in blocked_hosts:
        return False

    try:
        addresses = socket.getaddrinfo(hostname, None)

        for address in addresses:
            ip_string = address[4][0]
            ip = ipaddress.ip_address(ip_string)

            if (
                ip.is_private
                or ip.is_loopback
                or ip.is_reserved
                or ip.is_link_local
                or ip.is_multicast
            ):
                return False

    except socket.gaierror:
        raise SEOAnalyzerError(
            "Unable to resolve this domain. Please check the URL."
        )

    return True


def fetch_page(url):
    """
    Fetch website HTML and measure response time.
    """

    if not is_safe_public_url(url):
        raise SEOAnalyzerError(
            "This URL cannot be analyzed."
        )

    try:
        start_time = time.perf_counter()

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=REQUEST_TIMEOUT,
            allow_redirects=True,
        )

        response_time = round(
            (time.perf_counter() - start_time) * 1000
        )

    except requests.exceptions.Timeout:
        raise SEOAnalyzerError(
            "The website took too long to respond."
        )

    except requests.exceptions.ConnectionError:
        raise SEOAnalyzerError(
            "Unable to connect to the website."
        )

    except requests.exceptions.RequestException:
        raise SEOAnalyzerError(
            "Unable to analyze this website."
        )

    final_url = response.url

    if not is_safe_public_url(final_url):
        raise SEOAnalyzerError(
            "The website redirected to an unsupported address."
        )

    if response.status_code >= 400:
        raise SEOAnalyzerError(
            f"Website returned HTTP status {response.status_code}."
        )

    content_type = response.headers.get(
        "Content-Type",
        ""
    ).lower()

    if "text/html" not in content_type:
        raise SEOAnalyzerError(
            "The provided URL does not return an HTML webpage."
        )

    return response, response_time


def extract_title(soup):
    title = soup.title.string.strip() if soup.title and soup.title.string else ""

    return {
        "text": title,
        "length": len(title),
        "exists": bool(title),
    }


def extract_meta_description(soup):
    tag = soup.find(
        "meta",
        attrs={"name": re.compile("^description$", re.I)}
    )

    description = ""

    if tag:
        description = tag.get("content", "").strip()

    return {
        "text": description,
        "length": len(description),
        "exists": bool(description),
    }


def extract_headings(soup):
    h1_tags = soup.find_all("h1")
    h2_tags = soup.find_all("h2")

    h1_values = [
        tag.get_text(" ", strip=True)
        for tag in h1_tags
    ]

    h2_values = [
        tag.get_text(" ", strip=True)
        for tag in h2_tags
    ]

    return {
        "h1_count": len(h1_values),
        "h1": h1_values,
        "h2_count": len(h2_values),
        "h2": h2_values,
    }


def extract_images(soup):
    images = soup.find_all("img")

    missing_alt = []

    for image in images:
        alt = image.get("alt")

        if alt is None or not alt.strip():
            missing_alt.append(
                image.get("src", "")
            )

    total = len(images)
    missing = len(missing_alt)

    optimized = total - missing

    return {
        "total": total,
        "with_alt": optimized,
        "missing_alt": missing,
        "missing_alt_images": missing_alt[:20],
    }


def extract_canonical(soup):
    canonical = soup.find(
        "link",
        rel=lambda value: (
            value
            and "canonical" in (
                value if isinstance(value, list)
                else [value]
            )
        ),
    )

    href = canonical.get("href", "").strip() if canonical else ""

    return {
        "exists": bool(href),
        "url": href,
    }


def extract_viewport(soup):
    viewport = soup.find(
        "meta",
        attrs={"name": re.compile("^viewport$", re.I)}
    )

    content = viewport.get("content", "").strip() if viewport else ""

    return {
        "exists": bool(content),
        "content": content,
    }


def extract_robots_meta(soup):
    robots = soup.find(
        "meta",
        attrs={"name": re.compile("^robots$", re.I)}
    )

    content = robots.get("content", "").strip() if robots else ""

    return {
        "exists": bool(content),
        "content": content,
        "noindex": "noindex" in content.lower(),
        "nofollow": "nofollow" in content.lower(),
    }


def extract_links(soup, page_url):
    internal_links = []
    external_links = []

    page_domain = urlparse(page_url).netloc.lower()

    for anchor in soup.find_all("a", href=True):
        href = anchor.get("href", "").strip()

        if not href:
            continue

        if href.startswith(("#", "mailto:", "tel:", "javascript:")):
            continue

        absolute_url = urljoin(page_url, href)

        parsed = urlparse(absolute_url)

        if parsed.scheme not in ("http", "https"):
            continue

        link_domain = parsed.netloc.lower()

        if link_domain == page_domain:
            internal_links.append(absolute_url)
        else:
            external_links.append(absolute_url)

    return {
        "internal": len(set(internal_links)),
        "external": len(set(external_links)),
        "total": len(
            set(internal_links + external_links)
        ),
    }


def extract_content_stats(soup):
    clone = BeautifulSoup(str(soup), "html.parser")

    for tag in clone(
        ["script", "style", "noscript", "svg"]
    ):
        tag.decompose()

    text = clone.get_text(" ", strip=True)

    words = re.findall(
        r"\b[\w'-]+\b",
        text,
        flags=re.UNICODE,
    )

    return {
        "word_count": len(words),
    }


def calculate_score(data):
    """
    Simple deterministic SEO score.

    This is NOT an AI-generated score.
    It is based on measurable on-page SEO signals.
    """

    score = 0

    title = data["title"]
    description = data["meta_description"]
    headings = data["headings"]
    images = data["images"]
    canonical = data["canonical"]
    viewport = data["viewport"]
    robots = data["robots"]
    content = data["content"]

    # Title — 15 points
    if title["exists"]:
        score += 8

        if 30 <= title["length"] <= 65:
            score += 7

    # Meta description — 15 points
    if description["exists"]:
        score += 8

        if 70 <= description["length"] <= 170:
            score += 7

    # H1 — 15 points
    if headings["h1_count"] == 1:
        score += 15
    elif headings["h1_count"] > 1:
        score += 7

    # H2 structure — 5 points
    if headings["h2_count"] >= 1:
        score += 5

    # Images — 10 points
    if images["total"] == 0:
        score += 10
    else:
        alt_ratio = (
            images["with_alt"]
            / images["total"]
        )

        score += round(alt_ratio * 10)

    # Canonical — 10 points
    if canonical["exists"]:
        score += 10

    # Mobile viewport — 10 points
    if viewport["exists"]:
        score += 10

    # HTTPS — 10 points
    if data["https"]:
        score += 10

    # Indexability — 5 points
    if not robots["noindex"]:
        score += 5

    # Content — 5 points
    if content["word_count"] >= 300:
        score += 5
    elif content["word_count"] >= 150:
        score += 3

    return min(score, 100)


def build_recommendations(data):
    recommendations = []

    if not data["title"]["exists"]:
        recommendations.append({
            "type": "error",
            "title": "Missing title tag",
            "message": (
                "Add a descriptive HTML title tag "
                "to the page."
            ),
        })

    elif not 30 <= data["title"]["length"] <= 65:
        recommendations.append({
            "type": "warning",
            "title": "Improve title length",
            "message": (
                "Keep the page title roughly "
                "between 30 and 65 characters."
            ),
        })

    if not data["meta_description"]["exists"]:
        recommendations.append({
            "type": "error",
            "title": "Missing meta description",
            "message": (
                "Add a unique meta description "
                "for the page."
            ),
        })

    elif not 70 <= data["meta_description"]["length"] <= 170:
        recommendations.append({
            "type": "warning",
            "title": "Improve meta description",
            "message": (
                "Review the meta description length "
                "and make it concise and descriptive."
            ),
        })

    if data["headings"]["h1_count"] == 0:
        recommendations.append({
            "type": "error",
            "title": "Missing H1 heading",
            "message": (
                "Add one clear primary H1 heading."
            ),
        })

    elif data["headings"]["h1_count"] > 1:
        recommendations.append({
            "type": "warning",
            "title": "Multiple H1 headings",
            "message": (
                "Consider using one primary H1 "
                "for a clearer page structure."
            ),
        })

    if data["images"]["missing_alt"] > 0:
        recommendations.append({
            "type": "warning",
            "title": "Missing image alt text",
            "message": (
                f'{data["images"]["missing_alt"]} image(s) '
                "are missing descriptive alt text."
            ),
        })

    if not data["canonical"]["exists"]:
        recommendations.append({
            "type": "warning",
            "title": "Missing canonical tag",
            "message": (
                "Add a canonical URL to help search engines "
                "understand the preferred page version."
            ),
        })

    if not data["viewport"]["exists"]:
        recommendations.append({
            "type": "error",
            "title": "Viewport tag missing",
            "message": (
                "Add a responsive viewport meta tag "
                "for mobile compatibility."
            ),
        })

    if not data["https"]:
        recommendations.append({
            "type": "error",
            "title": "HTTPS not enabled",
            "message": (
                "Serve the website securely over HTTPS."
            ),
        })

    if data["robots"]["noindex"]:
        recommendations.append({
            "type": "error",
            "title": "Page is set to noindex",
            "message": (
                "Search engines may be instructed not "
                "to index this page."
            ),
        })

    if data["content"]["word_count"] < 150:
        recommendations.append({
            "type": "warning",
            "title": "Very limited page content",
            "message": (
                "The page contains relatively little "
                "indexable text content."
            ),
        })

    if not recommendations:
        recommendations.append({
            "type": "success",
            "title": "Strong basic SEO setup",
            "message": (
                "No major issues were found in the "
                "basic on-page SEO checks."
            ),
        })

    return recommendations

def calculate_category_scores(data):
    """
    Calculate SEO category scores from real website signals.

    These scores are deterministic and based on measurable
    SEO factors collected during analysis.
    """

    # =========================================
    # PERFORMANCE SCORE
    # =========================================

    response_time = data["response_time_ms"]

    if response_time <= 300:
        performance = 100
    elif response_time <= 700:
        performance = 90
    elif response_time <= 1200:
        performance = 80
    elif response_time <= 2000:
        performance = 65
    elif response_time <= 4000:
        performance = 45
    else:
        performance = 25

    # =========================================
    # ON-PAGE SEO SCORE
    # =========================================

    on_page = 0

    title = data["title"]
    description = data["meta_description"]
    headings = data["headings"]
    images = data["images"]
    content = data["content"]

    # Title — 20
    if title["exists"]:
        on_page += 10

        if 30 <= title["length"] <= 65:
            on_page += 10

    # Meta Description — 20
    if description["exists"]:
        on_page += 10

        if 70 <= description["length"] <= 170:
            on_page += 10

    # H1 — 20
    if headings["h1_count"] == 1:
        on_page += 20
    elif headings["h1_count"] > 1:
        on_page += 10

    # H2 — 10
    if headings["h2_count"] >= 1:
        on_page += 10

    # Image ALT — 15
    if images["total"] == 0:
        on_page += 15
    else:
        alt_ratio = (
            images["with_alt"]
            / images["total"]
        )

        on_page += round(alt_ratio * 15)

    # Content — 15
    if content["word_count"] >= 500:
        on_page += 15
    elif content["word_count"] >= 300:
        on_page += 12
    elif content["word_count"] >= 150:
        on_page += 7

    on_page = min(on_page, 100)

    # =========================================
    # TECHNICAL SEO SCORE
    # =========================================

    technical = 0

    # HTTP response health — 20
    if 200 <= data["status_code"] < 300:
        technical += 20
    elif 300 <= data["status_code"] < 400:
        technical += 10

    # HTTPS — 25
    if data["https"]:
        technical += 25

    # Canonical — 20
    if data["canonical"]["exists"]:
        technical += 20

    # Indexability — 20
    if not data["robots"]["noindex"]:
        technical += 20

    # Links available — 15
    if data["links"]["total"] > 0:
        technical += 15

    technical = min(technical, 100)

    # =========================================
    # MOBILE SEO SCORE
    # =========================================

    mobile = 0

    viewport = data["viewport"]

    if viewport["exists"]:
        mobile += 70

        viewport_content = viewport["content"].lower()

        if "width=device-width" in viewport_content:
            mobile += 20

        if "initial-scale" in viewport_content:
            mobile += 10

    mobile = min(mobile, 100)

    return {
        "performance": performance,
        "on_page": on_page,
        "technical": technical,
        "mobile": mobile,
    }

def analyze_website(raw_url):
    """
    Main function called by Flask API.
    """

    url = normalize_url(raw_url)

    response, response_time = fetch_page(url)

    final_url = response.url

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    data = {
        "requested_url": url,
        "final_url": final_url,
        "status_code": response.status_code,
        "response_time_ms": response_time,
        "https": (
            urlparse(final_url).scheme.lower()
            == "https"
        ),
        "title": extract_title(soup),
        "meta_description": extract_meta_description(soup),
        "headings": extract_headings(soup),
        "images": extract_images(soup),
        "canonical": extract_canonical(soup),
        "viewport": extract_viewport(soup),
        "robots": extract_robots_meta(soup),
        "links": extract_links(
            soup,
            final_url,
        ),
        "content": extract_content_stats(soup),
    }

    data["score"] = calculate_score(data)
    data["category_scores"] = calculate_category_scores(
    data
)

    data["recommendations"] = build_recommendations(
        data
    )

    return data