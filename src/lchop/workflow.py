

import asyncio

import yaml
from munch import Munch

from lchop.browser.browser_context import BrowserContext
from lchop.tasks.task_context import TaskContext
from lchop.work_context import WorkContext
from lchop.template.template_context import TemplateContext
from loguru import logger


def load_template_from_file(self, filename):
    try:
        with open(filename, 'r') as f:
            template_str = f.read()
        self.env.from_string(template_str)
        logger.info(f"Successfully loaded template from file {filename}.")
    except Exception as e:
        logger.error(f"Failed to load template from file {filename}: {str(e)}")
        raise


def render_template_to_file(self, template_str, filename, **kwargs):
    try:
        rendered_content = self.render_template(template_str, **kwargs)
        with open(filename, 'w') as f:
            f.write(rendered_content)
        logger.info(f"Successfully rendered template to file {filename}.")
    except Exception as e:
        logger.error(f"Failed to render template to file {filename}: {str(e)}")
        raise



# async def exe_workflow(workflow_config, work_ctx):
#     logger.info("Starting workflow execution.")
#
#     for task_config in workflow_config.workflow:
#         task_result = await exe_task(task_config, work_ctx)
#
#         if not task_result['success']:
#             logger.error(f"Task {task_config['action']} failed. Stopping workflow.")
#             return False
#
#     logger.info("Workflow execution completed.")
#     return True


from loguru import logger
import yaml


async def inject_tasks(workflow_config, work_ctx):
    logger.info("Attempting to identify and execute 'load_workflow' tasks...")

    # Identify 'load_workflow' tasks and their indices
    load_workflow_indices = [index for index, task in enumerate(workflow_config.workflow) if
                             task.action == 'load_workflow']

    if not load_workflow_indices:
        logger.info("'load_workflow' tasks not found. Skipping injection.")
        return

    for index in reversed(load_workflow_indices):
        task = workflow_config.workflow[index]
        yaml_path = task.params.get('path')

        # If yaml_path is not set, raise an error for a fail-fast approach
        if not yaml_path:
            logger.error("'load_workflow' task found, but no yaml_path specified.")
            raise ValueError("YAML path for 'load_workflow' is not specified.")

        try:
            # Load the new workflows from the given yaml_path
            with open(yaml_path, 'r') as stream:
                new_workflow_config = Munch.fromDict(yaml.safe_load(stream))
                logger.info(f"Successfully loaded new workflow from {yaml_path}")

            # Inject new tasks into the current workflow and remove the 'load_workflow' task
            workflow_config.workflow[index:index + 1] = new_workflow_config['workflow']
            logger.info(f"Injection complete. 'load_workflow' task at index {index} replaced by tasks from {yaml_path}")

        except Exception as e:
            logger.error(f"Failed to load or inject new workflow from {yaml_path}. Exception: {str(e)}")
            raise Exception(f"Failed to load or inject new workflow. Aborting.") from e


async def exe_task(task_config, work_ctx):
    action = task_config.action
    func = work_ctx.task_ctx.tasks[action]
    params = task_config.get('params', {})
    result = await func(work_ctx, **params)
    logger.info(f"Task {action} completed with result: {result}")

    # Update the WorkContext
    work_ctx.task_ctx.results[action] = result

    return result


async def exe_workflow(workflow_config, work_ctx):
    logger.info("Starting workflow execution.")

    # Inject tasks into the workflow as needed
    await inject_tasks(workflow_config, work_ctx)

    for task_config in workflow_config.workflow:
        task_result = await exe_task(task_config, work_ctx)

        if not task_result['success']:
            logger.error(f"Task {task_config['action']} failed. Stopping workflow.")
            return False

    logger.info(f"Results: {len(work_ctx.task_ctx.results.keys())}")
    logger.info("Workflow execution completed.")
    return True


def load_workflow(yaml_path, work_ctx):
    with open(yaml_path, 'r') as stream:
        try:
            workflow_config = Munch.fromDict(yaml.safe_load(stream))
            asyncio.run(exe_workflow(workflow_config, work_ctx))
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML file: {e}")


if __name__ == '__main__':
    # Initialize WorkContext
    work_ctx = WorkContext(TaskContext(), TemplateContext(), BrowserContext())

    # Load and execute the workflow from a YAML file
    load_workflow('workflows/hello_world_workflow.yaml', work_ctx)
    