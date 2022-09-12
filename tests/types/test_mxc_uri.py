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
from unittest import TestCase

from matrix_common.types.mxc_uri import MXCUri


class MXCUriTestCase(TestCase):
    def test_valid_mxc_uris_to_str(self) -> None:
        """Tests that a series of valid mxc are converted to a str correctly."""
        # Converting an MXCUri to its str representation
        mxc_0 = MXCUri(server_name="example.com", media_id="84n8493hnfsjkbcu")
        self.assertEqual(str(mxc_0), "mxc://example.com/84n8493hnfsjkbcu")

        mxc_1 = MXCUri(
            server_name="192.168.1.17:8008", media_id="bajkad89h31ausdhoqqasd"
        )
        self.assertEqual(str(mxc_1), "mxc://192.168.1.17:8008/bajkad89h31ausdhoqqasd")

        mxc_2 = MXCUri(server_name="123.123.123.123", media_id="000000000000")
        self.assertEqual(str(mxc_2), "mxc://123.123.123.123/000000000000")

    def test_valid_mxc_uris_from_str(self) -> None:
        """Tests that a series of valid mxc uris strs are parsed correctly."""
        # Converting a str to its MXCUri representation
        mxcuri_0 = MXCUri.from_str("mxc://example.com/g12789g890ajksjk")
        self.assertEqual(mxcuri_0.server_name, "example.com")
        self.assertEqual(mxcuri_0.media_id, "g12789g890ajksjk")

        mxcuri_1 = MXCUri.from_str("mxc://localhost:8448/abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(mxcuri_1.server_name, "localhost:8448")
        self.assertEqual(mxcuri_1.media_id, "abcdefghijklmnopqrstuvwxyz")

        mxcuri_2 = MXCUri.from_str("mxc://[::1]/abcdefghijklmnopqrstuvwxyz")
        self.assertEqual(mxcuri_2.server_name, "[::1]")
        self.assertEqual(mxcuri_2.media_id, "abcdefghijklmnopqrstuvwxyz")

        mxcuri_3 = MXCUri.from_str("mxc://123.123.123.123:32112/12893y81283781023")
        self.assertEqual(mxcuri_3.server_name, "123.123.123.123:32112")
        self.assertEqual(mxcuri_3.media_id, "12893y81283781023")

        mxcuri_4 = MXCUri.from_str("mxc://domain/abcdefg")
        self.assertEqual(mxcuri_4.server_name, "domain")
        self.assertEqual(mxcuri_4.media_id, "abcdefg")

    def test_invalid_mxc_uris_from_str(self) -> None:
        """Tests that a series of invalid mxc uris are appropriately rejected."""
        # Converting invalid MXC URI strs to MXCUri representations
        with self.assertRaises(ValueError):
            MXCUri.from_str("http://example.com/abcdef")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc:///example.com/abcdef")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc://example.com//abcdef")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc://example.com/abcdef/")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc://example.com/abc/abcdef")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc://example.com/abc/abcdef")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc:///abcdef")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc://example.com")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc://example.com/")

        with self.assertRaises(ValueError):
            MXCUri.from_str("mxc:///")

        with self.assertRaises(ValueError):
            MXCUri.from_str("example.com/abc")

        with self.assertRaises(ValueError):
            MXCUri.from_str("")

        with self.assertRaises(ValueError):
            MXCUri.from_str(None)  # type: ignore
