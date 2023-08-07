from collections import namedtuple

_geometry = "geometry.in"

dct = {
    "atoms": _geometry,
    "primitive": _geometry + ".primitive",
    "supercell": _geometry + ".supercell",
}


filenames = namedtuple("filenames", dct.keys())(**dct)

print(filenames)
