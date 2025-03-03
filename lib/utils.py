import os


def collect_file_data(root_dir: str):
    """
    Collect data from evaluation files in eval/allowed and eval/disallowed directories.

    Returns:
        tuple: A tuple containing two arrays (allowed_data, disallowed_data),
               where each array contains dictionaries with file info and content.
    """
    allowed_data = []
    disallowed_data = []

    # Process allowed data
    allowed_dir = os.path.join(root_dir, "allowed")
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
    disallowed_dir = os.path.join(root_dir, "disallowed")
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
