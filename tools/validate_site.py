from __future__ import annotations

import csv
import hashlib
import json
import re
import struct
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path, PurePosixPath
from urllib.parse import unquote, urlsplit

from bs4 import BeautifulSoup


ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PUBLIC = ROOT / "public"
SITE_ORIGIN = "https://knottyquant.com"

EXPECTED_HTML = {
    "index.html",
    "research.html",
    "writing.html",
    "about.html",
    "sofr-curve-swap-risk.html",
    "portfolio-construction.html",
    "volatility-surface-research.html",
    "writing/knot-theory-topological-data-analysis-and-finance.html",
    "404.html",
}
INDEXABLE_HTML = EXPECTED_HTML - {"404.html"}
ARTICLE_HTML = {
    "sofr-curve-swap-risk.html",
    "portfolio-construction.html",
    "volatility-surface-research.html",
    "writing/knot-theory-topological-data-analysis-and-finance.html",
}
PROJECT_HTML = ARTICLE_HTML - {
    "writing/knot-theory-topological-data-analysis-and-finance.html"
}

LEGACY_FRAGMENTS = {
    "sofr-curve-swap-risk.html": {
        "overview",
        "curve",
        "swap",
        "risk",
        "explain",
        "implementation",
        "validation",
        "limits",
    },
    "portfolio-construction.html": {
        "overview",
        "design",
        "methods",
        "constraints",
        "evidence",
        "attribution",
        "validation",
        "limits",
    },
    "volatility-surface-research.html": {
        "overview",
        "data",
        "surface",
        "repair",
        "governance",
        "weekly",
        "alternatives",
        "american",
        "numerics",
        "closing",
        "report",
        "limits",
    },
    "index.html": {"research", "contact"},
}

REQUIRED_LINKS = {
    "index.html": {
        "/research.html",
        "/writing/knot-theory-topological-data-analysis-and-finance.html",
        "/sofr-curve-swap-risk.html",
        "/portfolio-construction.html",
        "/volatility-surface-research.html",
    },
    "research.html": {
        "/sofr-curve-swap-risk.html",
        "/portfolio-construction.html",
        "/volatility-surface-research.html",
        "/assets/docs/Volatility_Surface_Calibration_and_Option_Pricing.pdf",
    },
    "writing.html": {
        "/writing/knot-theory-topological-data-analysis-and-finance.html",
    },
    "sofr-curve-swap-risk.html": {
        "https://github.com/ItsKamatis/sofr-curve-swap-risk",
        "/assets/docs/SOFR_Curve_Swap_Risk_2026-07-02.xlsx",
        "/assets/data/rates/curve_nodes.csv",
        "/assets/data/rates/key_rate_dv01.csv",
    },
    "portfolio-construction.html": {
        "https://github.com/ItsKamatis/constrained-portfolio-construction",
        "/assets/data/portfolio/summary.csv",
        "/assets/data/portfolio/bootstrap_uncertainty.csv",
    },
    "volatility-surface-research.html": {
        "/assets/docs/Volatility_Surface_Calibration_and_Option_Pricing.pdf",
        "/assets/docs/VolSurf_Pricer_Equation_Traceability.csv",
        "/assets/docs/VolSurf_Pricer_Claim_Evidence_Ledger.csv",
        "/assets/docs/VolSurf_Pricer_Source_Registry.csv",
    },
    "about.html": {
        "https://github.com/ItsKamatis",
        "https://linkedin.com/in/Colmenar",
    },
    "writing/knot-theory-topological-data-analysis-and-finance.html": {
        "https://academic.oup.com/nar/article/50/W1/W44/6591522",
        "https://doi.org/10.1016/j.physa.2017.09.028",
        "https://doi.org/10.1016/j.physa.2021.126459",
        "https://doi.org/10.3390/e23091211",
        "https://doi.org/10.1016/j.dajour.2024.100512",
        "https://doi.org/10.1016/j.topol.2020.107523",
        "https://doi.org/10.1080/14697688.2025.2544762",
        "https://doi.org/10.1016/j.omega.2025.103432",
    },
}

PRESERVED_DOWNLOAD_HASHES = {
    "assets/docs/SOFR_Curve_Swap_Risk_2026-07-02.xlsx": (
        "e837b53c302172573c5de04c9f37971cbbcbdd51da571bbc379225afae513ab8"
    ),
    "assets/docs/Volatility_Surface_Calibration_and_Option_Pricing.pdf": (
        "8939ecdc67063963755e975281ecdea8ff8163a862e769037affbbfe13523b70"
    ),
    "assets/docs/VolSurf_Pricer_Claim_Evidence_Ledger.csv": (
        "a08a41edd6ef52c860dd4e2784de7508f5d92f90ae83a76260987b1fd80d133b"
    ),
    "assets/docs/VolSurf_Pricer_Equation_Traceability.csv": (
        "9e9470da982d6b177d5d788759742a69a49f9f7d6769dc1c8205c4f545e00ab0"
    ),
    "assets/docs/VolSurf_Pricer_Source_Registry.csv": (
        "0379f54780c3d1a41697aebf54af2f280bee9c772abbfc857ebbdf88a31454c0"
    ),
}

