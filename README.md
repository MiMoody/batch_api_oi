# BATCH_TEXT_IO

**Этот пакет предназначен для работы с Batch API OpenAI**

### Пример использования

```python
import sys
import logging


from openai import OpenAI
from openai.resources.batches import Batch
from batch_text_oi import get_all_batches_gen, get_info_by_output_file_id, create_batch
from batch_text_oi.models.request_model import Message, BodyMessage


client = OpenAI(api_key="api_key")

logging.basicConfig(
    level=logging.DEBUG, handlers=[logging.StreamHandler(stream=sys.stdout)]
)

message = Message(
    model="gpt-4o",
    messages=[
        BodyMessage(
            role="system",
            content="Ты — великий программист с огромным опытом.",
        ),
        BodyMessage(
            role="user",
            content="Расскажи что такое язык программирования.",
        ),
    ],
    max_tokens=70,
)

batch: Batch = create_batch(client=client, messages=[message])
for batches in get_all_batches_gen(client=client, limit=100):
    for batch in batches:
        if batch.status == "completed":
            logging.info(f"Batch {batch.id} is completed.")
            batch_response = get_info_by_output_file_id(
                client=client, output_file_id=batch.output_file_id
            )
            logging.info(batch_response)
        else:
            logging.debug(
                "Batch with id %s has status %s and full info -->  %s",
                batch.id,
                batch.status,
                batch,
            )

```
