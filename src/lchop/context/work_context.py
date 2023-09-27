import yaml
from loguru import logger
from munch import Munch

from lchop.context.agent_context import AgentContext
from lchop.context.browser_context import BrowserContext
from lchop.context.state_context import StateContext
from lchop.context.task_context import TaskContext
from lchop.context.template_context import TemplateContext


class WorkContext:
    globals()

    def __init__(
        self,
        task_ctx: TaskContext,
        template_ctx: TemplateContext,
        browser_ctx: BrowserContext,
        agent_ctx: AgentContext,
        state_ctx: StateContext,
    ):
        self.task_ctx = task_ctx
        self.template_ctx = template_ctx
        self.browser_ctx = browser_ctx
        self.agent_ctx = agent_ctx
        self.state_ctx = state_ctx
        self.global_params = Munch()
        logger.info("WorkContext initialized.")


async def inject_tasks(workflow_config, work_ctx):
    logger.info("Attempting to identify and execute 'load_workflow' tasks...")

    load_workflow_indices = [
        index
        for index, task in enumerate(workflow_config.workflow)
        if task.name == "load_workflow"
    ]

    if not load_workflow_indices:
        logger.info("'load_workflow' tasks not found. Skipping injection.")
        return

    for index in reversed(load_workflow_indices):
        task = workflow_config.workflow[index]
        filepath = task.params.get("path")

        if not filepath:
            logger.error("'load_workflow' task found, but no filepath specified.")
            raise ValueError("YAML path for 'load_workflow' is not specified.")

        try:
            with open(filepath, "r") as stream:
                new_workflow_config = Munch.fromDict(yaml.safe_load(stream))
                logger.info(f"Successfully loaded new workflow from {filepath}")

            workflow_config.workflow[index : index + 1] = new_workflow_config[
                "workflow"
            ]
            logger.info(
                f"Injection complete. 'load_workflow' task at index {index} replaced by tasks from {filepath}"
            )

        except Exception as e:
            logger.error(
                f"Failed to load or inject new workflow from {filepath}. Exception: {str(e)}"
            )
            raise Exception(f"Failed to load or inject new workflow. Aborting.") from e


async def exe_task(task_config, work_ctx):
    func_name = None
    if hasattr(task_config, "func"):
        func_name = task_config.func
    else:
        func_name = task_config.name
    func_desc = task_config.get("description", "No Description")

    logger.info(f"Executing {func_name}: {func_desc}")

    implementation = work_ctx.task_ctx.tasks[func_name]
    global_params = work_ctx.global_params
    params = task_config.get("params", {})
    params["work_ctx"] = work_ctx
    params.update(work_ctx.__dict__)
    params.update(global_params)
    result = await implementation(**params)

    logger.info(f"Task {func_name} completed with result: {result}")

    work_ctx.task_ctx.results[func_name] = result
    work_ctx.task_ctx.results_list.append(result)

    return result


async def exe_workflow(workflow_config, work_ctx):
    logger.info("Starting workflow execution.")

    await inject_tasks(workflow_config, work_ctx)

    for task_config in workflow_config.workflow:
        task_result = await exe_task(task_config, work_ctx)

        if not task_result["success"]:
            logger.error(
                f"Task {task_config['name']} ({task_config['func']}) failed. Stopping workflow."
            )
            return False

    logger.info(f"Results: {len(work_ctx.task_ctx.results.keys())}")
    logger.info("Workflow execution completed.")
    return True


async def load_workflow(work_ctx, filepath=None, yaml_string=None):
    if not filepath and not yaml_string:
        raise ValueError("Either filepath or yaml_string must be specified.")
    if yaml_string:
        workflow_config = Munch.fromDict(yaml.safe_load(yaml_string))
        work_ctx.global_params = workflow_config.get("global_params", {})
        return await exe_workflow(workflow_config, work_ctx)
    with open(filepath, "r") as stream:
        try:
            workflow_config = Munch.fromDict(yaml.safe_load(stream))
            work_ctx.global_params = workflow_config.get("global_params", {})
            return await exe_workflow(workflow_config, work_ctx)
        except yaml.YAMLError as e:
            logger.error(f"Error loading YAML file: {e}")


def default_work_context():
    return WorkContext(
        TaskContext(),
        TemplateContext(),
        BrowserContext(),
        AgentContext(),
        StateContext(),
    )
