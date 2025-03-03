import os
import anthropic
from typing import Optional
import httpx


def call_baseline_llm(prompt: str) -> str:
    url = "https://api.fireworks.ai/inference/v1/chat/completions"
    payload = {
        "model": "accounts/fireworks/models/llama-v3p3-70b-instruct",
        "messages": [{"role": "user", "content": prompt}],
    }
    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"Bearer {os.environ.get('FIREWORKS_API_KEY')}",
    }

    response = httpx.post(url, headers=headers, json=payload)
    response_json = response.json()
    text_content = ""
    # Parse the response JSON to extract the message content
    if "choices" in response_json and len(response_json["choices"]) > 0:
        # Extract the content from the first choice's message
        if (
            "message" in response_json["choices"][0]
            and "content" in response_json["choices"][0]["message"]
        ):
            text_content = response_json["choices"][0]["message"]["content"]
            return text_content
    raise Exception("No content found in response")


def call_synthetic_llm(
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
