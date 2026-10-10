from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Command:
    command: str

    @classmethod
    def from_dict(cls, command_dict: dict) -> 'Command':
        command_str = command_dict.get('command')
        if command_str == "start_flow":
            return StartFlowCommand(**command_dict)
        elif command_str == "resume_flow":
            return ResumeFlowCommand(**command_dict)
        elif command_str == "cancel_flow":
            return CancelFlowCommand(**command_dict)
        elif command_str == "set_slots":
            return SetSlotsCommand(**command_dict)



@dataclass(slots=True)
class StartFlowCommand(Command):
    flow: str

@dataclass(slots=True)
class SetSlotsCommand(Command):
    slots: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class CancelFlowCommand(Command):
    pass

@dataclass(slots=True)
class ResumeFlowCommand(Command):
    flow: str