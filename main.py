from src.cli import TodoCLI


def main():
    """Start the CLI application."""
    cli = TodoCLI()
    cli.run()


if __name__ == "__main__":
    main()