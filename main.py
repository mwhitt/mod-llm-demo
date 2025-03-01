from dotenv import load_dotenv
from lib.md_helper import clean_markdown, combine_markdown_from_urls
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
    
    # Fetch and combine content from all unique URLs
    combined_markdown = combine_markdown_from_urls(markdown, unique_urls)
    
    # Clean the markdown
    cleaned_markdown = clean_markdown(combined_markdown)
    
    # Save the cleaned markdown to a file
    with open("cleaned_content.md", "w", encoding="utf-8") as f:
        f.write(cleaned_markdown)
    
    print(f"\nCombined markdown saved to combined_content.md")
    print(f"Cleaned markdown saved to cleaned_content.md")

if __name__ == "__main__":
    main()
