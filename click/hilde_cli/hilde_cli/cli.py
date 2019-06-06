from pathlib import Path

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


@cli.command()
@click.argument("workflow")
@click.option("--full", default=False, help="list all options", show_default=True)
@click.pass_obj
def input(obj, workflow, full):
    """provide template settings.in for WORKFLOW.

    Use `hilde input list` to list all possibilites."""

    if workflow.lower() == "list":
        click.echo("Possible workflows:")
        click.echo(obj.workflow_possibilites)

    elif workflow.lower() == "aims":
        click.echo(f"{workflow} coming soon")

    elif workflow.lower() == "phonopy":
        click.echo(f"{workflow} coming soon")

    elif workflow.lower() == "md":
        click.echo(f"{workflow} coming soon")

    else:
        msg = f"hilde input '{workflow}' not available. "
        msg += f"Possibilites:\n  {obj.workflow_possibilites}"
        raise click.UsageError(msg)


@cli.command()
@click.argument("workflow")
@click.option("--settings", default="settings.in", show_default=True)
@click.option("--workdir")
@click.pass_obj
def run(obj, workflow, settings, workdir):
    """run a hilde workflow of type WORKFLOW based on the SETTINGS in directory
    WORKDIR"""

    obj.settings_file = settings
    click.echo(f"Run workflow {workflow} with settings:")
    click.echo(obj.settings_file.read_text())

    if workdir:
        obj.workdir = workdir
    click.echo(f"Run in {obj.workdir}")

