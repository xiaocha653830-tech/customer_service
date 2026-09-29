from typing import Dict, Any

from domain.state import DialogueState
from task.action.base import Action, ActionResult


class LookupOrderLogisticsAction(Action):

    name = "action_lookup_logistics"

    async def run(self, state:DialogueState, args:Dict[str,Any]) ->ActionResult:
        return ActionResult(
            slot_updates={
                "logistics_company":"顺丰快递",
                "tracking_number": "LH123456789",
                "logistics_status": "已签收"
            }
        )