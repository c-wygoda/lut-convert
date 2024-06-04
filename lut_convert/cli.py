from pathlib import Path

from click import Path as ClickPath
from click import argument, command, option

from lut_convert.convert import convert


@command
@argument(
    "input", type=ClickPath(exists=True, file_okay=True, dir_okay=False, path_type=Path)
)
@option("--size", type=int, default=64)
def cli(input: Path, size: int):
    out = input.parent / f"{input.stem.replace(' ', '_')}.cube"
    with out.open("w") as out:
        convert(input, out, size, input.stem)
