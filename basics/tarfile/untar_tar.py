import tarfile
from pathlib import Path

_default_files = ("aims.out", "control.in", "geometry.in")

archive = Path("calculations")
outfile = Path(f"{archive}.tgz")

# untar backup.tgz
with tarfile.open("backup.tgz") as tar:
    tar.extractall()

# save wanted files to calculations.tgz
with tarfile.open(outfile, "w:gz") as tar:
    for file in archive.glob("*"):
        if file.name in _default_files:
            tar.add(file)
