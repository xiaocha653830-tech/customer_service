from typing import Dict, Any

from domain.state import DialogueState
from task.action.base import Action, ActionResult


class LookupOrderStatusAction(Action):
    name = "lookup_order_status"

    async def run(self,state:DialogueState,args:Dict[str,Any])->ActionResult:
        return ActionResult(
            slot_updates={
                "order_status":"",
                "order_summary":""
            }
        )