import json
import uuid
from typing import List

from fastapi import APIRouter, Depends
from starlette.websockets import WebSocket

from api.deps import get_dialogue_service, get_history_service
from api.schemas import ChatHistoryResponse, ChatHistoryMessageResponse, ChatRequest, ChatResponse, \
    BotMessageResponse, ChatObjectPayload
from conf.config import settings
from domain.messages import UserMessage, ProcessResult, MessageType, MessageObject, BotMessage
from service.dialogue_service import DialogueService
from service.history_service import HistoryService

router = APIRouter()


@router.get("/api/chat/history",response_model=ChatHistoryResponse)
async def chat_history(
        sender_id:str,
        history_service:HistoryService = Depends( get_history_service )
):
    messages = await history_service.list_history(sender_id)
    return ChatHistoryResponse(
        sender_id=sender_id,
        messages=messages,
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
    process_result:ProcessResult = await dialogue_service.process_message(user_message)

    # 3.将领域模型 process_result 转换成交互模型 ChatResponse
    messages=[]
    for message in process_result.messages:
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

@router.websocket("/ws/chat")
async def websocket_chat(
        websocket: WebSocket,
        dialogue_service:DialogueService = Depends( get_dialogue_service ),
):
    await websocket.accept()
    print("~~~~~~~~~~~~~~~~~~~~~~~客户端已连接")

    while True:
        data = await websocket.receive_text()
        try:
            payload = json.loads(data)
        except json.JSONDecodeError:
            await websocket.send_json({
                "type": "error",
                "data":{
                    "code":"INVALID_JSON",
                    "message":"消息格式错误，请发送正确的json格式数据"
                }
            })
        message_type = payload.get("type")
        if message_type == "cancel":
            continue

        if message_type == "message":
            await websocket.send_json({
                "type": "status",
                "sender_id": payload.get("sender_id"),
                "data":{
                    "status":"thinking"
                }
            })

            user_message = UserMessage(
                sender_id=payload.get("sender_id"),
                message_id=payload.get("message_id") if payload.get("message_id") else str(uuid.uuid4()),
                type=MessageType.TEXT if payload.get("text") else MessageType.OBJECT,
                text=payload.get("text") if payload.get("text") else None,
                object=MessageObject(**payload.get("object")) if payload.get("object") else None
            )

            result = await dialogue_service.process_message(user_message)
            bot_messages:List[BotMessage] = result.messages
            for bot_message in bot_messages:
                await websocket.send_json({
                    "type": "bot_message",
                    "sender_id":user_message.sender_id,
                    "message_id":user_message.message_id,
                    "data":{
                        "text":bot_message.text if bot_message.text else None,
                        "object":bot_message.object.to_dict() if bot_message.object else None
                    }
                })

            await websocket.send_json(
                {
                    "type": "status",
                    "sender_id": payload.get("sender_id"),
                    "data": {
                        "status": "done"
                    }
                }
            )


@router.get("/api/digital-human/credentials")
async def get_digital_human_credentials():
    return {
        "app_id": settings.digital_human_app_id,
        "app_secret": settings.digital_human_app_secret
    }