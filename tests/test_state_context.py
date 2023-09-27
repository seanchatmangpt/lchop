import os

import pytest
from sismic.model import MacroStep

from lchop.context.work_context import default_work_context, load_workflow


@pytest.mark.asyncio
async def test_state_context_load_from_file():
    yaml_path = "hello_state_workflow.yaml"
    work_ctx = default_work_context()
    await load_workflow(work_ctx, filepath=yaml_path)
    assert work_ctx.task_ctx.results["state_from_file"]["success"] is True
    assert (
        isinstance(
            work_ctx.task_ctx.results_list[1]["results"]["macro_step"], MacroStep
        )
        is True
    )
    # remove statechart_output.txt
    os.remove("statechart_output.txt")
    assert os.path.exists("statechart_output.txt") is False
