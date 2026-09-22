from pydantic import BaseModel
from typing import Any

class ChatObjectPayload(BaseModel):
    type: str
    id: str
    title: str
    attributes: dict[str,Any] = {}

class ChatHistoryMessageResponse(BaseModel):
    role:str
    text:str|None=None
    object:ChatObjectPayload | None=None

class ChatHistoryResponse(BaseModel):
    sender_id:str
    messages:list[ChatHistoryMessageResponse]

class ChatRequest(BaseModel):
    sender_id:str
    text: str|None=None
    object:ChatObjectPayload | None=None
    message_id:str|None=None

class BotMessageResponse(BaseModel):
    """客服回复消息"""
    text: str|None=None
    object:ChatObjectPayload | None=None

class ChatResponse(BaseModel):
    sender_id:str
    message_id:str
    messages:list[BotMessageResponse]