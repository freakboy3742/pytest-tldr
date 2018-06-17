===========
pytest-tldr
===========

.. image:: https://img.shields.io/pypi/v/pytest-tldr.svg
    :target: https://pypi.org/project/pytest-tldr
    :alt: PyPI version

.. image:: https://img.shields.io/pypi/pyversions/pytest-tldr.svg
    :target: https://pypi.org/project/pytest-tldr
    :alt: Python versions

.. image:: https://img.shields.io/pypi/l/briefcase.svg
    :target: https://github.com/pybee/briefcase/blob/master/LICENSE
    :alt: License

.. image:: https://beekeeper.herokuapp.com/projects/freakboy3742/pytest-tldr/shield
    :target: https://beekeeper.herokuapp.com/projects/freakboy3742/pytest-tldr
    :alt: Build status


A `pytest`_ plugin that limits the output of pytest to just the things you
need to see.

One of my biggest personal complaints about pytest is that its console
output is very, very chatty. It tells you it's starting. It tells you it's
working. It tells you it's done. And if a test fails, it doesn't just
tell you which test failed. It dumps pages and pages of code onto
your console.

And it does all this in Glorious Technicolor. Better hope you have perfect
color vision, and your console color choices are contrast compatible.

Yes: pytest has many, many command line options. And some of these behaviors
can be configured or turned off with feature flags. But there are some people
(presumably, at the very least, the pytest core team) who *like* pytest's
output format. So if you're the odd-one-out on a team who *doesn't* like
pytest's output, you can't commit "better" options into a default
configuration - you have to manually specify your options every time you run
the test suite.

Luckily, pytest also has a plugin system, so we can fix this.

`pytest-tldr` is plugin that gives you minimalist output, in monochrome,
while still giving an indication of test suite progress.

Installation
------------

You can install "pytest-tldr" via `pip`_ from `PyPI`_::

    $ pip install pytest-tldr

Then you can just run your test suite as normal::

    $ pytest tests
    EF..s..........ux
    ======================================================================
    ERROR: tests/test_things.py::TestTests::test_error
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/rkm/projects/sample/tests/test_things.py", line 182, in test_error
        raise Exception("this is really bad")
    Exception: this is really bad

    ======================================================================
    FAIL: tests/test_things.py::TestTests::test_failed
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/rkm/projects/sample/tests/test_things.py", line 179, in test_failed
        self.fail('failed!')
      File "/Users/rkm/.pyenv/versions/3.6.2/lib/python3.6/unittest/case.py", line 670, in fail
        raise self.failureException(msg)
    AssertionError: failed!

    ======================================================================
    UNEXPECTED SUCCESS: tests/test_things.py::TestTests::test_upassed

    ----------------------------------------------------------------------
    Ran 17 tests in 2.11s

    FAILED (errors=1, failures=1, skipped=1, expected failures=1, unexpected successes=1)

Or, if you need a little more detail, use the verbosity option::

    $ pytest tests -v
    platform darwin -- Python 3.6.2
    pytest==3.6.1
    py==1.5.2
    pluggy==0.6.0
    rootdir: /Users/rkm/projects/sample
    plugins: xdist-1.22.0, forked-0.2, tldr-0.1.0
    cachedir: .pytest_cache

    ----------------------------------------------------------------------
    tests/test_things.py::TestTests::test_error ... ERROR
    tests/test_things.py::TestTests::test_failed ... FAIL
    tests/test_things.py::TestTests::test_output ... ok
    tests/test_things.py::TestTests::test_passed ... ok
    tests/test_things.py::TestTests::test_skipped ... Skipped: tra-la-la
    tests/test_things.py::TestTests::test_thing_0 ... ok
    tests/test_things.py::TestTests::test_thing_1 ... ok
    tests/test_things.py::TestTests::test_thing_2 ... ok
    tests/test_things.py::TestTests::test_thing_3 ... ok
    tests/test_things.py::TestTests::test_thing_4 ... ok
    tests/test_things.py::TestTests::test_thing_5 ... ok
    tests/test_things.py::TestTests::test_thing_6 ... ok
    tests/test_things.py::TestTests::test_thing_7 ... ok
    tests/test_things.py::TestTests::test_thing_8 ... ok
    tests/test_things.py::TestTests::test_thing_9 ... ok
    tests/test_things.py::TestTests::test_upassed ... unexpected success
    tests/test_things.py::TestTests::test_xfailed ... expected failure

    ======================================================================
    ERROR: tests/test_things.py::TestTests::test_error
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/rkm/projects/sample/tests/test_things.py", line 182, in test_error
        raise Exception("this is really bad")
    Exception: this is really bad

    ======================================================================
    FAIL: tests/test_things.py::TestTests::test_failed
    ----------------------------------------------------------------------
    Traceback (most recent call last):
      File "/Users/rkm/projects/sample/tests/test_things.py", line 179, in test_failed
        self.fail('failed!')
      File "/Users/rkm/.pyenv/versions/3.6.2/lib/python3.6/unittest/case.py", line 670, in fail
        raise self.failureException(msg)
    AssertionError: failed!

    ======================================================================
    UNEXPECTED SUCCESS: tests/test_things.py::TestTests::test_upassed

    ----------------------------------------------------------------------
    Ran 17 tests in 2.07s

    FAILED (errors=1, failures=1, skipped=1, expected failures=1, unexpected successes=1)



.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
