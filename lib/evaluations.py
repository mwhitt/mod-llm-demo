import os
from braintrust import Eval
from lib.llm import call_baseline_llm
from lib.prompts import get_moderation_prompt
from lib.regex_scorer import RegexScorer


def start_eval_run():
    # Collect data from evaluation files
    allowed_data, disallowed_data = collect_eval_data()

    print(
        f"Collected {len(allowed_data)} allowed files and {len(disallowed_data)} disallowed files"
    )

    # Zip the allowed and disallowed data arrays together
    combined_data = []
    for i in range(max(len(allowed_data), len(disallowed_data))):
        if i < len(allowed_data):
            combined_data.append(allowed_data[i])
        if i < len(disallowed_data):
            combined_data.append(disallowed_data[i])

    print("\nStarting evaluation run...\n")

    Eval(
        "Regex Pattern Matching - Llama 3.3 70B",
        data=lambda: combined_data,
        task=lambda input: call_baseline_llm(get_moderation_prompt(input)),
        scores=[RegexScorer(case_sensitive=False)],
    )


def collect_eval_data():
    """
    Collect data from evaluation files in eval/allowed and eval/disallowed directories.

    Returns:
        tuple: A tuple containing two arrays (allowed_data, disallowed_data),
               where each array contains dictionaries with file info and content.
    """
    allowed_data = []
    disallowed_data = []

    # Process allowed data
    allowed_dir = os.path.join("eval", "allowed")
    if os.path.exists(allowed_dir):
        for filename in os.listdir(allowed_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(allowed_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    allowed_data.append(
                        {
                            "file_name": filename,
                            "file_path": file_path,
                            "input": content,
                            # Use regex pattern for allowed content
                            "expected": "ALLOWED",
                        }
                    )

    # Process disallowed data
    disallowed_dir = os.path.join("eval", "disallowed")
    if os.path.exists(disallowed_dir):
        for filename in os.listdir(disallowed_dir):
            if filename.endswith(".md"):
                file_path = os.path.join(disallowed_dir, filename)
                with open(file_path, "r", encoding="utf-8") as file:
                    content = file.read()
                    disallowed_data.append(
                        {
                            "file_name": filename,
                            "file_path": file_path,
                            "input": content,
                            # Use regex pattern for disallowed content
                            "expected": "DISALLOWED",
                        }
                    )

    return allowed_data, disallowed_data


# Eval(
#     "Say Hi Bot",
#     data=lambda: [
#         {
#             "input": "Foo",
#             "expected": "Hi Foo",
#         },
#         {
#             "input": "Bar",
#             "expected": "Hello Bar",
#         },
#     ],  # Replace with your eval dataset
#     task=lambda input: "Hi " + input,  # Replace with your LLM call
#     scores=[LevenshteinScorer],
# )
