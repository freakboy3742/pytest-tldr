# Release notes

.. towncrier release notes start

## 0.2.6 (2025-11-11)

### Features

* Support for Pytest 8 was added (#38)[https://github.com/beeware/briefcase/issues/38]
* Project metadata was updated to use PEP 621 format. (#38)[https://github.com/beeware/briefcase/issues/38]
* Support for Python 3.13 was added (#38)[https://github.com/beeware/briefcase/issues/38]
* Support for Python 3.12 was added. (#38)[https://github.com/beeware/briefcase/issues/38]
* Support for Python 3.14 was added. (#39)[https://github.com/beeware/briefcase/issues/39]
* Support for Python 3.15 was added. (#39)[https://github.com/beeware/briefcase/issues/39]
* Support for Pytest 9 was added (#39)[https://github.com/beeware/briefcase/issues/39]

### Backward Incompatible Changes

* Support for Python 3.7 was dropped. (#38)[https://github.com/beeware/briefcase/issues/38]
* Support for Python 3.8 was dropped. (#38)[https://github.com/beeware/briefcase/issues/38]
* Support for Python 3.9 was dropped. (#39)[https://github.com/beeware/briefcase/issues/39]
* Support for Pytest < 7 was dropped. (#39)[https://github.com/beeware/briefcase/issues/39]

## 0.2.5 (2022-10-26)

### Bugfixes

* An incompatibility with Pytest 7.2 was corrected. (#36)

### Misc

* #37

## 0.2.4 (2021-03-12)

### Bugfixes

* Restored compatibility with pytest < 6. (#32)[https://github.com/freakboy3742/pytest-tldr/issues/32]


## 0.2.3 (2021-03-10)

### Bugfixes

* Corrected output stream flush handling. This prevented long-running test results from being displayed until the end of the test suite. (#28)[https://github.com/freakboy3742/pytest-tldr/issues/28]


## 0.2.2 (2020-08-08)

### Bugfixes

* Added Pytest 6 support. (#26)

## 0.2.1 (2019-08-18)

### Bugfixes

* Added a flag to identify TerminalReporter.

## 0.2.0 (2019-07-03)

### Bugfixes

* Added Pytest 5 compatibility

## 0.1.5

* Restored compatibility with more pytest plugins that have output (e.g., pytest-json) (#9)

## 0.1.4

* Restored compatibility with pytest plugins that produce summary output (e.g., coverage reports from pytest-cov). (#6)
* Increased the verbosity needed to see stdout for passed tests.
* Included stdout for Unexpected Success results.

## 0.1.3

* Improved reporting when the test suite contains an error and cannot be imported. (#5)

## 0.1.2

* Fixed support for Python 2.7 (#4)
* Ensure tldr works when xdist isn't installed (#2)

## 0.1.1

* Ensure tldr doesn't overwrite the [Cricket](http://github.com/beeware/cricket) terminal reporter.

## 0.1.0

Initial release.
