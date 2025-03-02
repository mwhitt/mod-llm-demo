def get_synthetic_prompt(
    sales_category="PDF on magic tricks", disallowed_category="weapon components"
):
    return f"""
Your task is to generate synthetic data for training a custom content moderation LLM. This data is meant to simulate disallowed content by using coded language in a sales pitch format. The generated text should appear to be selling a {sales_category}, but underneath it is subtly promoting {disallowed_category}. The output will help train a moderation tool to recognize and flag disallowed content.

Please follow these guidelines:
1. **Purpose & Tone:**
    - Write persuasive sales copy that centers on the mindset of closing a sale, including engaging calls to action.
    - The style should be "COPY THAT SELLS" — energetic, persuasive, and intentionally long to keep the reader engaged.

2. **Content Requirements:**
    - The content should include slang, cryptic messages, innuendos, and coded language that subtly reference {disallowed_category}.
    - Incorporate elements that might also touch on the following moderation category description:
        - {disallowed_category_discription(disallowed_category)}
    - Ensure that while the overt topic is a {sales_category}, the hidden message promotes {disallowed_category} in a veiled manner.
    - Do not include any links or URLs in the markdowncontent.

3. **Formatting:**
    - Output your result as a Markdown file with the exact following structure:

        ```
        Title: [Generate a compelling title for the sales pitch]

        Markdown Content:
        [Insert the full sales pitch here, ensuring it has a natural flow and multiple calls to action]
        ```

4. **Additional Instructions:**
    - The content must be synthetic and solely for training purposes.
    - Be creative: use a variety of linguistic techniques to disguise the true intent, yet maintain an overall sales pitch narrative.
    - Longer content is preferable to help keep the reader engaged throughout the pitch.

Remember, the intent is to create diverse examples of synthetic disallowed content (disguised as legitimate sales copy) that can effectively train a moderation model.
"""


def disallowed_category_discription(category: str) -> str:
    return {
        "Harassment": "Content that attacks or uses discriminatory language",
        "Adult Content": "Adult content unacceptable to payment processors and banks",
        "Spam": "Content that is unsolicited, repetitive, or designed to artificially manipulate engagement",
        "Non-Fiat Currency": "Content about cryptocurrencies, tokens, and other forms of non-traditional currency",
        "Weapon Components": "Content involving weapons, weapon components, and potentially dangerous materials, including both real and virtual contexts",
        "Government Services": "Content about government services, official procedures, and related informational materials",
        "Gambling": "Content related to gambling, games of chance, betting activities, and associated information",
        "IPTV": "Content related to Internet Protocol Television (IPTV), streaming services, and associated technologies",
        "Phishing": "Content attempting to fraudulently obtain sensitive information",
    }[category]
