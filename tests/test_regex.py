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
from unittest import TestCase

from matrix_common.regex import glob_to_regex


class GlobToRegexTestCase(TestCase):
    def test_literal_match(self) -> None:
        """Tests matching against a literal."""
        pattern = glob_to_regex("foobaz")
        self.assertRegex(
            "FoobaZ", pattern, "patterns should match and be case-insensitive"
        )
        self.assertNotRegex(
            "x foobaz", pattern, "pattern should not match at word boundaries"
        )

    def test_wildcard_match(self) -> None:
        """Tests matching with wildcards."""
        pattern = glob_to_regex("f?o*baz")

        self.assertRegex(
            "FoobarbaZ",
            pattern,
            "* should match string and pattern should be case-insensitive",
        )
        self.assertRegex("foobaz", pattern, "* should match 0 characters")
        self.assertNotRegex("fooxaz", pattern, "the character after * must match")
        self.assertNotRegex("fobbaz", pattern, "? should not match 0 characters")
        self.assertNotRegex("fiiobaz", pattern, "? should not match 2 characters")

    def test_multi_wildcard(self) -> None:
        """Tests matching with multiple wildcards in a row."""
        pattern = glob_to_regex("**baz")
        self.assertRegex("agsgsbaz", pattern, "** should match any string")
        self.assertRegex("baz", pattern, "** should match the empty string")
        self.assertEqual(pattern.pattern, r"\A(.{0,}baz)\Z")

        pattern = glob_to_regex("*?baz")
        self.assertRegex("agsgsbaz", pattern, "*? should match any string")
        self.assertRegex("abaz", pattern, "*? should match a single char")
        self.assertNotRegex("baz", pattern, "*? should not match the empty string")
        self.assertEqual(pattern.pattern, r"\A(.{1,}baz)\Z")

        pattern = glob_to_regex("a?*?*?baz")
        self.assertRegex("a g baz", pattern, "?*?*? should match 3 chars")
        self.assertNotRegex("a..baz", pattern, "?*?*? should not match 2 chars")
        self.assertRegex("a.gg.baz", pattern, "?*?*? should match 4 chars")
        self.assertEqual(pattern.pattern, r"\A(a.{3,}baz)\Z")