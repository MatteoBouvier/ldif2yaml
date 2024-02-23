import typer
from typing_extensions import Annotated

from ldifparse.parse import LDIF2YAML_base, LDIF2YAML_tree


def parse(
    file: Annotated[str, typer.Argument(help="file with LDIF data to parse")],
    tree: Annotated[
        bool, typer.Option("--tree", "-t", help="parse as tree structure")
    ] = False,
) -> None:
    """
    Parse LDIF data to YAML format.
    """
    parse_method = LDIF2YAML_tree if tree else LDIF2YAML_base

    with open(file, "r") as input_file:
        parser = parse_method(input_file)
        parser.parse()
        parser.print()


def main():
    typer.run(parse)


if __name__ == "__main__":
    main()
