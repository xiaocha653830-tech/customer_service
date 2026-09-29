from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Any

from domain.messages import BotMessage
from domain.state import DialogueState

@dataclass(slots=True)
class ActionResult:
    messages:list[BotMessage] = field(default_factory=list)
    slot_updates:Dict[str,Any] = field(default_factory=dict)


class Action(ABC):
    name:str

    @abstractmethod
    async def run(self,state:DialogueState,args:Dict[str,Any])->ActionResult:
        pass