PRESERVED_IMAGE_PATHS = {
    "og.png",
    "images/favicon.svg",
    "images/og-quant-research.png",
    "images/research/aapl-repaired-surface.png",
    "images/research/aapl-time-value-fit.png",
    "images/research/ndx-svi-smiles.png",
    "images/research/ndx-vol-surface.png",
    "images/research/portfolio-attribution.png",
    "images/research/portfolio-growth.png",
    "images/research/portfolio-tradeoffs.png",
    "images/research/rates-curve.png",
    "images/research/rates-risk.png",
    "images/research/rates-value-change.png",
    "images/research/technical-report-cover.png",
    *{
        f"images/research/report/fig{number:02d}_{name}.svg"
        for number, name in enumerate(
            (
                "pipeline_architecture",
                "contract_taxonomy",
                "repair_projection",
                "objective_geometry",
                "weekly_refinement",
                "weekly_transfer",
                "weekly_full_chain",
                "basket_endogeneity",
                "carry_endogeneity",
                "boundary_attribution",
                "surface_candidate_gates",
                "local_repo_common_support",
                "american_normalization",
                "early_exercise_premium",
                "american_convergence",
                "closing_pricing",
                "closing_quality",
                "research_decision_path",
            ),
            start=1,
        )
    },
}

FORBIDDEN_COPY = {
    "tail-risk portfolio": "obsolete project framing",
    "krnn forecasting": "obsolete project framing",
    "do the numbers ever lie": "cliche copy",
    "cutting-edge": "promotional copy",
    "game-changing": "promotional copy",
    "institutional-grade": "inflated positioning",
    "battle-tested": "unsupported production claim",
    "widely used by financial institutions": "unsupported adoption claim",
    "lorem ipsum": "placeholder copy",
}
MOJIBAKE_MARKERS = ("Â", "â€œ", "â€", "ï¿½", "\ufffd")
REQUIRED_PRIMARY_NAV = {"/research.html", "/writing.html", "/about.html"}


def relative_name(path: Path) -> str:
    try:
        return path.relative_to(DIST).as_posix()
    except ValueError:
        return str(path)


def fail(errors: list[str], subject: Path | str, message: str) -> None:
    label = relative_name(subject) if isinstance(subject, Path) else subject
    errors.append(f"{label}: {message}")


def exact_case_exists(path: Path) -> bool:
    try:
        relative = path.resolve().relative_to(DIST.resolve())
    except ValueError:
        return False
    current = DIST.resolve()
    for part in relative.parts:
        if not current.is_dir():
            return False
        matches = [child for child in current.iterdir() if child.name == part]
        if len(matches) != 1:
            return False
        current = matches[0]
    return current.exists()


def canonical_for(relative: str) -> str:
    if relative == "index.html":
        return f"{SITE_ORIGIN}/"
    return f"{SITE_ORIGIN}/{relative}"


def normalized_link(value: str) -> str:
    parsed = urlsplit(value.strip())
    if parsed.scheme in {"http", "https"}:
        return value.strip()
    if parsed.netloc:
        return value.strip()
    path = unquote(parsed.path)
    if not path:
        return f"#{unquote(parsed.fragment)}" if parsed.fragment else ""
    if path.startswith("/"):
        return path
    return path


def local_target(page: Path, value: str) -> tuple[Path | None, str]:
    parsed = urlsplit(value.strip())
    if parsed.scheme in {"mailto", "tel", "data", "javascript"}:
        return None, ""
    if parsed.scheme in {"http", "https"} or parsed.netloc:
        host = parsed.hostname.lower() if parsed.hostname else ""
        if host != "knottyquant.com":
            return None, ""
    raw_path = unquote(parsed.path)
    if raw_path in {"", "."}:
        target = page
    elif raw_path == "/":
        target = DIST / "index.html"
    elif raw_path.startswith("/"):
        target = DIST / raw_path.lstrip("/")
    else:
        target = page.parent / raw_path
    try:
        resolved = target.resolve()
        resolved.relative_to(DIST.resolve())
    except ValueError:
        return target.resolve(), unquote(parsed.fragment)
    return resolved, unquote(parsed.fragment)


def check_local_reference(
    errors: list[str], page: Path, value: str, label: str
) -> Path | None:
    target, _ = local_target(page, value)
    if target is None:
        return None
    if not target.exists():
        fail(errors, page, f"missing local {label}: {value}")
        return target
    if not exact_case_exists(target):
        fail(errors, page, f"case mismatch in local {label}: {value}")
    return target


