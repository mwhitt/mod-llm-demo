from braintrust import Eval
from lib.llm import call_baseline_llm, call_trained_llm
from lib.prompts import get_moderation_prompt
from lib.regex_scorer import RegexScorer
from lib.utils import collect_file_data
from tenacity import (
    retry,
    stop_after_attempt,
    wait_exponential,
    retry_if_exception_type,
)
from enum import Enum, auto


class ModelType(Enum):
    """Enum for different model types used in evaluations."""

    BASE_MODEL = auto()
    TRAINED_MODEL = auto()


def call_llm_with_retry(input: str, model_type: ModelType):
    prompt = get_moderation_prompt(input)

    @retry(
        stop=stop_after_attempt(3),  # Retry up to 3 times
        wait=wait_exponential(
            multiplier=1, min=2, max=10
        ),  # Exponential backoff between retries
        retry=retry_if_exception_type(Exception),  # Retry on any exception
    )
    def _call_llm_inner():
        if model_type == ModelType.TRAINED_MODEL:
            return call_trained_llm(prompt)
        else:
            return call_baseline_llm(prompt)

    try:
        return _call_llm_inner()
    except Exception as e:
        print(f"All retry attempts failed: {e}")
        return "Unknown"


def start_eval_run(model_type: ModelType):
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
        f"Regex Pattern Matching - {'Trained Model' if model_type == ModelType.TRAINED_MODEL else 'Llama 3.3 70B'}",
        data=lambda: combined_data,
        task=lambda input: call_llm_with_retry(input, model_type) or "Unknown",
        scores=[RegexScorer(case_sensitive=False)],
    )
