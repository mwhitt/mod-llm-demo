import click
from dotenv import load_dotenv
from lib.data_helper import generate_allowed_data, generate_disallowed_data
from lib.evaluations import start_eval_run

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
    print("\nModel evaluation completed!")


if __name__ == "__main__":
    cli()
