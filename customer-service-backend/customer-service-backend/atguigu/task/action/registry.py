from typing import Dict

from task.action.base import Action
from task.action.builtin.action_listen import ActionListen
from task.action.builtin.action_response import ActionResponse
from task.action.custom.action_lookup_order_status import LookupOrderStatusAction


class ActionRegistry:

    def __init__(self):
        self._actions: Dict[str, Action] = {}

    def register(self, action: Action):
        self._actions[action.name] = action

    def get(self,action_name:str) -> Action:
        if action_name not in self._actions:
            raise KeyError(f"Action '{action_name}' not found")
        return self._actions[action_name]


if __name__ == '__main__':
    registry = ActionRegistry()
    registry.register( ActionResponse() )
    registry.register( ActionListen() )
    registry.register( LookupOrderStatusAction() )
