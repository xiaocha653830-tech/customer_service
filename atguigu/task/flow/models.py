#=======================================
# step的next属性 link
#=======================================
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, Any


@dataclass(slots=True)
class FlowStepLink:
    target: str

@dataclass(slots=True)
class ConditionalLink(FlowStepLink):
    conditional:str

@dataclass(slots=True)
class FallbackLink(FlowStepLink):
    pass

@dataclass(slots=True)
class StaticLink(FlowStepLink):
    pass

#=======================================
# flow下的steps属性
#=======================================
@dataclass(slots=True)
class FlowStepType(str, Enum):
    START = "start"
    ACTION = "action"
    COLLECT = "collect "
    END = "end"


@dataclass(slots=True)
class FlowStep:
    id:str
    type:FlowStepType
    next:list[FlowStepLink]

    @classmethod
    def from_dict(cls, dict_data:dict)->"FlowStep":
        step_type = dict_data.get("type")
        if step_type == "start":
            return StartFlowStep.from_dict(dict_data)
        elif step_type == "action":
            return ActionFlowStep.from_dict(dict_data)
        elif step_type == "collect ":
            return CollectFlowStep.from_dict(dict_data)
        elif step_type == "end":
            return EndFlowStep.from_dict(dict_data)

@dataclass(slots=True)
class StartFlowStep(FlowStep):
    @classmethod
    def from_dict(cls, dict_data:dict)->"StartFlowStep":
        return cls(
            id=dict_data["id"],
            type=FlowStepType.START,
            next=_build_next_links(dict_data["next"]),
        )

def _build_next_links(next_data:str | list)->list[FlowStepLink]:
    next_list = []
    if isinstance(next_data, str):
        next_list.append(StaticLink(target=next_data))
    else:
        for link_data in next_data:
            if link_data.get("if"):
                next_list.append(ConditionalLink(
                    conditional=link_data.get("if"),
                    target=link_data.get("then")
                ))
            else:
                next_list.append(FallbackLink(
                    target=link_data.get("else")
                ))
    return next_list

@dataclass(slots=True)
class ActionFlowStep(FlowStep):
    action:str
    args:Dict[str,Any] = field(default_factory=dict)
    @classmethod
    def from_dict(cls, dict_data:dict)->"ActionFlowStep":
        return cls(
            id=dict_data["id"],
            type=FlowStepType.ACTION,
            action=dict_data["action"],
            args=dict_data["args"]

        )

@dataclass(slots=True)
class EndFlowStep(FlowStep):
    @classmethod
    def from_dict(cls, dict_data: dict) -> "EndFlowStep":
        return cls(
            id=dict_data["id"],
            type=FlowStepType.START,
            next=[]
        )

@dataclass(slots=True)
class ResponseDefinition:
    mode:str = "static"
    text:str | None = None
    prompt:str | None = None

@dataclass(slots=True)
class SlotValidation:
    condition:str
    failure_response:ResponseDefinition | None = None

@dataclass(slots=True)
class CollectFlowStep(FlowStep):
    slot_name:str
    response:ResponseDefinition
    validation:SlotValidation | None = None

    @classmethod
    def from_dict(cls, dict_data:dict)->"CollectFlowStep":
        return cls(
            id=dict_data["id"],
            type=FlowStepType.COLLECT,
            next=_build_next_links(dict_data["next"]),
            slot_name=dict_data["slot_name"],
            response=ResponseDefinition(**dict_data.get("response",{})),
            validation=SlotValidation(
                condition=dict_data.get("validation",{}).get("condition",""),
                failure_response=ResponseDefinition(**dict_data.get("validation",{}).get("failure_response",{}))
            ) if dict_data.get("validation") else None,
        )

#=======================================
# flow
#=======================================
@dataclass(slots=True)
class FlowSlot:
    name:str
    type:str
    label:str
    description:str

@dataclass(slots=True)
class Flow:
    id:str
    name:str
    description:str
    steps:list[FlowStep] = field(default_factory=list)
    slots:list[FlowSlot] = field(default_factory=list)

@dataclass(slots=True)
class FlowList:
    slots: dict[Flow, FlowSlot] = field(default_factory=dict)
    flows: list[Flow] = field(default_factory=list)







