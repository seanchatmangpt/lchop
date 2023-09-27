from dataclasses import dataclass

from typetemp.template.typed_template import TypedTemplate

from lchop.context.task_context import register_task


@dataclass
class NewTypedTemplate(TypedTemplate):
    message: str = None
    source = "Hello, {{ message }}"


@register_task
async def type_temp(work_ctx, message="Hello, World!", **kwargs):
    temp = NewTypedTemplate(message=message)
    return {"success": True, "results": f"Successfully templated: {temp()}"}