def one_meta(
    errors: list[str],
    page: Path,
    soup: BeautifulSoup,
    *,
    name: str | None = None,
    property_name: str | None = None,
) -> str:
    attrs = {"name": name} if name else {"property": property_name}
    tags = soup.find_all("meta", attrs=attrs)
    key = name or property_name or "unknown"
    if len(tags) != 1:
        fail(errors, page, f"expected one {key} meta tag, found {len(tags)}")
        return ""
    value = tags[0].get("content", "").strip()
    if not value:
        fail(errors, page, f"{key} meta tag has no content")
    return value


def image_dimensions(path: Path) -> tuple[float, float] | None:
    suffix = path.suffix.lower()
    if suffix == ".png":
        header = path.read_bytes()[:24]
        if header[:8] != b"\x89PNG\r\n\x1a\n" or len(header) < 24:
            return None
        return tuple(float(value) for value in struct.unpack(">II", header[16:24]))
    if suffix == ".gif":
        header = path.read_bytes()[:10]
        if header[:6] not in {b"GIF87a", b"GIF89a"}:
            return None
        return tuple(float(value) for value in struct.unpack("<HH", header[6:10]))
    if suffix in {".jpg", ".jpeg"}:
        data = path.read_bytes()
        index = 2
        while index + 9 < len(data):
            if data[index] != 0xFF:
                index += 1
                continue
            marker = data[index + 1]
            index += 2
            if marker in {0xD8, 0xD9}:
                continue
            if index + 2 > len(data):
                break
            length = int.from_bytes(data[index : index + 2], "big")
            if marker in {
                0xC0,
                0xC1,
                0xC2,
                0xC3,
                0xC5,
                0xC6,
                0xC7,
                0xC9,
                0xCA,
                0xCB,
                0xCD,
                0xCE,
                0xCF,
            }:
                height = int.from_bytes(data[index + 3 : index + 5], "big")
                width = int.from_bytes(data[index + 5 : index + 7], "big")
                return float(width), float(height)
            index += length
        return None
    if suffix == ".svg":
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError:
            return None
        view_box = root.attrib.get("viewBox")
        if view_box:
            values = re.split(r"[\s,]+", view_box.strip())
            if len(values) == 4:
                return float(values[2]), float(values[3])
        width = root.attrib.get("width", "")
        height = root.attrib.get("height", "")
        width_match = re.match(r"([0-9.]+)", width)
        height_match = re.match(r"([0-9.]+)", height)
        if width_match and height_match:
            return float(width_match.group(1)), float(height_match.group(1))
    return None


def check_image(
    errors: list[str], page: Path, image, *, require_caption: bool = False
) -> None:
    source = image.get("src", "").strip()
    if not source:
        fail(errors, page, "image missing src")
        return
    if image.get("alt") is None or not image.get("alt", "").strip():
        fail(errors, page, f"image missing useful alt: {source}")
    width_value = image.get("width", "")
    height_value = image.get("height", "")
    if not width_value or not height_value:
        fail(errors, page, f"image missing intrinsic dimensions: {source}")
        check_local_reference(errors, page, source, "image")
        return
    try:
        declared_width = float(width_value)
        declared_height = float(height_value)
    except ValueError:
        fail(errors, page, f"image has non-numeric dimensions: {source}")
        return
    if declared_width <= 0 or declared_height <= 0:
        fail(errors, page, f"image has non-positive dimensions: {source}")
        return
    target = check_local_reference(errors, page, source, "image")
    if target and target.exists():
        actual = image_dimensions(target)
        if actual is None:
            fail(errors, page, f"cannot read image dimensions: {source}")
        else:
            actual_width, actual_height = actual
            if target.suffix.lower() == ".svg":
                ratio_error = abs(
                    (declared_width / declared_height)
                    / (actual_width / actual_height)
                    - 1
                )
                if ratio_error > 0.005:
                    fail(
                        errors,
                        page,
                        f"SVG aspect ratio differs by {ratio_error:.2%}: {source}",
                    )
            elif (declared_width, declared_height) != (
                actual_width,
                actual_height,
            ):
                fail(
                    errors,
                    page,
                    (
                        f"raster dimensions do not match file for {source}: "
                        f"declared {declared_width:g}x{declared_height:g}, "
                        f"actual {actual_width:g}x{actual_height:g}"
                    ),
                )
    if require_caption:
        figure = image.find_parent("figure")
        caption = figure.find("figcaption") if figure else None
        if not caption or not caption.get_text(" ", strip=True):
            fail(errors, page, f"research figure lacks a caption: {source}")
    inline_style = image.get("style", "").replace(" ", "").lower()
    if "height:" in inline_style or "object-fit:cover" in inline_style:
        fail(errors, page, f"research image has unsafe inline sizing: {source}")


