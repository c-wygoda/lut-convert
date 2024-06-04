from io import StringIO
from pathlib import Path

from numpy import array, cbrt, savetxt, uint8
from PIL import Image

from lut_convert.interpolation import interpolate_tetrahedral


def convert(input: Path, out: StringIO, size: int, title: str | None = None):
    with Image.open(input) as hald:
        square = array(hald.convert("RGB"), dtype=uint8)

    if square.shape[0] != square.shape[1]:
        raise RuntimeError("input must be square HALD image")
    input_size = cbrt(square.shape[0] ** 2)
    if input_size % 1 != 0.0:
        raise RuntimeError("invalid input size")
    input_size = int(input_size)

    cube = square.reshape([input_size, input_size, input_size, 3])
    if size != input_size:
        cube = interpolate_tetrahedral(cube, input_size, size)

    headers = []
    if title:
        headers.append(f'TITLE "{title}"')
    headers += ["DOMAIN_MIN 0 0 0", "DOMAIN_MAX 1 1 1", f"LUT_3D_SIZE {size}"]
    savetxt(
        out,
        cube.reshape([-1, 3]) / 255,
        fmt="%.9f",
        header="\n".join(headers),
        comments="",
    )
