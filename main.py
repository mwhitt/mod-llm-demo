from dotenv import load_dotenv
from lib.data_helper import generate_allowed_data, generate_disallowed_data
import click

load_dotenv(".env.local")


@click.group()
def cli():
    """Process allowed or disallowed data."""
    print("Hello from mod-llm!")


@cli.command()
def allowed():
    """Process allowed data."""
    print("Processing allowed data...")
    generate_allowed_data()
    print("\nAll URLs processed successfully!")


@cli.command()
def disallowed():
    """Process disallowed data."""
    print("Processing disallowed data...")
    generate_disallowed_data()
    print("\nAll URLs processed successfully!")


if __name__ == "__main__":
    cli()
