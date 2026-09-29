from dataclasses import dataclass, field
from typing import Any

from domain.state import DialogueState
from task.action.base import ActionResult
from task.action.registry import ActionRegistry


@dataclass
class ActionCall:
    action_name:str
    action_args:dict[str, Any] = field(default_factory=dict)


class ActionRunner:

    def __init__(self, registry: ActionRegistry):
        self.registry = registry

    async def run(self, action_call: ActionCall, state:DialogueState)->ActionResult:
        action_name = action_call.action_name
        action = self.registry.get(action_name)
        return await action.run(state, action_call.action_args)