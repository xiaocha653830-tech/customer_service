from dataclasses import dataclass, field, asdict
from typing import Dict, Any

from domain.state import DialogueState


@dataclass(slots=True)
class TaskContext:
    flow_id:str
    step_id:str
    slots:Dict[str,Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TaskContext':
        return cls(**data)

    def to_dict(self):
        return {
            "flow_id": self.flow_id,
            "step_id": self.step_id,
            "slots": dict(self.slots),
        }


@dataclass(slots=True)
class SystemContext:
    """
    所有系统任务上下文的父类
    """
    task_id:str
    flow_id:str

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'SystemContext':
        return SYSTEM_CONTEXT[sys_task["flow_id"]].from_dict(sys_task)

    # @classmethod
    # def to_dict(self) -> Dict[str, Any]:
    #     # return SYSTEM_CONTEXT[state.flow_id]

@dataclass(slots=True)
class StartedSystemContext(SystemContext):
    """system_task_started系统任务的上下文"""
    started_flow_name:str
    started_flow_id: str

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'StartedSystemContext':
        return cls(
            task_id=sys_task["task_id"],
            flow_id=sys_task["flow_id"],
            started_flow_name=sys_task["started_flow_name"],
            started_flow_id=sys_task["started_flow_id"],
        )

@dataclass(slots=True)
class ResumedSystemContext(SystemContext):
    """system_task_resumed系统任务的上下文"""
    started_flow_name: str
    started_flow_id: str

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'ResumedSystemContext':
        return cls(
            task_id=sys_task["task_id"],
            flow_id=sys_task["flow_id"],
            started_flow_name=sys_task["started_flow_name"],
            started_flow_id=sys_task["started_flow_id"],
        )

@dataclass(slots=True)
class CannotHandleSystemContext(SystemContext):
    """system_cannot_handle系统任务的上下文"""
    reason: str

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'CannotHandleSystemContext':
        return cls(
            task_id=sys_task["task_id"],
            flow_id=sys_task["flow_id"],
            reason=sys_task["reason"],
        )

@dataclass(slots=True)
class CollectSystemContext(SystemContext):
    """system_collect_information系统任务的上下文"""
    slot_name: str
    response: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'CollectSystemContext':
        return cls(
            task_id=sys_task["task_id"],
            flow_id=sys_task["flow_id"],
            slot_name=sys_task["slot_name"],
            response=sys_task.get("response", {}),
        )

@dataclass(slots=True)
class InterruptedSystemContext(SystemContext):
    """system_task_interrupted系统任务的上下文"""
    interrupted_flow_name: str
    interrupted_flow_id: str
    started_flow_name: str|None = None
    started_flow_id: str|None = None

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'InterruptedSystemContext':
        return cls(
            task_id=sys_task["task_id"],
            flow_id=sys_task["flow_id"],
            interrupted_flow_name=sys_task["interrupted_flow_name"],
            interrupted_flow_id=sys_task["interrupted_flow_id"],
            started_flow_name=sys_task.get("started_flow_name"),
            started_flow_id=sys_task.get("started_flow_id"),
        )

@dataclass(slots=True)
class CancelSystemContext(SystemContext):
    """system_task_canceled系统任务的上下文"""
    canceled_flow_name: str
    canceled_flow_id: str

    @classmethod
    def from_dict(cls, sys_task: Dict) -> 'CancelSystemContext':
        return cls(
            task_id=sys_task["task_id"],
            flow_id=sys_task["flow_id"],
            canceled_flow_name=sys_task["canceled_flow_name"],
            canceled_flow_id=sys_task["canceled_flow_id"],
        )

SYSTEM_CONTEXT = {
    "system_task_started": StartedSystemContext,
    "system_task_resumed": ResumedSystemContext,
    "system_cannot_handle": CannotHandleSystemContext,
    "system_collect_information": CollectSystemContext,
    "system_task_interrupted": InterruptedSystemContext,
    "system_task_canceled": CancelSystemContext,
}



