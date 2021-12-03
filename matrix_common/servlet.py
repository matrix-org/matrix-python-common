# Copyright 2021 The Matrix.org Foundation C.I.C.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import functools
import json
import logging
from typing import Any, Callable

from twisted.internet import defer
from twisted.python import failure
from twisted.web import server
from twisted.web.server import Request

from matrix_common.json import JsonDict

logger = logging.getLogger(__name__)


class MatrixRestError(Exception):
    """
    Handled by the jsonwrap wrapper. Any servlets that don't use this
    wrapper should catch this exception themselves.
    """

    def __init__(self, httpStatus: int, errcode: str, error: str):
        super(Exception, self).__init__(error)
        self.httpStatus = httpStatus
        self.errcode = errcode
        self.error = error


def json_servlet_sync(f: Callable[..., JsonDict]) -> Callable[..., bytes]:
    @functools.wraps(f)
    def inner(self: Any, request: Request, *args: Any, **kwargs: Any) -> bytes:
        """
        Runs a web handler function with the given request and parameters, then
        converts its result into JSON and returns it. If an error happens, also sets
        the HTTP response code.

        Args:
            self: The current object.
            request: The request to process.
            args: The arguments to pass to the function.
            kwargs: The keyword arguments to pass to the function.

        Returns:
            The JSON payload to send as a response to the request.
        """
        try:
            request.setHeader("Content-Type", "application/json")
            return dict_to_json_bytes(f(self, request, *args, **kwargs))
        except MatrixRestError as e:
            request.setResponseCode(e.httpStatus)
            return dict_to_json_bytes({"errcode": e.errcode, "error": e.error})
        except Exception:
            logger.exception("Exception processing request")
            request.setHeader("Content-Type", "application/json")
            request.setResponseCode(500)
            return dict_to_json_bytes(
                {
                    "errcode": "M_UNKNOWN",
                    "error": "Internal Server Error",
                }
            )

    return inner


def json_servlet_async(fn: Callable[..., JsonDict]) -> Callable[..., int]:
    async def render(
        fn: Callable[..., Any], self: Any, request: Request, **kwargs: Any
    ) -> None:
        """
        Runs an asynchronous web handler function with the given request and parameters,
        then converts its result into JSON bytes and writes it to the request. If an error
        happens, also sets the HTTP response code.

        Args:
            fn: The handler to run.
            self: The current object.
            request: The request to process.
            args: The arguments to pass to the function.
            kwargs: The keyword arguments to pass to the function.
        """

        request.setHeader("Content-Type", "application/json")
        try:
            result = await fn(self, request, **kwargs)
            request.write(dict_to_json_bytes(result))
        except MatrixRestError as e:
            request.setResponseCode(e.httpStatus)
            request.write(dict_to_json_bytes({"errcode": e.errcode, "error": e.error}))
        except Exception:
            f = failure.Failure()
            logger.error("Request processing failed: %r, %s", f, f.getTraceback())
            request.setResponseCode(500)
            request.write(
                dict_to_json_bytes(
                    {"errcode": "M_UNKNOWN", "error": "Internal Server Error"}
                )
            )
        request.finish()

    @functools.wraps(fn)
    def inner(*args: Any, **kwargs: Any) -> int:
        """
        Runs an asynchronous web handler function with the given arguments.

        Args:
            args: The arguments to pass to the function.
            kwargs: The keyword arguments to pass to the function.

        Returns:
            A special code to tell the servlet that the response isn't ready yet
            and will come later.
        """
        defer.ensureDeferred(render(fn, *args, **kwargs))
        return server.NOT_DONE_YET

    return inner


def send_cors(request: Request) -> None:
    """Send CORS headers when handling a request."""
    request.setHeader("Access-Control-Allow-Origin", "*")
    request.setHeader("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    request.setHeader("Access-Control-Allow-Headers", "*")


def dict_to_json_bytes(content: JsonDict) -> bytes:
    """
    Converts a dict into JSON and encodes it to bytes.

    Args:
        content: The dict to convert.

    Returns:
        The JSON bytes.
    """
    return json.dumps(content).encode("UTF-8")
