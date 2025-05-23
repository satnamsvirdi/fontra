#!/usr/bin/env python

import argparse
import csv
import io
import pathlib
from importlib.resources import files

from glyphsLib.glyphdata import GlyphData


def getGlyphData() -> GlyphData:
    path = files("glyphsLib.data") / "GlyphData.xml"
    with path.open("rb") as f:
        return GlyphData.from_files(f)


def readLicense():
    path = files("glyphsLib.data") / "GlyphData_LICENSE"
    return path.read_text()


attrs = [
    "unicode",
    # "unicodeLegacy",
    "name",
    "category",
    "subCategory",
    "case",
    "direction",
    "script",
    "description",
    "production",
    # "altNames",
]


def glyphDataAsCSV():
    data = getGlyphData()
    license = readLicense()

    f = io.StringIO()

    f.write(
        "# DO NOT EDIT: This file is generated by scripts/rebuild_glyph_data_csv.py\n"
    )
    f.write("# The data is derived from glyphsLib/data/GlyphData.xml\n")
    f.write("#\n")

    for line in license.splitlines():
        line = line.strip()
        f.write(f"# {line}\n" if line else "#\n")
    f.write("\n")

    writer = csv.writer(f, delimiter=";", lineterminator="\n")
    writer.writerow(attrs)
    for attrib in data.names.values():
        row = [attrib.get(attr, "") for attr in attrs]
        writer.writerow(row)

    return f.getvalue()


def rebuildGlyphData(check=False):
    repoDir = pathlib.Path(__file__).resolve().parent.parent
    glyphDataPath = (
        repoDir / "src-js" / "fontra-core" / "assets" / "data" / "glyph-data.csv"
    )

    csvGlyphData = glyphDataAsCSV()

    if check:
        oldData = glyphDataPath.read_text(encoding="utf-8")
        if csvGlyphData != oldData:
            raise ValueError("new source differs from old source")
    else:
        glyphDataPath.write_text(csvGlyphData, encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true", default=False)
    args = parser.parse_args()

    rebuildGlyphData(check=args.check)
