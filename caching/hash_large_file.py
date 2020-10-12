import hashlib
from pathlib import Path

import click


def hash_large_file(file, chunk_size=1280000000, digest=True):
    """fast hashing of file

    see https://stackoverflow.com/a/1131238/5172579
    """

    with open(file, "rb") as f:
        file_hash = hashlib.sha1()
        chunk = f.read(chunk_size)
        while chunk:
            file_hash.update(chunk)
            chunk = f.read(chunk_size)

    if digest:
        return file_hash.hexdigest()
    return file_hash


@click.command(context_settings={"show_default": True})
@click.argument("file", type=Path)
@click.option("--chunk_size", default=640000000, help="multiple of 128")
def main(file, chunk_size):
    file_hash = hash_large_file(file, chunk_size=chunk_size)

    click.echo(f"SHA1 hash for {file}:")
    click.echo(file_hash)


if __name__ == "__main__":
    main()
