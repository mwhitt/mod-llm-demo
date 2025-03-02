import re
from autoevals import Score


class RegexScorer:
    """
    A custom scorer for the braintrust eval library that uses regex pattern matching
    instead of exact output matching.

    The expected value should be a regex pattern string that will be matched against
    the output.

    Returns:
        Score: A Score object with score 1.0 if the output matches the regex pattern,
              and 0.0 otherwise.
    """

    name = "regex_matching"

    def __init__(self, case_sensitive=True):
        """
        Initialize the RegexScorer.

        Args:
            case_sensitive (bool): Whether to perform case-sensitive matching (default: True)
        """
        self.case_sensitive = case_sensitive

    def __call__(self, output, expected, input=None):
        """
        Score whether the output matches the expected regex pattern.

        Args:
            output (str): The output to evaluate
            expected (str): The expected regex pattern to match against
            input (str, optional): The input that generated the output (not used)

        Returns:
            Score: A Score object with score 1.0 if the output matches the regex pattern,
                  and 0.0 otherwise.
        """
        # Handle case sensitivity
        flags = 0 if self.case_sensitive else re.IGNORECASE

        try:
            # Try to compile the regex pattern
            pattern = re.compile(expected, flags)

            # Check if the pattern matches the output
            match = pattern.search(output)
            score = 1.0 if match else 0.0

            # Return a Score object with the match result
            return Score(
                name=self.name,
                score=score,
                metadata={
                    "pattern": expected,
                    "match": bool(match),
                    "case_sensitive": self.case_sensitive,
                    "matched_text": match.group(0) if match else None,
                },
            )
        except re.error as e:
            # Handle invalid regex pattern
            return Score(
                name=self.name,
                score=0.0,
                metadata={
                    "error": f"Invalid regex pattern: {str(e)}",
                    "pattern": expected,
                },
            )
