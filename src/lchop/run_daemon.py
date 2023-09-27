import asyncio

from daemon import DaemonContext
from loguru import logger
from munch import Munch

from lchop.context.browser_context import BrowserContext
from lchop.context.task_context import TaskContext
from lchop.context.template_context import TemplateContext
from lchop.context.work_context import WorkContext
from lchop.workflow import exe_workflow

logger.add(
    "/Users/candacechatman/dev/lchop/src/lchop/logfile.log"
)  # <-- Add this line to specify where logs should go

# ... (your existing imports and functions here)

if __name__ == "__main__":
    with DaemonContext(
        stdout=open("stdout.log", "w+"), stderr=open("stderr.log", "w+")
    ):
        # Initialize WorkContext
        work_ctx = WorkContext(TaskContext(), TemplateContext(), BrowserContext())

        # This is just a sample; you may load this dynamically
        workflow_config = {
            "workflow": [{"action": "print_hello"}, {"action": "print_goodbye"}]
        }

        # Convert to munch object for compatibility with your existing code
        workflow_config = Munch.fromDict(workflow_config)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(exe_workflow(workflow_config, work_ctx))
