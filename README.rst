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

.. image:: https://beekeeper.herokuapp.com/projects/pybee/pytest-tldr/shield
    :target: https://beekeeper.herokuapp.com/projects/pybee/pytest-tldr
    :alt: Build status


A `pytest`_ plugin that limits the output of pytest to just the things you
need to see.

One of my biggest personally complaints about pytest is that its console
output is very, very chatty. It tells you it's starting. It tells you it's
working. It tells you it's done. And if a test fails, it doesn't just
tell you which test failed. It dumps pages and pages of code onto
your console.

And it does all this in full technicolor glory. Better hope you have perfect
color vision, and your console color choices are contrast compatible.

Yes, pytest has many, many command line options. And some of these behaviors
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


.. _`Cookiecutter`: https://github.com/audreyr/cookiecutter
.. _`BSD-3`: http://opensource.org/licenses/BSD-3-Clause
.. _`pytest`: https://github.com/pytest-dev/pytest
.. _`pip`: https://pypi.org/project/pip/
.. _`PyPI`: https://pypi.org/project
