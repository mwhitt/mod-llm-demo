import os
from dotenv import load_dotenv
import httpx

load_dotenv(".env.local")

def main():
    print("Hello from mod-llm!")
    url = 'https://rawcaptureguide.gumroad.com/l/captureone2025guide'
    markdown = get_webpage_markdown(url)
    print(markdown)


def get_webpage_markdown(url: str) -> str:
    base_url = 'https://r.jina.ai/'
    headers = {
        'Authorization': 'Bearer ' + os.getenv("JINA_API_KEY")
    }

    with httpx.Client() as client:
        response = client.get(base_url + url, headers=headers)
    return response.text


if __name__ == "__main__":
    main()
