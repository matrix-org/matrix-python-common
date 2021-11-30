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
from unittest import TestCase

from matrix_common.regex import glob_to_regex, to_word_pattern


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

    def test_ignore_case(self) -> None:
        """Tests case sensitivity."""
        pattern = glob_to_regex("foobaz", ignore_case=False)
        self.assertEqual(pattern.flags & re.IGNORECASE, 0)

        pattern = glob_to_regex("foobaz", ignore_case=True)
        self.assertEqual(pattern.flags & re.IGNORECASE, re.IGNORECASE)


class WordPatternTestCase(TestCase):
    def test_whole_word(self) -> None:
        """Tests matching on whole words."""
        pattern = to_word_pattern("foo bar")

        self.assertRegex("foo bar", pattern)
        self.assertRegex(" foo bar ", pattern)
        self.assertRegex("baz foo bar baz", pattern)
        self.assertNotRegex("foo baré", pattern, "é should be seen as part of a word")
        self.assertNotRegex("bar foo", pattern, "Pattern should match words in order")

    def test_ends_with_non_letter(self) -> None:
        """Tests matching on whole words when the pattern ends with a space."""
        pattern = to_word_pattern("foo ")

        self.assertRegex(
            "foo bar",
            pattern,
            "Pattern should be able to end its match on a word boundary",
        )
        self.assertRegex(
            "foo ",
            pattern,
            "Pattern should be able to end its match at the end of a string",
        )
        self.assertRegex(
            "foo  ",
            pattern,
            "Pattern should be able to end its match anywhere",
        )
