import typer
from typer.main import get_command


SDIST_SUFFIX = ".tar.gz"
WHEEL_SUFFIX = "-py3-none-any.whl"
COMMAND = "python -m dictnet"
NAME = 'dictnet'


Arg = typer.Argument
Opt = typer.Option


app = typer.Typer(name=NAME)


def setup_cli() -> None:
    # Ensure that the help messages always display the correct prompt
    command = get_command(app)
    command(prog_name=COMMAND)
