import os
import re
import httpx
from urllib.parse import urlparse


def get_webpage_markdown(url: str) -> str:
    base_url = "https://r.jina.ai/"
    headers = {"Authorization": "Bearer " + os.getenv("JINA_API_KEY")}

    with httpx.Client() as client:
        response = client.get(base_url + url, headers=headers)
    return response.text


def extract_links_from_markdown_content(markdown_str: str) -> list[str]:
    """
    Extract all links from the 'Markdown Content:' section of a markdown string.

    Args:
        markdown_str: The markdown string to parse

    Returns:
        A list of extracted URLs
    """
    # Find the "Markdown Content:" section
    if "Markdown Content:" in markdown_str:
        content_section = markdown_str.split("Markdown Content:")[1]
    else:
        content_section = markdown_str

    # Use regex to find all markdown links in the format [text](url)
    link_pattern = r"\[([^\]]+)\]\(([^)]+)\)"
    links = re.findall(link_pattern, content_section)

    # Extract just the URLs (second group in each match)
    urls = [link[1] for link in links]

    return urls


def extract_unique_base_urls(urls: list[str]) -> list[str]:
    """
    Extract the unique base URLs from a list of URLs.

    Args:
        urls: A list of complete URLs

    Returns:
        A list of unique base URLs (scheme + domain)
    """
    base_urls = set()
    excluded_domains = [
        "gumroad.com",
        "patreon.com",
        "youtube.com",
        "instagram.com",
        "tiktok.com",
        "facebook.com",
        "x.com",
        "twitter.com",
        "youtu.be",
        "discord.com",
        "linktr.ee",
    ]

    for url in urls:
        try:
            # Skip URLs with "google" anywhere in the URL
            if "google" in url.lower():
                continue

            # Parse the URL
            parsed_url = urlparse(url)

            # Skip if domain is empty
            if not parsed_url.netloc:
                continue

            # Skip if protocol is not https
            if parsed_url.scheme and parsed_url.scheme != "https":
                continue

            # Skip URLs with excluded domains
            if any(domain in parsed_url.netloc for domain in excluded_domains):
                continue

            # Create base URL (scheme + domain)
            base_url = f"https://{parsed_url.netloc}"  # Always use https

            # Handle case where scheme might be missing
            if not parsed_url.scheme and not parsed_url.netloc and parsed_url.path:
                # Try to handle URLs without scheme but with domain in path
                potential_domain = parsed_url.path.split("/")[0]
                if "." in potential_domain:  # Simple check if it looks like a domain
                    # Skip if the potential domain contains any excluded domain
                    if any(domain in potential_domain for domain in excluded_domains):
                        continue
                    base_url = f"https://{potential_domain}"

            # Skip if base URL has empty domain
            if base_url == "https://" or not base_url:
                continue

            # Only add non-empty base URLs
            base_urls.add(base_url)

        except Exception as e:
            print(f"Error parsing URL '{url}': {e}")
            continue

    return sorted(list(base_urls))
