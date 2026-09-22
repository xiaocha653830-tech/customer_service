import uuid

from fastapi import APIRouter, Depends

from api.deps import get_dialogue_service
from api.schemas import ChatHistoryResponse, ChatHistoryMessageResponse, ChatRequest, ChatResponse, \
    BotMessageResponse, ChatObjectPayload
from domain.messages import UserMessage
from service.dialogue_service import DialogueService

router = APIRouter()


@router.get("/api/chat/history")
async def chat_history(sender_id:str):
    # TODO 调用service查询当前用户的历史记录
    return ChatHistoryResponse(
        sender_id=sender_id,
        messages=[
            ChatHistoryMessageResponse(
                role="user",
                text="你好呀",
                object=None
            ),
            ChatHistoryMessageResponse(
                role="bot",
                text="你好，很高兴为你服务。",
                object=None
            )
        ]
    )

@router.post("/api/chat")
async def chat(
        chat_request:ChatRequest,
        dialogue_service:DialogueService = Depends( get_dialogue_service ),
):
    # 1.将交互模型chat_request 转换成 领域模型 UserMessage
    dict_data = {
        "sender_id": chat_request.sender_id,
        "message_id": chat_request.message_id if chat_request.message_id else uuid.uuid4().hex,
        "type": "text" if chat_request.text else "object",
        "text": chat_request.text,
        "object": {
            "type": chat_request.object.type,
            "id": chat_request.object.id,
            "title":chat_request.object.title,
            "attributes":chat_request.object.attributes
        } if chat_request.object else None
    }

    user_message = UserMessage.from_dict(dict_data)

    # 2.调用DialogueService类中的process_message方法进行对话处理
    process_result = dialogue_service.process_message(user_message)

    # 3.将领域模型 process_result 转换成交互模型 ChatResponse
    messages=[]
    for message in process_result.message:
        message_response = BotMessageResponse(
            text=message.text,
            object=ChatObjectPayload(
                type=message.object.type,
                id=message.object.id,
                title=message.object.title,
                attributes=message.object.attributes
            ) if message.object is not None else None
        )
        messages.append(message_response)

    chat_response = ChatResponse(
        sender_id=process_result.sender_id,
        message_id=process_result.message_id,
        messages=messages,
    )

    # 4.返回交互模型 ChatResponse
    return chat_response