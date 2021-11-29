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

import re
from typing import List, Pattern

_WILDCARD_RUN = re.compile(r"([\?\*]+)")


def glob_to_regex(glob: str, word_boundary: bool = False) -> Pattern[str]:
    """Converts a glob to a compiled regex object.

    Args:
        glob: pattern to match
        word_boundary: If True, the pattern will be allowed to match at word boundaries
           anywhere in the string. Otherwise, the pattern is anchored at the start and
           end of the string.

    Returns:
        compiled regex pattern
    """

    # Patterns with wildcards must be simplified to avoid performance cliffs
    # - The glob `?**?**?` is equivalent to the glob `???*`
    # - The glob `???*` is equivalent to the regex `.{3,}`
    chunks: List[str] = []
    for chunk in _WILDCARD_RUN.split(glob):
        # No wildcards? re.escape()
        if not _WILDCARD_RUN.match(chunk):
            chunks.append(re.escape(chunk))
            continue

        # Wildcards? Simplify.
        qmarks = chunk.count("?")
        if "*" in chunk:
            chunks.append(".{%d,}" % qmarks)
        else:
            chunks.append(".{%d}" % qmarks)

    res = "".join(chunks)

    if word_boundary:
        res = to_word_pattern(res)
    else:
        # \A anchors at start of string, \Z at end of string
        res = r"\A" + res + r"\Z"

    return re.compile(res, re.IGNORECASE)


def to_word_pattern(pattern: str) -> str:
    """Converts the given pattern to one that only matches on whole words.

    Adds word boundary characters to the start and end of a pattern to require that the
    match occur as a whole word.

    If the start or end of the pattern is a non-word character, then a word boundary is
    not required to precede or succeed it.

    A word boundary is considered to be the boundary between a word and non-word
    character. As such, the returned pattern is not appropriate for internationalized
    text search because there are languages which do not use spaces between words.

    Args:
        pattern: The pattern to wrap.

    Returns:
        A new pattern that only matches on whole words. The new pattern may match up to
        one extra non-word character on either side. The exact match is provided by a
        capture group.
    """
    # `^|\W` and `\W|$` handle the case where `pattern` starts or ends with a non-word
    # character.
    return rf"(?:^|\W|\b)({pattern})(?:\b|\W|$)"
