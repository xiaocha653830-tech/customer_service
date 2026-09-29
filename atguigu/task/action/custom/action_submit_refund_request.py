from typing import Dict, Any

from domain.state import DialogueState
from task.action.base import Action, ActionResult


class SubmitRefundRequestAction(Action):

    name = "aciton_submit_refund_request"

    async def run(self, state:DialogueState, args:Dict[str,Any]) ->ActionResult:
        return ActionResult(
            slot_updates={
                "order_submit_status":"success"
            }
        )
