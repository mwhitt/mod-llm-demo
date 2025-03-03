from braintrust import Eval
from lib.llm import call_baseline_llm
from lib.prompts import get_moderation_prompt
from lib.regex_scorer import RegexScorer
from lib.utils import collect_file_data


def start_eval_run():
    # Collect data from evaluation files
    allowed_data, disallowed_data = collect_file_data("eval")

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
