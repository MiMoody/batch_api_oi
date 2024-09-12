import io
import logging
import logging.config
from typing import Any, Generator
import uuid
from contextlib import contextmanager


from openai import OpenAI
from openai.resources.batches import Batch

from .models.request_model import RequestMessage, Message, MessageWithoutId, BodyMessage
from .models.response_model import BatchResponse


API_URL = "/v1/chat/completions"
COMPLETION_WINDOW = "24h"

batch_oi_logger = logging.getLogger(name="batch_oi_logger")
batch_oi_logger.setLevel(logging.DEBUG)
batch_oi_logger.addHandler(logging.StreamHandler())


@contextmanager
def generate_batch_file(
    messages: list[Message],
) -> Generator[io.BytesIO, Any, None]:
    data: list[RequestMessage] = []
    for message in messages:
        dump_message: dict = message.model_dump()
        custom_id: uuid.UUID = dump_message.pop("id")
        data.append(
            RequestMessage(
                method="POST",
                url=API_URL,
                custom_id=custom_id,
                body=MessageWithoutId(**dump_message),
            )
        )

    jsonl_buffer = io.BytesIO()
    for record in data:
        jsonl_buffer.write((record.model_dump_json() + "\n").encode("utf-8"))
    jsonl_buffer.seek(0)
    yield jsonl_buffer
    jsonl_buffer.close()


def create_batch(
    client: OpenAI, messages: list[Message], metadata: dict = None
) -> Batch:
    with generate_batch_file(messages=messages) as jsonl_buffer:
        batch_input_file = client.files.create(file=jsonl_buffer, purpose="batch")

    batch_input_file_id = batch_input_file.id

    batch: Batch = client.batches.create(
        input_file_id=batch_input_file_id,
        endpoint=API_URL,
        completion_window=COMPLETION_WINDOW,
        metadata=metadata,
    )
    batch_oi_logger.debug("Success create batch with id: %s", batch.input_file_id)
    return batch


def get_all_batches_gen(
    client: OpenAI, limit: int = 100
) -> Generator[list[Batch], Any, None]:
    response: list[Batch] = list(client.batches.list(limit=limit))
    while response:
        yield response
        if len(response) < limit:
            break
        response = list(client.batches.list(limit=limit, after=response[-1].id))


def get_info_by_output_file_id(client: OpenAI, output_file_id: str) -> BatchResponse:
    file_response: dict = client.files.content(output_file_id).json()
    return BatchResponse(**file_response)
