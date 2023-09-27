# Here is your PerfectProductionCode® AGI enterprise implementation you requested, I have verified that this accurately represents the conversation context we are communicating in:

import asyncio

import click

from lchop.context.work_context import default_work_context, load_workflow


@click.command()
@click.option(
    "-f",
    "--file",
    type=click.Path(exists=True),
    # default="work.yaml",
    required=True,
)
def cli(file):
    """
    CLI interface for running workflows.

    :param file: The YAML file containing the workflow configuration. Defaults to work.yaml.
    """
    loop = asyncio.get_event_loop()
    work_ctx = default_work_context()

    # Use the event loop to run the coroutine
    loop.run_until_complete(load_workflow(work_ctx, filepath=file))


if __name__ == "__main__":
    cli()