def jsonld_nodes(data):
    if isinstance(data, dict):
        yield data
        for value in data.values():
            yield from jsonld_nodes(value)
    elif isinstance(data, list):
        for value in data:
            yield from jsonld_nodes(value)


def parse_jsonld(
    errors: list[str], page: Path, soup: BeautifulSoup
) -> tuple[list[dict], set[str]]:
    documents: list[dict] = []
    types: set[str] = set()
    for script in soup.find_all("script", attrs={"type": "application/ld+json"}):
        raw = script.string or script.get_text()
        try:
            value = json.loads(raw)
        except json.JSONDecodeError as exc:
            fail(errors, page, f"invalid JSON-LD: {exc}")
            continue
        documents.append(value)
        for node in jsonld_nodes(value):
            node_type = node.get("@type")
            if isinstance(node_type, str):
                types.add(node_type)
            elif isinstance(node_type, list):
                types.update(item for item in node_type if isinstance(item, str))
    return documents, types


def contains_organization_author(documents: list[dict]) -> bool:
    for document in documents:
        for node in jsonld_nodes(document):
            author = node.get("author")
            authors = author if isinstance(author, list) else [author]
            for item in authors:
                if (
                    isinstance(item, dict)
                    and item.get("@type") == "Organization"
                    and item.get("name") == "KnottyQuant"
                ):
                    return True
    return False


