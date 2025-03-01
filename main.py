from dotenv import load_dotenv
from lib.scraper import extract_links_from_markdown_content, extract_unique_base_urls, get_webpage_markdown

load_dotenv(".env.local")

def main():
    print("Hello from mod-llm!")
    url = 'https://rawcaptureguide.gumroad.com/l/captureone2025guide'
    markdown = get_webpage_markdown(url)
    links = extract_links_from_markdown_content(markdown)
    unique_urls = extract_unique_base_urls(links)
    print(f"Found {len(unique_urls)} unique URLs")
    for base_url in unique_urls:
        print(f"- {base_url}")

if __name__ == "__main__":
    main()
