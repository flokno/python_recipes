from pathlib import Path
import importlib.resources as pkg_resources

import click
import attr

INFO_POSSIBILITES = ["geometry", "settings", "trajectory"]
WORKFLOW_POSSIBILITES = ["aims", "phonopy", "md"]


@attr.s
class CliTracker:
    input_filename = attr.ib(default=None)
    geometry_filename = attr.ib(default="geometry.in")
    settings_filename = attr.ib(default="settings.in")
    trajectory_filename = attr.ib(default="trajectory.son")
    config_filename = attr.ib(default="~/.hilderc")
    workdir = attr.ib(default="aims_calculation")

    info_possibilites = attr.ib(default=INFO_POSSIBILITES)
    workflow_possibilites = attr.ib(default=WORKFLOW_POSSIBILITES)

    full_input = attr.ib(default=False)

    @property
    def geometry_file(self):
        return Path(self.geometry_filename)

    @geometry_file.setter
    def geometry_file(self, new_file):
        self.check_path(new_file)
        self.geometry_filename = new_file

    @property
    def settings_file(self):
        return Path(self.settings_filename)

    @settings_file.setter
    def settings_file(self, new_file):
        self.check_path(new_file)
        self.settings_filename = new_file

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


@cli.group()
def info():
    """inform about content of a file"""
    pass


@info.command("geometry")
@click.argument("filename")
@click.pass_obj
def geometry_info(obj, filename):
    """inform about content of a geometry file"""

    obj.geometry_file = filename
    click.echo(obj.geometry_file.read_text())


@info.command("settings")
@click.argument("filename", default="settings.in")
@click.pass_obj
def settings_info(obj, filename):
    """inform about content of a settings.in file"""

    obj.settings_file = filename
    click.echo(obj.settings_file.read_text())


@cli.group()
@click.option("--full", is_flag=True, help="list all options", show_default=True)
@click.pass_obj
def input(obj, full):
    """provide template settings.in for workflows"""
    obj.full_input = full


@input.command("aims")
@click.argument("filename", default="settings.in")
@click.option("--allow_overwrite", is_flag=True)
@click.pass_obj
def aims_input(obj, filename, allow_overwrite):
    """provide template settings.in for WORKFLOW.

    Use `hilde input list` to list all possibilites."""

    from .templates import settings

    if obj.full_input:
        template_file = "aims_full"
    else:
        template_file = "aims"

    template = pkg_resources.read_text(settings, template_file)

    outfile = Path(filename)

    if not allow_overwrite and outfile.exists():
        msg = f"{outfile} exists."
        raise click.ClickException(msg)

    outfile.write_text(template)

    click.echo(f"Default {template_file} settings file written to {filename}.")


@cli.group()
@click.option("--workdir", help="provide a working directory to run the calculation")
@click.option("--settings", default="settings.in", show_default=True)
@click.pass_obj
def run(obj, workdir, settings):
    """run a hilde workflow"""
    obj.workdir = workdir
    obj.settings_file = settings


@run.command("aims")
@click.pass_obj
def run_aims(obj):
    """run and aims calculation"""

    click.echo(f"run aims coming soon")
