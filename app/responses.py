import asyncio
import gzip
from typing import Any, Awaitable, Callable

import orjson
import trio_asyncio
from blacksheep import Content, Request, Response
from blacksheep.server.gzip import GzipMiddleware as BSGzipMiddleware
from blacksheep.server.normalization import ensure_response


class GzipMiddleware(BSGzipMiddleware):
    """Trio-enabled gzip middleware."""

    async def __call__(
        self, request: Request, handler: Callable[[Request], Awaitable[Response]]
    ) -> Response:
        response = ensure_response(await handler(request))

        if response is None or response.content is None:
            return response

        if not self.should_handle(request, response):
            return response

        loop = asyncio.get_running_loop()
        compressed_body = await trio_asyncio.aio_as_trio(loop.run_in_executor)(
            self._executor,
            gzip.compress,
            response.content.body,
            self.comp_level,
        )

        response.with_content(
            Content(
                content_type=response.content.type,
                data=compressed_body,
            )
        )
        response.add_header(b"content-encoding", b"gzip")
        return response


def json(data: Any, status: int = 200) -> Response:
    """
    Returns a Response with given status and content (data) serialized with orjson
    dumps. Serialized JSON objects are sorted for determinism, integers are restricted
    to 53 bits, and datetimes use Zulu time while omitting microseconds.
    """
    return Response(
        status,
        None,
        Content(
            b"application/json",
            orjson.dumps(
                data,
                option=orjson.OPT_UTC_Z
                | orjson.OPT_OMIT_MICROSECONDS
                | orjson.OPT_STRICT_INTEGER
                | orjson.OPT_SORT_KEYS,
            ),
        ),
    )
