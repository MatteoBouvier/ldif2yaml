import json
import yaml
import typer
from typing import Callable
from typing_extensions import Annotated

from ldifparse.parse import Parser_base, Parser_tree


def get_dump_method(output_format: str) -> Callable:
    if output_format in {"json", "j"}:
        return json.dump

    elif output_format in {"yaml", "y"}:
        return yaml.dump

    raise ValueError(f"Invalid option '{output_format}' for parameter 'output'")


def parse(
    file: Annotated[str, typer.Argument(help="file with LDIF data to parse")],
    tree: Annotated[
        bool, typer.Option("--tree", "-t", help="parse as tree structure")
    ] = False,
    output_format: Annotated[
        str, typer.Option("--output", "-o", help="output format (json | yaml)")
    ] = "yaml",
) -> None:
    """
    Parse LDIF data to YAML format.
    """
    parse_method = Parser_tree if tree else Parser_base
    dump_method = get_dump_method(output_format)

    with open(file, "r") as input_file:
        parser = parse_method(input_file, dump_method)
        parser.parse()
        parser.print()


def main():
    typer.run(parse)


if __name__ == "__main__":
    main()
