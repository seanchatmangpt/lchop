import click

from lchop.browser.browser_context import BrowserContext
from lchop.tasks import TaskContext
from lchop.template.template_context import TemplateContext
from lchop.work_context import WorkContext
from lchop.workflow import load_workflow


@click.command()
@click.argument('file', type=click.Path(exists=True), default='workflow.yaml', required=False)
def cli(file):
    """
    CLI interface for running workflows.

    :param file: The YAML file containing the workflow configuration. Defaults to workflow.yaml.
    """
    # Initialize WorkContext
    work_ctx = WorkContext(TaskContext(), TemplateContext(), BrowserContext())

    # Load and execute the workflow from the specified YAML file
    load_workflow(file, work_ctx)


if __name__ == '__main__':
    cli()
