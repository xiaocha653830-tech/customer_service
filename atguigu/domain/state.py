import time
from dataclasses import dataclass, field
from typing import Any

from domain.context import TaskContext, SystemContext
from domain.messages import UserMessage, BotMessage


@dataclass(slots=True)
class FocusedObject:
    type:str
    id:str
    title:str
    attributes:dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, d:dict[str, Any]) -> "FocusedObject":
        return cls(
            type=d["type"],
            id=d["id"],
            title=d["title"],
            attributes=d.get("attributes", {}),
        )


@dataclass(slots=True)
class Turn:
    """对话轮次：一个Turn实例表示一轮对话"""
    turn_id:str
    input_message:UserMessage
    assistant_message:list[BotMessage] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d:dict[str, Any]) -> "Turn":
        return cls(
            turn_id=d["turn_id"],
            input_message=UserMessage.from_dict(d["input_message"]),
            assistant_message=[BotMessage.from_dict(t) for t in d.get("assistant_message", [])],
        )

@dataclass(slots=True)
class Session:
    """用户会话：当两条消息之间的时间间隔超过【1小时】时，会话结束"""
    session_id:str
    started_at: float
    last_activity_at:float
    closed_at:float
    turns:list[Turn] = field(default_factory=list)

    @classmethod
    def from_dict(cls, d:dict[str, Any]) -> "Session":
        return cls(
            session_id=d["session_id"],
            started_at=d.get("started_at", time.time()),
            last_activity_at=d.get("last_activity_at", time.time()),
            closed_at=d["closed_at"],
            turns=[Turn.from_dict(t) for t in d.get("turns", [])],
        )

@dataclass(slots=True)
class DialogueState:
    sender_id:str
    active_task: TaskContext | None = None
    paused_tasks: list[TaskContext] = field(default_factory=list)
    active_system_task: SystemContext | None = None
    focused_object: FocusedObject | None = None
    sessions: list[Session] = field(default_factory=list)
    current_session_id: str | None = None
    pending_turn: Turn | None = None

    @classmethod
    def from_dict(cls, d:dict[str, Any]) -> "DialogueState":
        state = cls(sender_id=d["sender_id"])

        raw_task = d.get("active_task")
        sys_task = d.get("active_system_task")

        state.active_task = TaskContext.from_dict(raw_task) if raw_task is not None else None
        state.paused_tasks = [TaskContext.from_dict(t) for t in d.get("paused_tasks", [])]
        state.active_system_task = SystemContext.from_dict(sys_task) if sys_task is not None else None

        raw_fo = d.get("focused_object")
        state.focused_object = FocusedObject.from_dict(raw_fo) if raw_fo is not None else None

        state.sessions = [Session.from_dict(t) for t in d.get("sessions", [])]
        state.current_session_id = d.get("current_session_id")
        # state.pending_turn = Turn.from_dict(d.get("pending_turn"))

        return state

    @classmethod
    def to_dict(self)-> dict[str, Any]:
        return {
            "sender_id": self.sender_id,
            "active_task": self.active_task.to_dict() if self.active_task is not None else None,
            "paused_tasks": [t.to_dict() for t in self.paused_tasks],
            "active_system_task": self.active_system_task.to_dict() if self.active_system_task is not None else None,
        }












