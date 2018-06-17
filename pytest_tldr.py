# -*- coding: utf-8 -*-
import platform
import sys
import time

import pluggy
import py
import pytest


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    # Unregister the default terminal reporter.
    config.pluginmanager.unregister(name="terminalreporter")

    reporter = TerseReporter(config, sys.stdout)
    config.pluginmanager.register(reporter, "terminalreporter")

    # Force the traceback style to native.
    config.option.tbstyle = 'native'


def _plugin_nameversions(plugininfo):
    values = []
    for plugin, dist in plugininfo:
        # gets us name and version!
        name = "{dist.project_name}-{dist.version}".format(dist=dist)
        # questionable convenience, but it keeps things short
        if name.startswith("pytest-"):
            name = name[7:]
        # we decided to print python package names
        # they can have more than one plugin
        if name not in values:
            values.append(name)
    return values


class TerseReporter:
    def __init__(self, config, file=None):
        self.config = config
        self.file = file if file is not None else sys.stdout

        self.verbosity = self.config.option.verbose
        self.xdist = self.config.option.numprocesses is not None

        self.stats = {}

        # This is needed for compatibility; some other plugins
        # rely on the fact that there is a terminalreporter
        # plugin that has a _tw attribute.
        import _pytest.config
        self._tw = _pytest.config.create_terminal_writer(config, file)

    def print(self, *args, **kwargs):
        print(*args, **kwargs, file=self.file)

    def pytest_internalerror(self, excrepr):
        for line in str(excrepr).split("\n"):
            self.print("INTERNALERROR> " + line)
        return 1

    def pytest_sessionstart(self, session):
        self._starttime = time.time()
        self._n_tests = 0
        self._started = False

        if self.verbosity:
            verinfo = platform.python_version()
            msg = "platform {} -- Python {}".format(sys.platform, verinfo)
            if hasattr(sys, "pypy_version_info"):
                verinfo = ".".join(map(str, sys.pypy_version_info[:3]))
                msg += "[pypy-{}-{}]".format(verinfo, sys.pypy_version_info[3])
            self.print(msg)
            self.print("pytest=={}".format(pytest.__version__))
            self.print("py=={}".format(py.__version__))
            self.print("pluggy=={}".format(pluggy.__version__))

            headers = self.config.hook.pytest_report_header(
                config=self.config, startdir=py.path.local()
            )
            for header in headers:
                if isinstance(header, str):
                    self.print(header)
                else:
                    for line in header:
                        self.print(line)

    def pytest_report_header(self, config):
        lines = [
            "rootdir: {}".format(config.rootdir),
        ]
        if config.inifile:
            lines.append("inifile: {}".format(config.rootdir.bestrelpath(config.inifile)))

        plugininfo = config.pluginmanager.list_plugin_distinfo()
        if plugininfo:
            lines.append("plugins: {}".format(", ".join(_plugin_nameversions(plugininfo))))

        return lines

    def pytest_runtest_logstart(self, nodeid, location):
        if not self._started:
            if self.verbosity:
                self.print()
                self.print("----------------------------------------------------------------------")
            self._started = True

        # If we're running in distributed mode, we can't
        # print a hanging statement *before* the test,
        # because other processes may return before this
        # one. So; only output a "before" line if we're
        # in singlethreaded mode; or, if we're in
        # hyper-verbose mode (in which case, output with a newline)
        if self.verbosity:
            if self.xdist:
                if self.verbosity >= 2:
                    self.print("{} ... ".format(nodeid))
            else:
                self.print("{} ... ".format(nodeid), end='')

    def pytest_runtest_logreport(self, report):
        if report.when == 'call':
            if self.verbosity and self.xdist:
                self.print("{}: ".format(report.nodeid), end='')

            self._n_tests += 1
            if report.failed:
                if report.longrepr == 'Unexpected success':
                    # pytest raw xfail
                    self.stats.setdefault('u', []).append(report)
                    if self.verbosity:
                        self.print("unexpected success")
                    else:
                        self.print('u', end='', flush=True)
                else:
                    if '\nAssertionError: ' in str(report.longrepr) \
                            or '\nFailed: ' in str(report.longrepr):
                        # pytest assertion
                        # unittest self.assert()
                        self.stats.setdefault('F', []).append(report)
                        if self.verbosity:
                            self.print("FAIL")
                        else:
                            self.print('F', end='', flush=True)
                    elif str(report.longrepr).startswith('[XPASS('):
                        # pytest xfail(strict=True)
                        self.stats.setdefault('u', []).append(report)
                        if self.verbosity:
                            self.print("unexpected success")
                        else:
                            self.print('u', end='', flush=True)
                    else:
                        self.stats.setdefault('E', []).append(report)
                        if self.verbosity:
                            self.print("ERROR")
                        else:
                            self.print('E', end='', flush=True)
            elif report.skipped:
                if isinstance(report.longrepr, tuple):
                    self.stats.setdefault('s', []).append(report)
                    if self.verbosity:
                        self.print(report.longrepr[2])
                    else:
                        self.print('s', end='', flush=True)
                else:
                    self.stats.setdefault('x', []).append(report)
                    if self.verbosity:
                        self.print('expected failure')
                    else:
                        self.print('x', end='', flush=True)
            else:
                self.stats.setdefault('.', []).append(report)
                if self.verbosity:
                    self.print("ok")
                else:
                    self.print('.', end='', flush=True)
        else:
            if report.failed:
                self.stats.setdefault('E', []).append(report)
                if self.verbosity:
                    self.print("ERROR")
                else:
                    self.print('E', end='', flush=True)
            elif report.skipped:
                if isinstance(report.longrepr, tuple):
                    self.stats.setdefault('s', []).append(report)
                    if self.verbosity:
                        self.print(report.longrepr[2])
                    else:
                        self.print('s', end='', flush=True)

    def pytest_sessionfinish(self, exitstatus):
        self.print()
        duration = time.time() - self._starttime

        errors = self.stats.get('E', [])
        for report in errors:
            self.print("======================================================================")
            self.print("ERROR: {}".format(report.nodeid))
            self.print("----------------------------------------------------------------------")
            if report.capstdout:
                self.print(report.capstdout)
            self.print(report.longrepr)
            self.print()

        failures = self.stats.get('F', [])
        for report in failures:
            self.print("======================================================================")
            self.print("FAIL: {}".format(report.nodeid))
            self.print("----------------------------------------------------------------------")
            if report.capstdout:
                self.print(report.capstdout)
            self.print(report.longrepr)
            self.print()

        if self.verbosity >= 2:
            for report in self.stats.get('.', []):
                if report.capstdout:
                    self.print("======================================================================")
                    self.print("Pass: {}".format(report.nodeid))
                    self.print("----------------------------------------------------------------------")
                    self.print(report.capstdout)
                    self.print()

        upasses = self.stats.get('u', [])
        for report in upasses:
            self.print("======================================================================")
            self.print("UNEXPECTED SUCCESS: {}".format(report.nodeid))
            self.print()

        self.print("----------------------------------------------------------------------")
        self.print("Ran {n_tests} tests in {duration:.2f}s".format(
                n_tests=self._n_tests,
                duration=duration,
            ))
        self.print()



        problems = []


        xfails = self.stats.get('x', [])
        skips = self.stats.get('s', [])

        if errors:
            problems.append('errors={}'.format(len(errors)))
        if failures:
            problems.append('failures={}'.format(len(failures)))
        if skips:
            problems.append('skipped={}'.format(len(skips)))
        if xfails:
            problems.append('expected failures={}'.format(len(xfails)))
        if upasses:
            problems.append('unexpected successes={}'.format(len(xfails)))

        if failures or errors or upasses:
            self.print("FAILED (" + ", ".join(problems) + ")")
        elif skips or xfails:
            self.print("OK (" + ", ".join(problems) + ")")
        else:
            self.print("OK")
