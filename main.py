import click
from dotenv import load_dotenv
from lib.data_helper import generate_allowed_data, generate_disallowed_data
from lib.evaluations import start_eval_run
from lib.llm import call_baseline_llm
from lib.prompts import get_moderation_prompt

load_dotenv(".env.local")


@click.group()
def cli():
    """Process allowed or disallowed data."""
    print("Hello from mod-llm!")


@cli.command()
def generate_allowed():
    """Process allowed data."""
    print("Processing allowed data...")
    generate_allowed_data(root_dir="eval")
    print("\nAll URLs processed successfully!")


@cli.command()
def generate_disallowed():
    """Process disallowed data."""
    print("Processing disallowed data...")
    generate_disallowed_data(root_dir="eval")
    print("\nAll URLs processed successfully!")


@cli.command()
def run_eval():
    """Run model evaluation."""
    print("Running model evaluation...")
    start_eval_run()
    # import os

    # # Read the first .md file from eval/allowed directory
    # allowed_dir = os.path.join("eval", "disallowed")
    # input = ""

    # if os.path.exists(allowed_dir):
    #     for filename in os.listdir(allowed_dir):
    #         if filename.endswith(".md"):
    #             file_path = os.path.join(allowed_dir, filename)
    #             with open(file_path, "r", encoding="utf-8") as file:
    #                 input = file.read()
    #             break  # Stop after reading the first file

    # if not input:
    #     print("No .md files found in eval/allowed directory")
    #     return

    # response = call_baseline_llm(get_moderation_prompt(input))
    # print(response)
    print("\nModel evaluation completed!")


if __name__ == "__main__":
    cli()
