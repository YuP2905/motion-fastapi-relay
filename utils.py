from __future__ import annotations
from typing import (
    Generator,
)
from requests import (
    Response as ClientResponse
)
def motion_stream_iterator(
    upstream: ClientResponse,
    chunk_size: int
) -> Generator[bytes, None, None]:
    try:
        for chunk in upstream.iter_content(
            chunk_size=chunk_size
        ):
            if chunk:
                yield chunk
    finally:
        upstream.close()