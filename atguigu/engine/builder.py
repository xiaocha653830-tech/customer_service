from pathlib import Path

from atguigu.engine.dialogue_engine import DialogueEngine
from task.action.build import build_action_runner
from task.commands.processor import CommandProcessor
from task.flow.executor import FlowExecutor
from task.flow.loader import FlowLoader
from task.handler import TaskHandler


def build_dialogue_engine()->DialogueEngine:
    user_flows_path = Path(__file__).parents[2] / 'flowConfig' / 'user_flows.yml'
    system_flows_path = Path(__file__).parents[2] / 'flowConfig' / 'system_flows.yml'
    load = FlowLoader()
    flows_list = load.load_many([user_flows_path, system_flows_path])

    task_handler = TaskHandler(
        processor = CommandProcessor(),
        executor= FlowExecutor(
            runner=build_action_runner()
        ),
        flowslist=flows_list,
    )

    return DialogueEngine(task_handler=task_handler)