# Contributing code to matrix-python-common

Everyone is welcome to contribute code to matrix-python-common, provided you are
willing to license your contributions under the same license as the project
itself. In this case, the [Apache Software License v2](LICENSE).

## Set up your development environment

To contribute to matrix-python-common, ensure you have Python 3.7 and `git`
available on your system. You'll need to clone the source code first:

```shell
git clone https://github.com/matrix-org/matrix-python-common.git
```

## Create a virtualenv

To contribute to matrix-python-common, ensure you have Python 3.7 or newer and
then run:

```bash
python3 -m venv .venv
.venv/bin/pip install -e .[dev]
```

This creates an isolated virtual Python environment ("virtualenv") just for
use with matrix-python-common, then installs matrix-python-common along with its
dependencies, and lastly installs a handful of useful tools

Finally, activate the virtualenv by running:

```bash
source .venv/bin/activate
```

Be sure to do this _every time_ you open a new terminal window for working on
matrix-python-common. Activating the venv ensures that any Python commands you
run (`pip`, `python`, etc.) use the versions inside your venv, and not your
system Python.

When you're done, you can close your terminal or run `deactivate` to disable
the virtualenv.

## Run the unit tests

To make sure everything is working as expected, run the unit tests:

```bash
tox -e py
```

If you see a message like:

```
-------------------------------------------------------------------------------
Ran 25 tests in 0.324s

PASSED (successes=25)
```

Then all is well and you're ready to work!

## How to contribute

The preferred and easiest way to contribute changes is to fork the relevant
project on github, and then [create a pull request](
https://help.github.com/articles/using-pull-requests/) to ask us to pull your
changes into our repo.

Some other points to follow:

 * Please base your changes on the `main` branch.

 * Please follow the [code style requirements](
   #code-style-and-continuous-integration).

 * Please [sign off](#sign-off) your contribution.

 * Please keep an eye on the pull request for feedback from the [continuous
   integration system](#code-style-and-continuous-integration) and try to fix
   any errors that come up.

 * If you need to [update your PR](#updating-your-pull-request), just add new
   commits to your branch rather than rebasing.

## Code style and continuous integration

matrix-python-common uses `black`, `isort` and `flake8` to enforce code style.
Use the following script to enforce these style guides:

```shell
scripts-dev/lint.sh
```

(This also runs `mypy`, our preferred typechecker.)

All of these checks are automatically run against any pull request via GitHub
Actions. If your change breaks the build, this
will be shown in GitHub, with links to the build results. If your build fails,
please try to fix the errors and update your branch.

## Sign off

In order to have a concrete record that your contribution is intentional
and you agree to license it under the same terms as the project's license, we've
adopted the same lightweight approach that the Linux Kernel
[submitting patches process](
https://www.kernel.org/doc/html/latest/process/submitting-patches.html#sign-your-work-the-developer-s-certificate-of-origin>),
[Docker](https://github.com/docker/docker/blob/master/CONTRIBUTING.md), and many
other projects use: the DCO (Developer Certificate of Origin:
https://developercertificate.org/). This is a simple declaration that you wrote
the contribution or otherwise have the right to contribute it to Matrix:

```
Developer Certificate of Origin
Version 1.1

Copyright (C) 2004, 2006 The Linux Foundation and its contributors.
660 York Street, Suite 102,
San Francisco, CA 94110 USA

Everyone is permitted to copy and distribute verbatim copies of this
license document, but changing it is not allowed.

Developer's Certificate of Origin 1.1

By making a contribution to this project, I certify that:

(a) The contribution was created in whole or in part by me and I
    have the right to submit it under the open source license
    indicated in the file; or

(b) The contribution is based upon previous work that, to the best
    of my knowledge, is covered under an appropriate open source
    license and I have the right under that license to submit that
    work with modifications, whether created in whole or in part
    by me, under the same open source license (unless I am
    permitted to submit under a different license), as indicated
    in the file; or

(c) The contribution was provided directly to me by some other
    person who certified (a), (b) or (c) and I have not modified
    it.

(d) I understand and agree that this project and the contribution
    are public and that a record of the contribution (including all
    personal information I submit with it, including my sign-off) is
    maintained indefinitely and may be redistributed consistent with
    this project or the open source license(s) involved.
```

If you agree to this for your contribution, then all that's needed is to
include the line in your commit or pull request comment:

```
Signed-off-by: Your Name <your@email.example.org>
```

We accept contributions under a legally identifiable name, such as
your name on government documentation or common-law names (names
claimed by legitimate usage or repute). Unfortunately, we cannot
accept anonymous contributions at this time.

Git allows you to add this signoff automatically when using the `-s`
flag to `git commit`, which uses the name and email set in your
`user.name` and `user.email` git configs.


## Updating your pull request

If you decide to make changes to your pull request - perhaps to address issues
raised in a review, or to fix problems highlighted by [continuous
integration](#continuous-integration-and-testing) - just add new commits to your
branch, and push to GitHub. The pull request will automatically be updated.

Please **avoid** rebasing your branch, especially once the PR has been
reviewed: doing so makes it very difficult for a reviewer to see what has
changed since a previous review.

## Conclusion

That's it! Matrix is a very open and collaborative project as you might expect
given our obsession with open communication. If we're going to successfully
matrix together all the fragmented communication technologies out there we are
reliant on contributions and collaboration from the community to do so. So
please get involved - and we hope you have as much fun hacking on Matrix as we
do!
