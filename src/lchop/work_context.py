from loguru import logger

from lchop.browser_context import BrowserContext
from lchop.task_context import TaskContext
from lchop.template_context import TemplateContext


class WorkContext:
    def __init__(self, task_ctx: TaskContext, template_ctx: TemplateContext, browser_ctx: BrowserContext):
        self.task_ctx = task_ctx
        self.template_ctx = template_ctx
        self.browser_ctx = browser_ctx
        logger.info("WorkContext initialized.")
