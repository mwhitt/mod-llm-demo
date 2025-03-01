import re
from lib.scraper import get_webpage_markdown


def combine_markdown_from_urls(original_markdown: str, urls: list[str]) -> str:
    """
    Fetch markdown content from each URL and combine it with the original markdown.
    
    Args:
        original_markdown: The original markdown content
        urls: List of unique base URLs to fetch content from
        
    Returns:
        Combined markdown content with separators
    """
    combined_content = original_markdown    
    for url in urls:
        try:
            print(f"Fetching content from: {url}")
            url_content = get_webpage_markdown(url)
            combined_content += f"\n\n---\n\n"
            combined_content += url_content
            
        except Exception as e:
            print(f"Error fetching content from {url}: {e}")
    
    return combined_content

def clean_markdown(markdown_text: str) -> str:
    """
    Clean markdown by removing HTTP links and images according to specific rules:
    - Delete lines starting with 'URL Source:' followed by a link
    - For markdown links, keep the text but remove the surrounding parentheses with the URL
    - Delete lines containing markdown image syntax
    - Ensure there's only one blank line in a row
    - Remove lines with more than three consecutive equal signs
    
    Args:
        markdown_text: The original markdown content
        
    Returns:
        Cleaned markdown content with links and images removed and no consecutive blank lines
    """
    # Split the markdown into lines for processing
    lines = markdown_text.split('\n')
    cleaned_lines = []
    
    # Flag to track if the previous line was blank
    previous_line_was_blank = False
    
    for line in lines:
        # Rule 1: Skip lines that start with 'URL Source:' followed by an HTTP link
        if re.match(r'^\s*URL Source:\s*https?://', line):
            continue
        
        # Rule 3: Skip lines containing markdown image syntax ![...](...)
        if re.search(r'!\[.*?\]\(https?://.*?\)', line):
            continue
        
        # Skip lines with more than three consecutive equal signs
        if re.search(r'-{4,}', line):
            continue
            
        # Skip lines with 3 or more consecutive equal signs
        if re.search(r'={3,}', line):
            continue

        # Rule 2: For markdown links, keep the text but remove the URL and parentheses
        # This regex finds markdown links [text](http://url) and replaces with just the text
        line = re.sub(r'\[(.*?)\]\(https?://.*?\)', r'\1', line)
        
        # Also handle bare URLs (not in markdown format)
        # But only if they're not part of code blocks (simple heuristic: line doesn't start with spaces followed by http)
        if not re.match(r'^\s+https?://', line):
            line = re.sub(r'https?://\S+', '', line)
        
        # Check if current line is blank (empty or just whitespace)
        current_line_is_blank = line.strip() == ''
        
        # Only add the line if:
        # 1. It's not blank, or
        # 2. It's blank but the previous line wasn't blank
        if not current_line_is_blank or not previous_line_was_blank:
            cleaned_lines.append(line)
            
        # Update the flag for the next iteration
        previous_line_was_blank = current_line_is_blank
    
    # Join the cleaned lines back into a single string
    return '\n'.join(cleaned_lines)