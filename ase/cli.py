import click

@click.command("upload", context_settings=_default_context_settings)
@click.argument("files", nargs=-1, type=complete_files)
@click.option("--token", help="nomad token, otherwise read from .vibesrc")
@click.option("--name", help="nomad upload name")
@click.option("--legacy", is_flag=True, help="use old Nomad")
@click.option("--dry", is_flag=True, help="only show the commands")
def tool_nomad_upload(files, token, name, legacy, dry):
    """upload FILES to NOMAD"""
    from .scripts.nomad_upload import nomad_upload

    nomad_upload(files, token, legacy, dry, name=name


