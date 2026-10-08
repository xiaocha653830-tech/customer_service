import json
from dataclasses import asdict

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate

import knowledge
from domain.state import DialogueState
from infrastructure.ai_clients import llm_client
from knowledge.intents import KnowledgeIntent
from plan.models import TurnPlan
from prompt.history_builder import build_history, render_user_message
from prompt.prompt_loader import load_prompt
from task.flow.models import FlowsList


class TurnPlanner:

    async def predict(
            self,
            flowslist:FlowsList,
            knowledge_intents:dict[str,KnowledgeIntent],
            state:DialogueState
    ):
        # 1.加载提示词模板
        prompt_text = load_prompt("turn_plan")
        # 2.构造提示词参数
        flow_info = [{k: v for k, v in asdict(flow).items() if k != "steps"} for flow in flowslist.flows]
        knowledge_intents_info = [ {"id":intent.id,"description":intent.description} for intent in knowledge_intents.values() ]
        prompt_inputs = {
            "available_flows_json": json.dumps({"flows":flow_info},ensure_ascii=False),
            "knowledge_intents_json": json.dumps(knowledge_intents_info,ensure_ascii=False),
            "active_task_json": json.dumps(asdict(state.active_task) if state.active_task else None,ensure_ascii=False),
            "interrupted_tasks_json": json.dumps([asdict(task) for task in state.paused_tasks],ensure_ascii=False),
            "focused_object_json": json.dumps(asdict(state.focused_object) if state.focused_object else None,ensure_ascii=False),
            "current_conversation": build_history(state.get_current_session().turns),
            "user_message":render_user_message(state.pending_turn.input_message)
        }
        # 3.调用llm
        prompt = PromptTemplate.from_template(
            prompt_text,
            template_format="jinja2"
        )
        chain = prompt | llm_client | JsonOutputParser()
        result = await chain.ainvoke(prompt_inputs)
        # 4.将大模型返回的JSON对象，转换成TurnPlan
        return TurnPlan.from_dict(result)