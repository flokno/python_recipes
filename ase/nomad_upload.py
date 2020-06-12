""" Summarize output from ASE.md class (in md.log) """

import json
import shutil
import subprocess
import tarfile
import tempfile
from argparse import ArgumentParser
from pathlib import Path

from vibes import Settings
from vibes.helpers import Timer, talk

new_addr = "http://repository.nomad-coe.eu/app/api/uploads/?token="
old_addr = "http://nomad-repository.eu:8000"
upload_folder_dry = "nomad_upload_dry"


def upload_command(
    files: list,
    token: str,
    legacy: bool = False,
    name: str = None,
    nojson: bool = False,
) -> str:
    """Generate the NOMAD upload command

    Args:
        folder: The folder to upload
        token: The NOMAD token
        legacy: use old NOMAD
        name: nomad upload name
        nojson: don't retrieve json summary

    Returns:
        str: The upload command
    """
    name_str = ""
    if name is not None:
        name_str = f"&name={name}"

    json_str = " -H 'Accept: application/json'"
    if nojson:
        json_str = ""

    file_str = " ".join((str(f) for f in sorted(files)))
    cmd = f"tar cf - {file_str} | "

    if legacy:
        cmd = +(f"curl -XPUT -# -HX-Token:{token} " f"-N -F file=@- {old_addr}")
    else:
        cmd += f'curl "{new_addr}{token}{name_str}" {json_str} -T'

    cmd += " - | xargs -0 echo"

    return cmd


def nomad_upload(
    files: list = None,
    token: str = None,
    legacy: bool = False,
    dry: bool = False,
    name: str = None,
    tmp_prefix: str = "nomad_upload_",
    summary_file: str = "nomad.json",
) -> None:
    """upload folders with calculations to NOMAD

    Args:
        files: The files to upload
        token: The NOMAD token
        legacy: use old NOMAD
        dry: only show upload command
        name: nomad upload name
        tmp_prefix: name of the tmpdir prefix to be used to upload from
        summary_file: if given, write nomad summary json file
    """
    timer = Timer("Perform Nomad upload")

    settings = Settings()

    if not token and "nomad" in settings:
        token = settings.nomad.token

    if token is None:
        exit("** Token is missing, chech your .vibesrc or provide manually")

    # from ASE
    if files is None:
        exit("No folders specified -- another job well done!")

    # copy files to tmpdir, unzip if necessary
    tmp_files = []
    if dry:
        tmp_dir = Path(upload_folder_dry)
    else:
        tmp_dir = Path(tempfile.mkdtemp(prefix=tmp_prefix, dir="."))
    for file in files:
        path = tmp_dir / file
        if path.suffix == ".tgz":
            path = tmp_dir / Path(file).parent / path.stem

        if path.exists():
            talk(f'Clean up "{path}"')
            shutil.rmtree(path)

        talk(f'Exctract "{file}" into "{path}"')
        try:
            with tarfile.open(file) as f:
                f.extractall(path=path)
            tmp_files.append(path)
        except IsADirectoryError:
            shutil.copytree(file, path)
            tmp_files.append(path)
        except tarfile.ReadError:
            talk(f'** Read error for file "{file}"')

    # upload
    cmd = upload_command(tmp_files, token, legacy, name=name)
    print(f"Upload command:\n{cmd}")

    if dry:
        return

    outp = subprocess.run(cmd, shell=True, text=True, capture_output=True)
    shutil.rmtree(tmp_dir)
    timer(f"Nomad upload finished")

    summary = json.dumps(json.loads(outp.stdout), indent=2)
    if summary_file is not None:
        Path(summary_file).write_text(summary)
        talk(f"JSON summary written to {summary_file}")
    else:
        print("# json summary")
        print(summary)


def main():
    """ main routine """
    parser = ArgumentParser(description="Upload folder to Nomad")
    parser.add_argument("folders", nargs="+", help="folder containing data to upload")
    parser.add_argument("--token", help="Nomad token for uploads")
    parser.add_argument("--dry", action="store_true", help="only show command")
    args = parser.parse_args()

    nomad_upload(args.folders, args.token, args.dry)


if __name__ == "__main__":
    main()
