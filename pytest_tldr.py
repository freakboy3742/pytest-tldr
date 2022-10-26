import platform
import sys
import time

import pluggy
import py
import pytest

try:
    from pytest import ExitCode
except ImportError:
    # PyTest <5 compatibibility
    from _pytest.main import EXIT_OK, EXIT_TESTSFAILED

    class ExitCode:
        OK = EXIT_OK
        TESTS_FAILED = EXIT_TESTSFAILED


__version__ = "0.2.5"


@pytest.hookimpl(trylast=True)
def pytest_configure(config):
    if getattr(config.option, "cricket_mode", "off") == "off":
        # Unregister the default terminal reporter.
        config.pluginmanager.unregister(name="terminalreporter")

        reporter = TLDRReporter(config, sys.stdout)
        config.pluginmanager.register(reporter, "terminalreporter")

        # Force the traceback style to native.
        config.option.tbstyle = "native"


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


class TLDRReporter:
    def __init__(self, config, file=None):
        self.config = config
        self.file = file if file is not None else sys.stdout

        self.verbosity = self.config.option.verbose
        self.xdist = getattr(self.config.option, "numprocesses", None) is not None
        self.hasmarkup = False

        self.stats = {}

        # These are needed for compatibility; some plugins
        # rely on the fact that there is a terminalreporter
        # that has specific attributes.
        import _pytest.config

        self._tw = _pytest.config.create_terminal_writer(config, file)
        self.reportchars = None

    ######################################################################
    # Plugin compatibility methods.
    #
    # TLDR overwrites TerminalReporter, but some plugins depend
    # on the outout capabilities of TerminalReporter. Preserve them,
    # to the extent possible.
    ######################################################################

    def write(self, content, **markup):
        self._tw.write(content)

    def write_sep(self, sep, title=None, **markup):
        self.ensure_newline()
        self._tw.sep(sep, title, **markup)

    def ensure_newline(self):
        self._tw.line()

    def write_line(self, line, **markup):
        if not isinstance(line, str):
            line = str(line, errors="replace")
        self.ensure_newline()
        self._tw.line(line, **markup)

    def rewrite(self, line, **markup):
        erase = markup.pop("erase", False)
        if erase:
            fill_count = self._tw.fullwidth - len(line) - 1
            fill = " " * fill_count
        else:
            fill = ""
        line = str(line)
        self._tw.write("\r" + line + fill, **markup)

    def section(self, title, sep="=", **kw):
        self._tw.sep(sep, title, **kw)

    def line(self, msg, **kw):
        self._tw.line(msg, **kw)

    ######################################################################

    def print(self, text="", **kwargs):
        end = kwargs.pop("end", "\n")

        self._tw.write(text)
        self._tw.write(end)
        try:
            if kwargs.pop("flush", False):
                self._tw.flush()
        except AttributeError:
            # pytest 6 introduced a separate flush argument to
            # TerminalWriter.write(), and a standalone TerminalWriter.flush()
            # method. This argument/method didn't exist on pytest 5 and lower;
            # the flush was made implicitly on every write.
            pass

    def pytest_internalerror(self, excrepr):
        for line in str(excrepr).split("\n"):
            self.write_line("INTERNALERROR> " + line)
        return 1

    def pytest_collectreport(self, report):
        if report.failed:
            self.print("=" * 78)
            self.print(f"CRITICAL: {report.nodeid}")
            self.print("-" * 78)
            self.print(report.longreprtext)

    def pytest_sessionstart(self, session):
        self._starttime = time.time()
        self._n_tests = 0
        self._started = False

        if self.verbosity:
            verinfo = platform.python_version()
            msg = f"platform {sys.platform} -- Python {verinfo}"
            if hasattr(sys, "pypy_version_info"):
                verinfo = ".".join(map(str, sys.pypy_version_info[:3]))
                msg += f"[pypy-{verinfo}-{sys.pypy_version_info[3]}]"
            self.print(msg)
            self.print(f"pytest=={pytest.__version__}")
            try:
                # Pytest 7.2 vendored `py`; if it's vendored, the version
                # won't exist, but we also don't care that it doesn't exist.
                self.print(f"py=={py.__version__}")
            except AttributeError:
                pass
            self.print(f"pluggy=={pluggy.__version__}")

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
            f"rootdir: {config.rootdir}",
        ]
        if config.inifile:
            lines.append(f"inifile: {config.rootdir.bestrelpath(config.inifile)}")

        plugininfo = config.pluginmanager.list_plugin_distinfo()
        if plugininfo:
            lines.append(
                "plugins: {}".format(", ".join(_plugin_nameversions(plugininfo)))
            )

        return lines

    def pytest_runtest_logstart(self, nodeid, location):
        if not self._started:
            if self.verbosity:
                self.print()
                self.print("-" * 78)
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
                    self.print(f"{nodeid} ... ")
            else:
                self.print(f"{nodeid} ... ", end="", flush=True)

    def report_pass(self, report):
        self.stats.setdefault(".", []).append(report)
        if self.verbosity:
            self.print("ok")
        else:
            self.print(".", end="", flush=True)

    def report_fail(self, report):
        self.stats.setdefault("F", []).append(report)
        if self.verbosity:
            self.print("FAIL")
        else:
            self.print("F", end="", flush=True)

    def report_error(self, report):
        self.stats.setdefault("E", []).append(report)
        if self.verbosity:
            self.print("ERROR")
        else:
            self.print("E", end="", flush=True)

    def report_skip(self, report):
        self.stats.setdefault("s", []).append(report)
        if self.verbosity:
            self.print(report.longrepr[2])
        else:
            self.print("s", end="", flush=True)

    def report_expected_failure(self, report):
        self.stats.setdefault("x", []).append(report)
        if self.verbosity:
            self.print("expected failure")
        else:
            self.print("x", end="", flush=True)

    def report_unexpected_success(self, report):
        self.stats.setdefault("u", []).append(report)
        if self.verbosity:
            self.print("unexpected success")
        else:
            self.print("u", end="", flush=True)

    def pytest_runtest_logreport(self, report):
        if report.when == "call":
            if self.verbosity and self.xdist:
                self.print(f"{report.nodeid}: ", end="")

            self._n_tests += 1
            if report.failed:
                if report.longreprtext == "Unexpected success":
                    # pytest raw xfail
                    # unittest @unexpectedSuccess, Python 3
                    self.report_unexpected_success(report)
                else:
                    if "\nAssertionError: " in str(
                        report.longreprtext
                    ) or "\nFailed: " in str(report.longreprtext):
                        # pytest assertion
                        # unittest self.assert()
                        self.report_fail(report)
                    elif str(report.longreprtext).startswith("[XPASS("):
                        # pytest xfail(strict=True)
                        self.report_unexpected_success(report)
                    else:
                        self.report_error(report)
            elif report.skipped:
                if isinstance(report.longrepr, tuple):
                    self.report_skip(report)
                else:
                    self.report_expected_failure(report)
            else:
                if report.longreprtext == "Unexpected success":
                    # unittest @unexpectedSuccess, Py2.7
                    self.report_unexpected_success(report)
                else:
                    self.report_pass(report)
        else:
            if report.failed:
                self.report_error(report)
            elif report.skipped:
                if isinstance(report.longrepr, tuple):
                    self.report_skip(report)
                else:
                    self.report_expected_failure(report)

    def pytest_sessionfinish(self, exitstatus):
        self.print()
        duration = time.time() - self._starttime

        errors = self.stats.get("E", [])
        for report in errors:
            self.print("=" * 78)
            self.print(f"ERROR: {report.nodeid}")
            self.print("-" * 78)
            if report.capstdout:
                self.print(report.capstdout)
            self.print(report.longreprtext)
            self.print()

        failures = self.stats.get("F", [])
        for report in failures:
            self.print("=" * 78)
            self.print(f"FAIL: {report.nodeid}")
            self.print("-" * 78)
            if report.capstdout:
                self.print(report.capstdout)
            self.print(report.longreprtext)
            self.print()

        if self.verbosity >= 3:
            for report in self.stats.get(".", []):
                if report.capstdout:
                    self.print("=" * 78)
                    self.print(f"Pass: {report.nodeid}")
                    self.print("-" * 78)
                    self.print(report.capstdout)
                    self.print()

        upasses = self.stats.get("u", [])
        for report in upasses:
            self.print("=" * 78)
            self.print(f"UNEXPECTED SUCCESS: {report.nodeid}")
            if report.capstdout:
                self.print(report.capstdout)
            self.print(report.longreprtext)
            self.print()

        self.print("-" * 78)
        self.print(
            "Ran {n_tests} tests in {duration:.2f}s".format(
                n_tests=self._n_tests,
                duration=duration,
            )
        )

        if exitstatus in {ExitCode.OK, ExitCode.TESTS_FAILED}:
            self.config.hook.pytest_terminal_summary(
                config=self.config,
                terminalreporter=self,
                exitstatus=exitstatus,
            )

        xfails = self.stats.get("x", [])
        skips = self.stats.get("s", [])

        problems = []
        if errors:
            problems.append(f"errors={len(errors)}")
        if failures:
            problems.append(f"failures={len(failures)}")
        if skips:
            problems.append(f"skipped={len(skips)}")
        if xfails:
            problems.append(f"expected failures={len(xfails)}")
        if upasses:
            problems.append(f"unexpected successes={len(upasses)}")

        if self._n_tests:
            self.print()
            if failures or errors or upasses:
                self.print("FAILED (" + ", ".join(problems) + ")")
            elif skips or xfails:
                self.print("OK (" + ", ".join(problems) + ")")
            else:
                self.print("OK")