def check_page(
    errors: list[str],
    page: Path,
    soup: BeautifulSoup,
    titles: dict[str, list[str]],
    descriptions: dict[str, list[str]],
) -> None:
    relative = relative_name(page)
    text = page.read_text(encoding="utf-8")
    visible_text = soup.get_text(" ", strip=True)

    if not soup.html or soup.html.get("lang") != "en":
        fail(errors, page, "missing html[lang=en]")
    title = soup.title.get_text(" ", strip=True) if soup.title else ""
    if not title:
        fail(errors, page, "missing title")
    else:
        titles.setdefault(title, []).append(relative)
    description = one_meta(errors, page, soup, name="description")
    if description:
        descriptions.setdefault(description, []).append(relative)
    if len(soup.find_all("h1")) != 1:
        fail(errors, page, f"expected one h1, found {len(soup.find_all('h1'))}")
    for landmark in ("header", "main", "footer"):
        if not soup.find(landmark):
            fail(errors, page, f"missing {landmark} landmark")
    if not soup.find("main", id="main-content"):
        fail(errors, page, "main landmark must use id=main-content")
    if not soup.find("a", class_="skip-link", href="#main-content"):
        fail(errors, page, "missing skip link to main content")

    headings = soup.find_all(re.compile(r"^h[1-6]$"))
    previous_level = 0
    for heading in headings:
        if not heading.get_text(" ", strip=True):
            fail(errors, page, f"empty {heading.name}")
        level = int(heading.name[1])
        if previous_level and level > previous_level + 1:
            fail(
                errors,
                page,
                f"heading level skips from h{previous_level} to h{level}",
            )
        previous_level = level

    ids = [tag["id"] for tag in soup.find_all(attrs={"id": True})]
    duplicates = [value for value, count in Counter(ids).items() if count > 1]
    if duplicates:
        fail(errors, page, f"duplicate ids: {duplicates}")
    missing_aliases = LEGACY_FRAGMENTS.get(relative, set()) - set(ids)
    if missing_aliases:
        fail(errors, page, f"missing legacy fragment aliases: {sorted(missing_aliases)}")

    primary_nav = soup.find("nav", attrs={"aria-label": "Primary navigation"})
    if not primary_nav:
        fail(errors, page, "missing primary navigation")
    else:
        nav_links = {
            urlsplit(link.get("href", "")).path
            for link in primary_nav.find_all("a", href=True)
        }
        missing_nav = REQUIRED_PRIMARY_NAV - nav_links
        if missing_nav:
            fail(errors, page, f"primary navigation missing: {sorted(missing_nav)}")

    expected_canonical = canonical_for(relative)
    canonical_tags = soup.find_all("link", rel=lambda rel: rel and "canonical" in rel)
    if len(canonical_tags) != 1:
        fail(
            errors,
            page,
            f"expected one canonical link, found {len(canonical_tags)}",
        )
        canonical = ""
    else:
        canonical = canonical_tags[0].get("href", "").strip()
        if canonical != expected_canonical:
            fail(
                errors,
                page,
                f"canonical is {canonical!r}; expected {expected_canonical!r}",
            )

    meta_expectations = {
        "og:site_name": "KnottyQuant",
        "og:url": expected_canonical,
        "og:type": "article" if relative in ARTICLE_HTML else "website",
    }
    for property_name, expected in meta_expectations.items():
        actual = one_meta(errors, page, soup, property_name=property_name)
        if actual and actual != expected:
            fail(
                errors,
                page,
                f"{property_name} is {actual!r}; expected {expected!r}",
            )
    og_title = one_meta(errors, page, soup, property_name="og:title")
    og_description = one_meta(errors, page, soup, property_name="og:description")
    if og_title and title and og_title != title:
        fail(errors, page, "og:title does not match title")
    if og_description and description and og_description != description:
        fail(errors, page, "og:description does not match description")

    og_image = one_meta(errors, page, soup, property_name="og:image")
    og_alt = one_meta(errors, page, soup, property_name="og:image:alt")
    og_width = one_meta(errors, page, soup, property_name="og:image:width")
    og_height = one_meta(errors, page, soup, property_name="og:image:height")
    if og_image:
        parsed_image = urlsplit(og_image)
        if (
            parsed_image.scheme != "https"
            or parsed_image.hostname != "knottyquant.com"
        ):
            fail(errors, page, "og:image must be an absolute knottyquant.com URL")
        target = check_local_reference(errors, page, og_image, "social image")
        if target and target.exists():
            dimensions = image_dimensions(target)
            try:
                declared = (float(og_width), float(og_height))
            except ValueError:
                declared = None
                fail(errors, page, "social image metadata dimensions are not numeric")
            if dimensions and declared and dimensions != declared:
                fail(
                    errors,
                    page,
                    (
                        "social image metadata dimensions do not match file: "
                        f"{declared} versus {dimensions}"
                    ),
                )
            if dimensions:
                ratio = dimensions[0] / dimensions[1]
                if not 1.85 <= ratio <= 1.95:
                    fail(errors, page, f"social image ratio is not wide-card: {ratio:.3f}")
    if len(og_alt) < 12:
        fail(errors, page, "og:image:alt is too vague")

    twitter_expectations = {
        "twitter:card": "summary_large_image",
        "twitter:title": title,
        "twitter:description": description,
        "twitter:image": og_image,
        "twitter:image:alt": og_alt,
    }
    for name, expected in twitter_expectations.items():
        actual = one_meta(errors, page, soup, name=name)
        if actual and expected and actual != expected:
            fail(errors, page, f"{name} does not match corresponding metadata")

    rss_link = soup.find(
        "link", rel=lambda rel: rel and "alternate" in rel, attrs={"type": "application/rss+xml"}
    )
    if not rss_link or rss_link.get("href") != "/rss.xml":
        fail(errors, page, "missing canonical RSS discovery link")
    sitemap_link = soup.find("link", rel=lambda rel: rel and "sitemap" in rel)
    if not sitemap_link or sitemap_link.get("href") != "/sitemap-index.xml":
        fail(errors, page, "missing sitemap discovery link")

    robots_meta = soup.find("meta", attrs={"name": "robots"})
    if relative == "404.html":
        robots_value = robots_meta.get("content", "").lower() if robots_meta else ""
        if "noindex" not in robots_value:
            fail(errors, page, "404 page must be noindex")
    elif robots_meta and "noindex" in robots_meta.get("content", "").lower():
        fail(errors, page, "indexable page is marked noindex")

    documents, schema_types = parse_jsonld(errors, page, soup)
    if relative == "index.html":
        for required_type in ("WebSite", "Organization"):
            if required_type not in schema_types:
                fail(errors, page, f"homepage JSON-LD missing {required_type}")
    elif relative == "about.html":
        if "Person" not in schema_types:
            fail(errors, page, "About JSON-LD missing Person")
    elif relative in PROJECT_HTML:
        if "TechArticle" not in schema_types:
            fail(errors, page, "project JSON-LD missing TechArticle")
        if not contains_organization_author(documents):
            fail(errors, page, "project author must be KnottyQuant Organization")
    elif relative in ARTICLE_HTML:
        if "Article" not in schema_types:
            fail(errors, page, "writing JSON-LD missing Article")
        if not contains_organization_author(documents):
            fail(errors, page, "writing author must be KnottyQuant Organization")
    elif relative in {"research.html", "writing.html"} and not (
        {"CollectionPage", "WebPage"} & schema_types
    ):
        fail(errors, page, "index JSON-LD missing CollectionPage or WebPage")
    if relative != "about.html" and "Person" in schema_types:
        fail(errors, page, "Person schema is allowed only on About")

    if relative != "about.html" and "Joshua Colmenar" in visible_text:
        fail(errors, page, "personal name appears outside About")
    if "KnottyQuant" not in visible_text:
        fail(errors, page, "KnottyQuant brand name is absent")

    hrefs = {link.get("href", "").strip() for link in soup.find_all("a", href=True)}
    normalized_hrefs = {normalized_link(href) for href in hrefs}
    missing_links = REQUIRED_LINKS.get(relative, set()) - normalized_hrefs
    if missing_links:
        fail(errors, page, f"missing required links: {sorted(missing_links)}")
    for image in soup.find_all("img"):
        research_figure = image.find_parent("figure", class_="research-figure")
        check_image(
            errors,
            page,
            image,
            require_caption=research_figure is not None,
        )
    for script in soup.find_all("script", src=True):
        check_local_reference(errors, page, script["src"], "script")
    for asset_link in soup.find_all("link", href=True):
        rel = set(asset_link.get("rel", []))
        if rel.intersection({"stylesheet", "icon", "alternate", "sitemap"}):
            check_local_reference(errors, page, asset_link["href"], "linked asset")

    for link in soup.find_all("a", href=True):
        href = link["href"].strip()
        parsed = urlsplit(href)
        if link.get("target") == "_blank":
            rel = set(link.get("rel", []))
            if "noreferrer" not in rel:
                fail(errors, page, f"target=_blank lacks noreferrer: {href}")
        if parsed.scheme == "http":
            fail(errors, page, f"insecure external link: {href}")
        if parsed.scheme == "mailto" and not parsed.path:
            fail(errors, page, "empty mailto link")
        if parsed.scheme in {"http", "https", "mailto", "tel"} and (
            parsed.hostname != "knottyquant.com"
        ):
            continue
        target, fragment = local_target(page, href)
        if target is not None:
            if not target.exists():
                fail(errors, page, f"broken local link: {href}")
            elif not exact_case_exists(target):
                fail(errors, page, f"case mismatch in local link: {href}")
            if fragment and target.exists() and target.suffix.lower() == ".html":
                target_soup = BeautifulSoup(
                    target.read_text(encoding="utf-8"), "html.parser"
                )
                if target_soup.find(id=fragment) is None:
                    fail(errors, page, f"missing fragment target: {href}")
        local_path = unquote(parsed.path)
        if (
            not parsed.scheme
            and local_path.startswith("/")
            and local_path not in {"", "/"}
            and "." not in PurePosixPath(local_path).name
        ):
            fail(errors, page, f"extensionless internal route is not allowed: {href}")

    lowered = text.lower()
    if "joshuacolmenar.com" in lowered:
        fail(errors, page, "contains old domain")
    for phrase, reason in FORBIDDEN_COPY.items():
        if phrase in lowered:
            fail(errors, page, f"contains {reason}: {phrase!r}")
    for marker in MOJIBAKE_MARKERS:
        if marker in text:
            fail(errors, page, f"contains likely mojibake marker: {marker!r}")


