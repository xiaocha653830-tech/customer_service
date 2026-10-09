from knowledge.provider import KnowledgeProvider, ProductAPIProvider, OrderAPIProvider


class KnowledgeProviderRegistry:

    def __init__(self,providers:list[KnowledgeProvider]):
        self._providers = { p.provider_id:p for p in providers }

    def get(self,provider_id:str) -> KnowledgeProvider:
        return self._providers[provider_id]


if __name__ == '__main__':
    registry = KnowledgeProviderRegistry([
        ProductAPIProvider(),
        OrderAPIProvider()
    ])