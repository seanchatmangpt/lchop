

import asyncio

import yaml
from munch import Munch

from lchop.browser_context import BrowserContext
from lchop.task_context import TaskContext
from lchop.work_context import WorkContext
from lchop.template_context import TemplateContext
from loguru import logger

from lchop.tasks.chief_of_staff_gpt_tasks import *

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



@TaskContext.register_task
async def print_hello(work_ctx, message="Hello, World!"):
    logger.info(f"Executing task: print_hello")
    logger.info(f"Message: {message}")
    return {'success': True, 'results': f"Successfully printed: {message}"}

@TaskContext.register_task
async def print_goodbye(work_ctx, message="Goodbye, World!"):
    logger.info(f"Executing task: print_goodbye")
    logger.info(f"Message: {message}")
    return {'success': True, 'results': f"Successfully printed: {message}"}

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


async def inject_tasks(workflow_config, work_ctx):
    # Logic to inject tasks based on the conditions or configurations
    injected_tasks = []  # Assume this list contains the tasks you want to inject.

    # Insert the tasks into the workflow_config right after the 'load_workflow' task
    for index, task in enumerate(workflow_config.workflow):
        if task.action == 'load_workflow':
            workflow_config.workflow[index + 1:index + 1] = injected_tasks
            break


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
    load_workflow('your_workflow.yaml', work_ctx)
    