import sys


def test_pass(testdir):
    testdir.makepyfile("""
        import unittest


        class TestCase(unittest.TestCase):
            def test_pass(self):
                self.assertTrue(str(True) == 'True')
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::TestCase::test_pass ... ok'
    ])

    assert result.ret == 0


def test_fail(testdir):
    testdir.makepyfile("""
        import unittest


        class TestCase(unittest.TestCase):
            def test_fail(self):
                self.assertTrue(str(True) == 'Garble')
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::TestCase::test_fail ... FAIL',
        'FAIL: test_fail.py::TestCase::test_fail'
    ])

    assert result.ret == 1


def test_error(testdir):
    testdir.makepyfile("""
        import unittest


        class TestCase(unittest.TestCase):
            def test_error(self):
                raise Exception("This shouldn't happen")
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::TestCase::test_error ... ERROR',
        'ERROR: test_error.py::TestCase::test_error'
    ])

    assert result.ret == 1


def test_skip(testdir):
    testdir.makepyfile("""
        import unittest


        class TestCase(unittest.TestCase):
            @unittest.skip('this should be skipped')
            def test_skip(self):
                self.assertTrue(str(True) == 'Garble')
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::TestCase::test_skip ... Skipped: this should be skipped',
    ])

    assert result.ret == 0


def test_xfail(testdir):
    testdir.makepyfile("""
        import unittest


        class TestCase(unittest.TestCase):
            @unittest.expectedFailure
            def test_expected_failure(self):
                self.assertTrue(str(True) == 'Garble')
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::TestCase::test_expected_failure ... expected failure',
    ])

    assert result.ret == 0


def test_upass(testdir):
    testdir.makepyfile("""
        import unittest


        class TestCase(unittest.TestCase):
            @unittest.expectedFailure
            def test_unexpected_success(self):
                self.assertTrue(str(True) == 'True')
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        '*::TestCase::test_unexpected_success ... unexpected success',
    ])

    # pytest under Python2 reports an unexpected pass as a success,
    # but a failure under Python3.
    if sys.version_info.major == 2:
        assert result.ret == 0
    else:
        assert result.ret == 1