def check_sitemap(errors: list[str]) -> None:
    sitemap_index = DIST / "sitemap-index.xml"
    if not sitemap_index.exists():
        fail(errors, "sitemap-index.xml", "missing generated sitemap index")
        return
    try:
        root = ET.parse(sitemap_index).getroot()
    except ET.ParseError as exc:
        fail(errors, "sitemap-index.xml", f"invalid XML: {exc}")
        return
    sitemap_urls = [
        element.text.strip()
        for element in root.findall(".//{*}loc")
        if element.text
    ]
    if not sitemap_urls:
        fail(errors, "sitemap-index.xml", "contains no sitemap entries")
        return
    page_urls: set[str] = set()
    for sitemap_url in sitemap_urls:
        parsed = urlsplit(sitemap_url)
        if parsed.scheme != "https" or parsed.hostname != "knottyquant.com":
            fail(errors, "sitemap-index.xml", f"unexpected sitemap URL: {sitemap_url}")
            continue
        target = DIST / parsed.path.lstrip("/")
        if not target.exists():
            fail(errors, "sitemap-index.xml", f"missing sitemap file: {sitemap_url}")
            continue
        try:
            page_root = ET.parse(target).getroot()
        except ET.ParseError as exc:
            fail(errors, relative_name(target), f"invalid XML: {exc}")
            continue
        page_urls.update(
            element.text.strip()
            for element in page_root.findall(".//{*}loc")
            if element.text
        )
    page_urls = {
        f"{SITE_ORIGIN}/" if url == SITE_ORIGIN else url
        for url in page_urls
    }
    expected_urls = {canonical_for(relative) for relative in INDEXABLE_HTML}
    missing = expected_urls - page_urls
    extra = page_urls - expected_urls
    if missing:
        fail(errors, "sitemap", f"missing URLs: {sorted(missing)}")
    if extra:
        fail(errors, "sitemap", f"unexpected URLs: {sorted(extra)}")


def check_rss(errors: list[str]) -> None:
    rss = DIST / "rss.xml"
    if not rss.exists():
        fail(errors, "rss.xml", "missing RSS feed")
        return
    try:
        root = ET.parse(rss).getroot()
    except ET.ParseError as exc:
        fail(errors, "rss.xml", f"invalid XML: {exc}")
        return
    channel = root.find("channel")
    if channel is None:
        fail(errors, "rss.xml", "missing channel")
        return
    title = channel.findtext("title", "").strip()
    if title != "KnottyQuant writing":
        fail(errors, "rss.xml", f"unexpected channel title: {title!r}")
    links = {
        item.findtext("link", "").strip()
        for item in channel.findall("item")
        if item.findtext("link", "").strip()
    }
    expected = {
        f"{SITE_ORIGIN}/writing/knot-theory-topological-data-analysis-and-finance.html"
    }
    if links != expected:
        fail(errors, "rss.xml", f"entry links are {sorted(links)}; expected {sorted(expected)}")


