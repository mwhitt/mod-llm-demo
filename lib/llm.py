import os
import anthropic
from typing import Optional


def call_llm(
    prompt: str,
    model: str = "claude-3-7-sonnet-20250219",
    max_tokens: int = 20000,
    system_prompt: Optional[str] = None,
) -> str:
    """
    Call the Anthropic Claude LLM with the given prompt.

    Args:
        prompt: The prompt to send to the LLM
        model: The model to use (default: claude-3-opus-20240229)
        max_tokens: Maximum number of tokens to generate (default: 4000)
        temperature: Controls randomness in the output (default: 0.7)
        system_prompt: Optional system prompt to provide context

    Returns:
        The complete response from the LLM as a dictionary
    """
    # Get API key from environment variables
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set")

    # Initialize the Anthropic client
    client = anthropic.Anthropic(api_key=api_key)

    # Prepare the message parameters
    message_params = {
        "model": model,
        "max_tokens": max_tokens,
        "thinking": {"type": "enabled", "budget_tokens": 16000},
        "messages": [{"role": "user", "content": prompt}],
    }

    # Add system prompt if provided
    if system_prompt:
        message_params["system"] = system_prompt

    # Call the LLM
    response = client.messages.create(**message_params)
    text_content = ""
    for content_block in response.content:
        if content_block.type == "text":
            text_content += content_block.text

    return text_content.replace("```", "").strip()
