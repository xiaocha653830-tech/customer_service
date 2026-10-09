from pathlib import Path

import clarify
from atguigu.engine.dialogue_engine import DialogueEngine
from chitchat.handler import ChitchatHandler
from clarify.responder import ClarifyResponder
from knowledge.handler import KnowledgeHandler
from knowledge.intents import KNOWLEDGE_INTENTS
from knowledge.provider import FAQProvider, OrderAPIProvider, ProductAPIProvider, RAGProvider
from knowledge.registry import KnowledgeProviderRegistry
from knowledge.responder import KnowledgeResponder
from plan.planner import TurnPlanner
from plan.validator import TurnPlanValidator
from task.action.builder import build_action_runner
from task.commands.processor import CommandProcessor
from task.flow.executor import FlowExecutor
from task.flow.loader import FlowLoader
from task.handler import TaskHandler


def build_dialogue_engine()->DialogueEngine:
    user_flows_path = Path(__file__).parents[2] / 'flowConfig' / 'user_flows.yml'
    system_flows_path = Path(__file__).parents[2] / 'flowConfig' / 'system_flows.yml'
    load = FlowLoader()
    flows_list = load.load_many([user_flows_path, system_flows_path])
    # 1.创建TaskHandler实例
    task_handler = TaskHandler(
        processor = CommandProcessor(),
        executor= FlowExecutor(
            runner=build_action_runner()
        ),
        flowslist=flows_list,
    )
    # 2. 创建KnowledgeHandler实例
    knowledge_handler = KnowledgeHandler(
        knowledge_intents=KNOWLEDGE_INTENTS,
        provider_registry=KnowledgeProviderRegistry([
            ProductAPIProvider(),
            OrderAPIProvider(),
            FAQProvider(),
            RAGProvider()
            ]),
        knowledge_responder=KnowledgeResponder(),
    )
    # 3.创建ChitchatHandler实例
    chitchat_handler = ChitchatHandler()

    #4.创建TurnPlanner实例
    turn_planner = TurnPlanner()

    #5.创建TurnPlanValidator
    turn_plan_validator = TurnPlanValidator()

    #6.创建ClarifyResponder
    clarify_responder = ClarifyResponder()

    return DialogueEngine(
        task_handler=task_handler,
        knowledge_handler=knowledge_handler,
        chitchat_handler=chitchat_handler,
        turn_planner=turn_planner,
        turn_plan_validator=turn_plan_validator,
        clarify_responder=clarify_responder
    )