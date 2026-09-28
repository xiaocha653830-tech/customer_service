from typing import List

from atguigu.domain.messages import BotMessage


class ActionResponse:

    name:str = "action_response"

    def run(self,args:dict)->List[BotMessage]:
        # 生成一条回复消息
        # 三种生成回复消息的方式：
        # ① static 静态模式 : 直接将 text参数，包装成BotMessage对象并返回
        # ② rephrase 改写模式 ： 调用LLM对text进行改写，改写之后包装成BotMessage对象并返回
        # ③ generate 生成模式 ： 调用LLM生成回复消息,并返回
        pass