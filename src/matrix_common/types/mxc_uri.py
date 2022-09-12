# Copyright 2022 The Matrix.org Foundation C.I.C.
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
from typing import Type, TypeVar
from urllib.parse import urlparse

import attr

MU = TypeVar("MU", bound="MXCUri")


@attr.s(frozen=True, slots=True, auto_attribs=True)
class MXCUri:
    """Represents a URI that points to a media resource in matrix.

    MXC URIs take the form 'mxc://server_name/media_id'.
    """

    server_name: str
    media_id: str

    @classmethod
    def from_str(cls: Type[MU], mxc_uri_str: str) -> MU:
        """
        Given a str in the form "mxc://<domain>/<media_id>", return an equivalent MXCUri.

        Args:
            mxc_uri_str: The MXC Uri as a str.

        Returns:
            An MXCUri object with matching attributes.

        Raises:
            ValueError: If the str was not a valid MXC Uri.
        """
        # Attempt to parse the given URI. This will raise a ValueError if the uri is
        # particularly malformed.
        parsed_mxc_uri = urlparse(mxc_uri_str)

        # MXC Uri's are pretty bare bones. The scheme must be "mxc", and we don't allow
        # any fragments, query parameters or other features.
        if (
            # The scheme must be "mxc".
            parsed_mxc_uri.scheme != "mxc"
            # There must be a host and path provided.
            or not parsed_mxc_uri.netloc
            or not parsed_mxc_uri.path
            or not parsed_mxc_uri.path.startswith("/")
            or len(parsed_mxc_uri.path) == 1  # if the path is only '/', aka no Media ID
            # There cannot be any fragments, queries or parameters.
            or parsed_mxc_uri.fragment
            or parsed_mxc_uri.query
            or parsed_mxc_uri.params
        ):
            raise ValueError(
                f"Found invalid structure when parsing MXC Uri: {mxc_uri_str}"
            )

        # We use the parsed 'network location' as the server name
        server_name = parsed_mxc_uri.netloc

        # urlparse adds a '/' to the beginning of the path, so let's remove that and use
        # it as the media_id
        media_id = parsed_mxc_uri.path[1:]

        # The media ID should not contain a '/'
        if "/" in media_id:
            raise ValueError(
                f"Found invalid character in media ID portion of MXC Uri: {mxc_uri_str}"
            )

        return cls(server_name, media_id)

    def __str__(self) -> str:
        """Convert an MXCUri object to a str."""
        return f"mxc://{self.server_name}/{self.media_id}"
