import asyncio
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from munch import Munch

from lchop.context.work_context import (default_work_context, exe_task,
                                        load_workflow)


@pytest.mark.asyncio
async def test_state_context_load_from_file():
    yaml_path = "workflows/prompt_workflow.yaml"
    work_ctx = default_work_context()

    await load_workflow(work_ctx, filepath=yaml_path)
    assert len(work_ctx.task_ctx.results_list) == 2
