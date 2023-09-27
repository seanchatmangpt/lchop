from types import CodeType
from typing import Any, Dict, Mapping

from sismic.code import PythonEvaluator
from sismic.code.context import FrozenContext
from sismic.interpreter import Interpreter


class ExtPythonEvaluator(PythonEvaluator):
    def __init__(
        self, interpreter=None, *, initial_context: Mapping[str, Any] = None
    ) -> None:
        super().__init__(interpreter, initial_context=initial_context)

        self._context = {}  # type: Dict[str, Any]
        self._context.update(initial_context if initial_context else {})
        self._interpreter = interpreter

        # Precompiled code
        self._evaluable_code = {}  # type: Dict[str, CodeType]
        self._executable_code = {}  # type: Dict[str, CodeType]

        # Frozen context for __old__
        self._memory = {}  # type: Dict[int, FrozenContext]


class ExtendedInterpreter(Interpreter):
    def __init__(self, statechart, work_ctx, **kwargs):
        super().__init__(statechart, evaluator_klass=ExtPythonEvaluator, **kwargs)
        self.work_ctx = work_ctx

    async def execute_special_action(self, action: str, **kwargs):
        task_config = {"name": action, "params": kwargs}
        result = await self.work_ctx.exe_task(task_config, self.work_ctx)
        return result
