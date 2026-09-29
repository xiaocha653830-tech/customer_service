from typing import Dict, Any

from jinja2 import Template
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate

from domain.messages import BotMessage
from domain.state import DialogueState
from infrastructure.ai_clients import llm_client
from prompt.history_builder import build_history
from task.action.base import Action, ActionResult


class ActionResponse(Action):
    name = "action_response"

    async def run(self,state:DialogueState,args:Dict[str,Any])->ActionResult:
        mode = args.get("mode","static")
        if mode == "static":
            #静态模式
            # mode: static
            # text:"订单{{ slots.order_number }}当前状态是{{ slots.order_status }}我会继续帮你跟进。"
            text = args.get("text","")
            data = {
                "slots":state.active_task.slots if state.active_task else {},
                "context":state.active_system_task.to_dict() if state.active_task else {},
            }
            rendered_text = Template(text).render(data)
            return ActionResult(
                messages=[BotMessage(text=rendered_text)],
            )
        elif mode == "rephrase":
            #改写模式
            #1.获取text并渲染
            text = args.get("text", "")
            data = {
                "slots": state.active_task.slots if state.active_task else {},
                "context": state.active_system_task.to_dict() if state.active_task else {},
            }
            rendered_text = Template(text).render(data)
            #2.llm对渲染后的回复进行改写
            prompt_text = args.get("prompt", "")
            prompt_inputs = {
                "history" : build_history(state.get_current_session().turns),
                "user_message" : state.pending_turn.input_message.text,
                "current_response" : rendered_text
            }
            #调用llm构建提示词
            prompt = PromptTemplate.from_template(
                prompt_text,
                template_format="jinja2",
            )
            chain = prompt | llm_client | StrOutputParser()
            rephrased_text = chain.invoke(prompt_inputs)
            return ActionResult(
                messages=[BotMessage(text=rephrased_text)],
            )

        else:
            #生成模式
            prompt_text = args.get("prompt", "")
            prompt_inputs = {
                "history": build_history(state.get_current_session().turns),
                "user_message": state.pending_turn.input_message.text,
            }
            # 调用llm构建提示词
            prompt = PromptTemplate.from_template(
                prompt_text,
                template_format="jinja2",
            )
            chain = prompt | llm_client | StrOutputParser()
            generated_text = chain.invoke(prompt_inputs)
            return ActionResult(
                messages=[BotMessage(text=generated_text)],
            )













