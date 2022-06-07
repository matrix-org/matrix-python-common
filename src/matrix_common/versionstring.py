# Copyright 2016 OpenMarket Ltd
# Copyright 2021-2022 The Matrix.org Foundation C.I.C.
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
import logging
import os.path
import subprocess
from typing import Optional

try:
    from importlib.metadata import distribution
except ImportError:
    from importlib_metadata import distribution  # type: ignore

__all__ = ["get_distribution_version_string"]

logger = logging.getLogger(__name__)


@functools.lru_cache()
def get_distribution_version_string(
    distribution_name: str, cwd: Optional[str] = None
) -> str:
    """Calculate a git-aware version string for a distribution package.

    A "distribution package" is a thing that you can e.g. install and manage with pip.
    It can contain modules, an "import package" of multiple modules, and arbitrary
    resource data. See the glossary at

        https://packaging.python.org/en/latest/glossary/#term-Distribution-Package

    for all your taxonomic needs. Often a distribution package contains exactly import
    package---possibly with _different_ names. For example, one can install the
    "matrix-sydent" distribution package from PyPI using pip, and doing so makes the
    "sydent" import package available to import.

    Args:
        distribution_name: The name of the distribution package to check the version of

        cwd: if provided, the directory to run all git commands in. `cwd` may also be
            the path to a file, in which case `os.path.dirname(cwd)` is used instead.
            If omitted, the function will attempt to locate the distribution's source
            on disk and use that location instead---but this fallback is not reliable.

    Raises:
        importlib.metadata.PackageNotFoundError if the given distribution name doesn't
        exist.

    Returns:
        The module version, possibly with git version information included.
    """

    dist = distribution(distribution_name)
    version_string = dist.version
    if cwd is None:
        # This used to work for Synapse, but seems to have broken between versions 1.56
        # and 1.57. I suspect that the cause is a difference in the metadata generated
        # by `setuptools` and `poetry-core` at package-install time.
        cwd = dist.locate_file(".").__fspath__()
    cwd = os.path.dirname(cwd)
    try:

        def _run_git_command(prefix: str, *params: str) -> str:
            try:
                result = (
                    subprocess.check_output(
                        ["git", *params], stderr=subprocess.DEVNULL, cwd=cwd
                    )
                    .strip()
                    .decode("ascii")
                )
                return prefix + result
            except (subprocess.CalledProcessError, FileNotFoundError):
                return ""

        git_branch = _run_git_command("b=", "rev-parse", "--abbrev-ref", "HEAD")
        git_tag = _run_git_command("t=", "describe", "--exact-match")
        git_commit = _run_git_command("", "rev-parse", "--short", "HEAD")

        dirty_string = "-this_is_a_dirty_checkout"
        is_dirty = _run_git_command("", "describe", "--dirty=" + dirty_string).endswith(
            dirty_string
        )
        git_dirty = "dirty" if is_dirty else ""

        if git_branch or git_tag or git_commit or git_dirty:
            git_version = ",".join(
                s for s in (git_branch, git_tag, git_commit, git_dirty) if s
            )

            version_string = f"{version_string} ({git_version})"
    except Exception as e:
        logger.info("Failed to check for git repository: %s", e)

    return version_string
