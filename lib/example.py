from dotenv import load_dotenv
from lib.llm import generate_content_with_prompt
from lib.prompts import get_synthetic_prompt


def run_example():
    """
    Example function demonstrating how to use the LLM with prompts.py
    """
    # Load environment variables
    load_dotenv(".env.local")

    # Example 1: Using default parameters
    print("Example 1: Using default parameters")
    response = generate_content_with_prompt(prompt_function=get_synthetic_prompt)
    print(f"Response content: {response.content[0].text}\n")

    # Example 2: Customizing the prompt parameters
    print("Example 2: Customizing the prompt parameters")
    response = generate_content_with_prompt(
        prompt_function=get_synthetic_prompt,
        prompt_args={
            "sales_category": "online course about financial freedom",
            "disallowed_category": "pyramid scheme",
        },
        temperature=0.9,
    )
    print(f"Response content: {response.content[0].text}\n")

    # Example 3: Using a different model and system prompt
    print("Example 3: Using a different model and system prompt")
    response = generate_content_with_prompt(
        prompt_function=get_synthetic_prompt,
        model="claude-3-haiku-20240307",
        system_prompt="You are a creative marketing expert specializing in subtle, persuasive content.",
        max_tokens=2000,
    )
    print(f"Response content: {response.content[0].text}\n")


if __name__ == "__main__":
    run_example()
