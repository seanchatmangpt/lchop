from lchop.context.browser_context import with_delay
from lchop.context.task_context import register_task
from lchop.context.work_context import WorkContext


@with_delay
@register_task
async def navigate_to_group_members(work_ctx: WorkContext, **kwargs):
    page = work_ctx.browser_ctx.page

    await page.goto("https://chat.openai.com/")
