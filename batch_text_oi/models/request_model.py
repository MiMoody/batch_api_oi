import uuid

from pydantic import BaseModel, Field


class BodyMessage(BaseModel):
    role: str
    content: str


class MessageWithoutId(BaseModel):
    model: str
    messages: list[BodyMessage]
    max_tokens: int | None = None


class Message(MessageWithoutId):
    id: uuid.UUID = Field(default_factory=uuid.uuid4)


class RequestMessage(BaseModel):
    custom_id: uuid.UUID
    method: str
    url: str
    body: MessageWithoutId
