import subprocess as sp
from pathlib import Path

import click


@click.command()
@click.argument("file", type=Path)
def embed(file):
    file = Path(file)
    cmd = (
        "gs -dNOPAUSE -dBATCH -sDEVICE=pdfwrite -dPDFSETTINGS=/prepress "
        "-dEmbedAllFonts=true "
        f"-sOutputFile={file.parent/ file.stem}_emb.pdf -f {file}"
    )
    sp.run(cmd.split())


if __name__ == "__main__":
    embed()
