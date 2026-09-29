from typing import Dict, Any

from domain.messages import BotMessage, MessageObject
from domain.state import DialogueState
from task.action.base import Action, ActionResult


class RecommendSimilarProductsAction(Action):

    name = "action_recommend_similar_products"

    async def run(self, state:DialogueState, args:Dict[str,Any]) ->ActionResult:
        return ActionResult(
            messages=[
                BotMessage(object=MessageObject()
                )
            ]
        )
