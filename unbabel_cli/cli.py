import click

from unbabel_cli import core
from unbabel_cli import helpers


@click.command()
@click.option(
    '--input_file',
    default="../events.json",
    help='The input file containing the events.',
    show_default=True,
    required=True
)
@click.option(
    '--window_size',
    default=10,
    help='Rolling mean window size.',
    show_default=True
)
def run(input_file: str, window_size: int):
    click.echo(
        helpers.to_json(core.calculate_moving_average(
            helpers.extract_events_from_input_file(input_file),
            window_size
        ))
    )
