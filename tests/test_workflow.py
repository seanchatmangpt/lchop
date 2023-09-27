import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from munch import Munch

from lchop.context.work_context import default_work_context, exe_task


@pytest.mark.asyncio
async def test_exe_task_success():
    task_config = Munch(
        {
            "func": "print_hello",
            "name": "Print Hello",
            "description": "This task prints Hello to the console.",
            "params": {},
        }
    )

    work_ctx = MagicMock()
    work_ctx.task_ctx.tasks["print_hello"] = AsyncMock(return_value={"success": True})
    work_ctx.task_ctx.tasks["print_hello"].return_value = asyncio.Future()
    work_ctx.task_ctx.tasks["print_hello"].return_value.set_result({"success": True})
    work_ctx.task_ctx.results = {}

    result = await exe_task(task_config, work_ctx)
    assert result["success"] == True
    assert work_ctx.task_ctx.results["print_hello"]["success"] == True


@pytest.mark.asyncio
async def test_state_context_load_from_file():
    yaml_path = "hello_world_workflow.yaml"
    work_ctx = default_work_context()

    await work_ctx.load_workflow(work_ctx, filepath=yaml_path)
    assert work_ctx.task_ctx.results["print_hello"]["success"] == True
    assert work_ctx.task_ctx.results["print_goodbye"]["success"] == True
