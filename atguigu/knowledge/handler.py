from typing import List

import knowledge
from domain.messages import BotMessage
from domain.state import DialogueState
from knowledge.intents import KnowledgeIntent, KNOWLEDGE_INTENTS
from knowledge.registry import KnowledgeProviderRegistry
from knowledge.responder import KnowledgeResponder


class KnowledgeHandler:

    def __init__(
            self,
            provider_registry:KnowledgeProviderRegistry,
            knowledge_responder:KnowledgeResponder,
            knowledge_intents:dict[str, KnowledgeIntent]
    ):
        self.provider_registry = provider_registry
        self.knowledge_responder = knowledge_responder
        self.knowledge_intents = knowledge_intents


    async def handle(self,intents:List[str], state: DialogueState) -> List[BotMessage]:
        # 1.根据intent_id(refund_policy)查找对应的provider_ids=["rag.default"]
        provider_ids = []
        for intent in intents:
            knowledge_intent: KnowledgeIntent = self.knowledge_intents[intent]
            provider_ids.extend(knowledge_intent.provider_ids)
        # 2.去重
        provider_ids = list(set(provider_ids))
        print(provider_ids)
        # 3.根据provider_ids找到对应的Provider类实例
        knowledge_chunks = []
        for provider_id in provider_ids:
            provider = self.provider_registry.get(provider_id)
            # 4.Provider类实例调用retrieve方法
            chunks = await provider.retrieve(state)
            knowledge_chunks.extend(chunks)
        # 5.调用KnowledgeResponder生成答案
        return await self.knowledge_responder.respond(state, knowledge_chunks)