from pathlib import Path
import importlib.resources as pkg_resources

import click
import click_completion
import attr

INFO_POSSIBILITES = ["geometry", "settings", "trajectory"]
WORKFLOW_POSSIBILITES = ["aims", "phonopy", "md"]


def complete(self, ctx, incomplete):

    if incomplete.startswith("/"):
        path_orig = incomplete
    else:
        path_orig = os.path.join(os.getcwd(), incomplete)

    path, file_prefix = path_orig.rsplit("/", 1)

    result = []
    if not path:
        path = "/"

    for filename in os.listdir(path):

        if not file_prefix or filename.startswith(file_prefix):

            file_path = os.path.join(path, filename)
            if os.path.isdir(file_path):
                filename += "/"

            if incomplete.startswith("/"):
                result.append(os.path.join(path, filename))
            else:
                result.append(filename)

    return result


click_completion.init(match_incomplete=complete)


@attr.s
class CliTracker:
    input_filename = attr.ib(default=None)

    @property
    def input_file(self):
        return Path(self.input_filename)

    @input_file.setter
    def input_file(self, new_file):
        self.check_path(new_file)
        self.input_filename = new_file

    def check_path(self, filename):
        if not Path(filename).exists() is True:
            msg = f"Current working directory:\n  {Path().cwd()}"
            raise click.FileError(filename, hint=msg)


@click.group()
@click.pass_context
def cli(ctx):
    """hilde Command Line Interface"""
    ctx.obj = CliTracker()
    ctx.help_option_names = ["-h", "--help"]


@cli.command("info")
@click.argument("filename", type=click.Path(exists=True))
@click.pass_obj
def info(obj, filename):
    """inform about content of a geometry file"""

    obj.input_file = filename
    click.echo(obj.input_file.read_text())