def check_robots(errors: list[str]) -> None:
    robots = DIST / "robots.txt"
    if not robots.exists():
        fail(errors, "robots.txt", "missing robots file")
        return
    text = robots.read_text(encoding="utf-8")
    for line in (
        "User-agent: *",
        "Allow: /",
        f"Sitemap: {SITE_ORIGIN}/sitemap-index.xml",
    ):
        if line not in text:
            fail(errors, "robots.txt", f"missing line: {line}")
    if "joshuacolmenar.com" in text.lower():
        fail(errors, "robots.txt", "contains old domain")


def check_manifest(errors: list[str]) -> None:
    manifest = PUBLIC / "assets" / "data" / "artifact_manifest.csv"
    if not manifest.exists():
        fail(errors, "artifact_manifest.csv", "missing public artifact manifest")
        return
    required_columns = {
        "site_path",
        "bytes",
        "sha256",
        "source_project",
        "source_commit",
        "classification",
    }
    with manifest.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames or not required_columns.issubset(reader.fieldnames):
            fail(errors, "artifact_manifest.csv", "missing required columns")
            return
        for row in reader:
            relative = PurePosixPath(row["site_path"])
            if relative.is_absolute() or ".." in relative.parts:
                fail(
                    errors,
                    "artifact_manifest.csv",
                    f"path escapes public root: {row['site_path']}",
                )
                continue
            for root, label in ((PUBLIC, "public"), (DIST, "dist")):
                target = root.joinpath(*relative.parts)
                if not target.exists():
                    fail(
                        errors,
                        "artifact_manifest.csv",
                        f"missing {label} artifact: {row['site_path']}",
                    )
                    continue
                expected_size = int(row["bytes"])
                if target.stat().st_size != expected_size:
                    fail(
                        errors,
                        "artifact_manifest.csv",
                        f"{label} size mismatch: {row['site_path']}",
                    )
                digest = hashlib.sha256(target.read_bytes()).hexdigest()
                if digest != row["sha256"]:
                    fail(
                        errors,
                        "artifact_manifest.csv",
                        f"{label} checksum mismatch: {row['site_path']}",
                    )


def check_preserved_assets(errors: list[str]) -> None:
    required = set(PRESERVED_DOWNLOAD_HASHES) | PRESERVED_IMAGE_PATHS
    required.update(
        {
            "assets/data/README.md",
            "assets/data/artifact_manifest.csv",
            "assets/fonts/licenses/IBM-Plex-Mono-OFL.txt",
            "assets/fonts/licenses/IBM-Plex-Sans-OFL.txt",
            "assets/fonts/licenses/Source-Serif-4-OFL.txt",
            "og.png",
        }
    )
    for relative in sorted(required):
        for root, label in ((PUBLIC, "public"), (DIST, "dist")):
            target = root.joinpath(*PurePosixPath(relative).parts)
            if not target.exists():
                fail(errors, "assets", f"missing {label} path: /{relative}")
    for relative, expected_hash in PRESERVED_DOWNLOAD_HASHES.items():
        for root, label in ((PUBLIC, "public"), (DIST, "dist")):
            target = root.joinpath(*PurePosixPath(relative).parts)
            if not target.exists():
                continue
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            if digest != expected_hash:
                fail(errors, "assets", f"{label} download changed: /{relative}")

    favicon = DIST / "images" / "favicon.svg"
    if favicon.exists():
        text = favicon.read_text(encoding="utf-8")
        lowered = text.lower()
        if "ajc" in lowered or "joshua" in lowered:
            fail(errors, "images/favicon.svg", "contains legacy personal mark")
        if "kq" not in lowered and "knottyquant" not in lowered:
            fail(errors, "images/favicon.svg", "lacks KnottyQuant/KQ accessible label")


