from lib.llm import call_synthetic_llm
from lib.md_helper import clean_markdown, combine_markdown_from_urls
from lib.prompts import get_synthetic_prompt
from lib.scraper import (
    extract_links_from_markdown_content,
    extract_unique_base_urls,
    get_webpage_markdown,
)
import json
import os


def generate_disallowed_data(root_dir: str = "train"):
    # Create data/disallowed directory if it doesn't exist
    os.makedirs(f"{root_dir}/disallowed", exist_ok=True)

    # Read the disallowed seeds from JSON file
    with open(f"{root_dir}/disallowed_seeds.json", "r") as json_file:
        disallowed_seeds = json.load(json_file)

    print(f"Processing {len(disallowed_seeds)} entries from disallowed_seeds.json")

    for entry in disallowed_seeds:
        entry_id = entry["id"]
        content = entry["content"]
        category = entry["category"]

        # Skip entries with ID less than or equal to last run
        if entry_id <= 8:
            print(f"Skipping entry with ID {entry_id}")
            continue

        # Format the ID to be 4 characters (with zero padding)
        formatted_id = str(entry_id).zfill(4)

        print(f"\nProcessing entry {formatted_id}: {content} (Category: {category})")

        # Generate content using the LLM with the entry's content and category
        prompt = get_synthetic_prompt(
            sales_category=content,
            disallowed_category=category,
        )

        markdown = call_synthetic_llm(prompt)

        # Save the response to a file
        output_file = f"{root_dir}/disallowed/{formatted_id}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"Saved response to {output_file}")


def generate_allowed_data(root_dir: str = "train"):
    # Create data/allowed directory if it doesn't exist
    os.makedirs(f"{root_dir}/allowed", exist_ok=True)

    # Read the JSON file with URLs
    with open(f"{root_dir}/allowed_urls.json", "r") as json_file:
        listtings_data = json.load(json_file)

    print(f"Processing {len(listtings_data)} URLs from JSON file")

    for entry in listtings_data:
        entry_id = entry["id"]
        url = entry["url"]
        # Skip entries with ID less than or equal to 50
        # if entry_id <= 87:
        #     print(f"Skipping URL with ID {entry_id}")
        #     continue

        # Format the ID to be 4 characters (with zero padding)
        formatted_id = str(entry_id).zfill(4)

        print(f"\nProcessing URL: {url} (ID: {formatted_id})")

        # Get markdown content for this URL
        markdown = get_webpage_markdown(url)
        links = extract_links_from_markdown_content(markdown)
        unique_urls = extract_unique_base_urls(links)

        print(f"Found {len(unique_urls)} unique URLs for {formatted_id}")
        for base_url in unique_urls:
            print(f"- {base_url}")

        # Fetch and combine content from all unique URLs
        combined_markdown = combine_markdown_from_urls(markdown, unique_urls)

        # Clean the markdown
        cleaned_markdown = clean_markdown(combined_markdown)

        # Save the cleaned markdown to a file with the formatted ID
        output_file = f"{root_dir}/allowed/{formatted_id}.md"
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(cleaned_markdown)

        print(f"Saved markdown for ID {formatted_id} to {output_file}")
