from pydantic import BaseModel


class Message(BaseModel):
    role: str
    content: str
    refusal: str | None = None


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: str | None = None
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class Body(BaseModel):
    id: str
    object: str
    created: int
    model: str
    choices: list[Choice]
    usage: Usage
    system_fingerprint: str


class Response(BaseModel):
    status_code: int
    request_id: str
    body: Body


class BatchResponse(BaseModel):
    id: str
    custom_id: str
    response: Response
    error: str | None = None