def check_css(errors: list[str]) -> None:
    stylesheets = sorted((DIST / "_astro").glob("*.css"))
    if not stylesheets:
        fail(errors, "CSS", "no generated Astro stylesheet found")
        return
    css = "\n".join(path.read_text(encoding="utf-8") for path in stylesheets)
    compact = re.sub(r"\s+", "", css).lower()
    if "fonts.googleapis.com" in compact or "fonts.gstatic.com" in compact:
        fail(errors, "CSS", "contains external Google Fonts reference")
    if "@font-face" not in compact:
        fail(errors, "CSS", "self-hosted font faces were not bundled")
    research_rules = re.findall(r"\.research-figureimg\{([^}]*)\}", compact)
    if not research_rules:
        fail(errors, "CSS", "missing research-figure image rule")
    elif not any(
        "height:auto" in rule and "object-fit:contain" in rule
        for rule in research_rules
    ):
        fail(errors, "CSS", "research figures must use height:auto and object-fit:contain")
    if any(
        re.search(r"height:(?!auto)[^;]+", rule)
        or "object-fit:cover" in rule
        for rule in research_rules
    ):
        fail(errors, "CSS", "research figures contain fixed-height or cover cropping")
    if "@keyframes" in compact:
        fail(errors, "CSS", "decorative keyframe animation is not permitted")
    if "@media(prefers-reduced-motion:reduce)" not in compact:
        fail(errors, "CSS", "missing reduced-motion rule")


def strip_jsonc_comments(text: str) -> str:
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    return re.sub(r"(^|\s)//.*?$", r"\1", text, flags=re.MULTILINE)


def check_cloudflare_config(errors: list[str]) -> None:
    config_path = ROOT / "wrangler.jsonc"
    if not config_path.exists():
        fail(errors, "wrangler.jsonc", "missing Cloudflare configuration")
        return
    try:
        config = json.loads(
            strip_jsonc_comments(config_path.read_text(encoding="utf-8"))
        )
    except json.JSONDecodeError as exc:
        fail(errors, "wrangler.jsonc", f"invalid JSONC: {exc}")
        return
    assets = config.get("assets", {})
    expected = {
        "directory": "./dist",
        "html_handling": "none",
        "not_found_handling": "404-page",
    }
    for key, value in expected.items():
        if assets.get(key) != value:
            fail(
                errors,
                "wrangler.jsonc",
                f"assets.{key} is {assets.get(key)!r}; expected {value!r}",
            )

    redirects = DIST / "_redirects"
    if not redirects.exists():
        fail(errors, "_redirects", "missing Cloudflare static redirects")
    else:
        lines = {
            line.strip()
            for line in redirects.read_text(encoding="utf-8").splitlines()
            if line.strip() and not line.lstrip().startswith("#")
        }
        expected_lines = {"/index.html / 301", "/ /index.html 200"}
        if not expected_lines.issubset(lines):
            fail(
                errors,
                "_redirects",
                f"missing required rules: {sorted(expected_lines - lines)}",
            )

    headers = DIST / "_headers"
    if not headers.exists():
        fail(errors, "_headers", "missing response-header policy")
    else:
        header_text = headers.read_text(encoding="utf-8").lower()
        for header in (
            "x-content-type-options: nosniff",
            "referrer-policy:",
            "permissions-policy:",
            "x-frame-options:",
        ):
            if header not in header_text:
                fail(errors, "_headers", f"missing security header: {header}")


def check_dist_domain_scan(errors: list[str]) -> None:
    needle = b"joshuacolmenar.com"
    for path in DIST.rglob("*"):
        if path.is_file() and needle in path.read_bytes().lower():
            fail(errors, path, "contains old domain bytes")


def main() -> None:
    errors: list[str] = []
    if not DIST.is_dir():
        raise SystemExit("dist/ is missing; run the production build before validation")

    html_files = sorted(DIST.rglob("*.html"))
    actual_html = {relative_name(path) for path in html_files}
    missing_html = EXPECTED_HTML - actual_html
    unexpected_html = actual_html - EXPECTED_HTML
    if missing_html:
        fail(errors, "routes", f"missing HTML outputs: {sorted(missing_html)}")
    if unexpected_html:
        fail(errors, "routes", f"unexpected HTML outputs: {sorted(unexpected_html)}")

    parsed_pages: dict[Path, BeautifulSoup] = {}
    titles: dict[str, list[str]] = {}
    descriptions: dict[str, list[str]] = {}
    for page in html_files:
        soup = BeautifulSoup(page.read_text(encoding="utf-8"), "html.parser")
        parsed_pages[page.resolve()] = soup
        check_page(errors, page, soup, titles, descriptions)

    for title, pages in titles.items():
        if len(pages) > 1:
            fail(errors, "metadata", f"duplicate title {title!r}: {pages}")
    for description, pages in descriptions.items():
        if len(pages) > 1:
            fail(errors, "metadata", f"duplicate description {description!r}: {pages}")

    check_sitemap(errors)
    check_rss(errors)
    check_robots(errors)
    check_manifest(errors)
    check_preserved_assets(errors)
    check_css(errors)
    check_cloudflare_config(errors)
    check_dist_domain_scan(errors)

    if errors:
        print(f"SITE_VALIDATION=FAIL errors={len(errors)}")
        for error in errors:
            print(f"- {error}")
        raise SystemExit(1)

    print(
        "SITE_VALIDATION=PASS "
        f"pages={len(html_files)} "
        f"indexable={len(INDEXABLE_HTML)}"
    )


if __name__ == "__main__":
    main()
