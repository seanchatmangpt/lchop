from loguru import logger

from lchop.context.task_context import register_task
from lchop.context.work_context import WorkContext


@register_task
async def launch_browser(ctx: WorkContext, **kwargs):
    logger.info("Launching browser...")
    await ctx.browser_ctx.launch_browser(**kwargs)

    return {
        "success": True,
        "results": f"Successfully launched browser",
    }
