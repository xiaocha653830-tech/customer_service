from atguigu.infrastructure.ai_clients import llm_client

if __name__ == '__main__':
    response = llm_client.invoke("你好")
    print(response.content)