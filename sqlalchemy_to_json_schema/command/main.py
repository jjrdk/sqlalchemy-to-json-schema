from pathlib import Path
from typing import Optional, Sequence

import click

from sqlalchemy_to_json_schema.types import (
    DecisionChoice,
    FormatChoice,
    LayoutChoice,
    WalkerChoice,
)
from sqlalchemy_to_json_schema.utils.imports import load_module_or_symbol

DEFAULT_WALKER = WalkerChoice.STRUCTURAL
DEFAULT_DECISION = DecisionChoice.DEFAULT
DEFAULT_LAYOUT = LayoutChoice.SWAGGER_2
DEFAULT_DRIVER = "sqlalchemy_to_json_schema.command.driver:Driver"


@click.command()
@click.option("--format", type=click.Choice([format.value for format in FormatChoice]))
@click.option(
    "--walker",
    type=click.Choice([walker.value for walker in WalkerChoice]),
    default=DEFAULT_WALKER.value,
)
@click.option(
    "--decision",
    type=click.Choice([decision.value for decision in DecisionChoice]),
    default=DEFAULT_DECISION.value,
)
@click.option(
    "--layout",
    type=click.Choice([layout.value for layout in LayoutChoice]),
    default=DEFAULT_LAYOUT.value,
)
@click.option("--depth", type=int)
@click.option("--driver", type=str, default=DEFAULT_DRIVER)
@click.option(
    "--out",
    type=click.Path(
        file_okay=True, dir_okay=False, resolve_path=True, writable=True, path_type=Path
    ),
)
@click.argument("targets", type=str, nargs=-1)
def main(
    targets: Sequence[str],
    walker: str,
    decision: str,
    layout: str,
    driver: str,
    out: Optional[Path] = None,
    format: Optional[str] = None,
    depth: Optional[int] = None,
) -> None:
    driver_cls = load_module_or_symbol(driver)
    driver = driver_cls(WalkerChoice(walker), DecisionChoice(decision), LayoutChoice(layout))  # type: ignore[operator] # noqa: E501
    driver.run(targets, filename=out, format=None if format is None else FormatChoice(format))  # type: ignore[attr-defined] # noqa: E501


if __name__ == "__main__":
    main()
