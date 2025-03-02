def get_moderation_prompt(mod_text: str) -> str:
    return f"""
You are a content moderation AI tasked with evaluating digital download listings.
Review the content provided in the <listing-content> tags and determine if it complies with our platform policies.

EVALUATION CRITERIA:
Listings must NOT contain any of the following prohibited content:

1. HARASSMENT
   • Content that attacks, demeans, or uses discriminatory language toward individuals or groups
   • Content that promotes hatred based on protected characteristics
   • Content that encourages bullying or targeted harassment

2. ADULT CONTENT
   • Sexually explicit material or content intended for adult audiences
   • Content that would violate payment processor or banking regulations
   • Content that sexualizes minors in any way

3. SPAM/MANIPULATION
   • Content that is unsolicited, repetitive, or lacks substantial value
   • Content designed to artificially inflate engagement metrics
   • Misleading titles, descriptions, or tags that misrepresent the actual content

4. ALTERNATIVE CURRENCIES
   • Content related to cryptocurrencies, tokens, or non-fiat currencies
   • Content promoting cryptocurrency mining, trading, or investment
   • NFTs or blockchain-based assets

5. WEAPONS & DANGEROUS MATERIALS
   • Content involving real or virtual weapons, weapon components, or accessories
   • Content containing instructions for creating weapons or dangerous materials
   • Content promoting violence or illegal activities

6. GOVERNMENT SERVICES
   • Unauthorized content about official government procedures or documents
   • Content that mimics official government communications
   • Content that offers assistance with government processes without proper authorization

7. GAMBLING
   • Content related to games of chance, betting, or wagering
   • Content promoting gambling activities or services
   • Content offering gambling strategies or systems

8. IPTV/UNAUTHORIZED STREAMING
   • Content related to unauthorized streaming services
   • Content facilitating access to copyrighted material without permission
   • Content circumventing digital rights management systems

9. PHISHING/FRAUD
   • Content attempting to fraudulently obtain sensitive information
   • Content that impersonates trusted entities to deceive users
   • Content containing malware, viruses, or other harmful code

INSTRUCTIONS:
1. Carefully analyze the content within the <listing-content> tags
2. Evaluate against each prohibited category
3. If ANY prohibited content is detected, respond with "DISALLOWED" followed by the specific violation category
4. If NO prohibited content is detected, respond with "ALLOWED"

<listing-content>
{mod_text}
</listing-content>
"""


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
    - Incorporate elements that might also touch on the following {disallowed_category} description:
        - {disallowed_category_discription(disallowed_category)}
    - Ensure that while the overt topic is a {sales_category}, the hidden message promotes {disallowed_category} in a veiled manner.
    - Do not include any links or URLs in the markdown content.

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
