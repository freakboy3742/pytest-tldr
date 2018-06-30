
def test_pass(testdir):
    testdir.makepyfile("""
        def test_pass():
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_pass.py::test_pass ... ok'
    ])

    assert result.ret == 0


def test_fail(testdir):
    testdir.makepyfile("""
        def test_fail():
            assert str(True) == 'Garble'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_fail.py::test_fail ... FAIL',
        'FAIL: test_fail.py::test_fail'
    ])

    assert result.ret == 1


def test_error(testdir):
    testdir.makepyfile("""
        def test_error():
            raise Exception("This shouldn't happen")
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_error.py::test_error ... ERROR',
        'ERROR: test_error.py::test_error'
    ])

    assert result.ret == 1


def test_skip(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.skip(reason="this should be skipped")
        def test_skip():
            assert str(True) == 'Garble'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_skip.py::test_skip ... Skipped: this should be skipped',
    ])

    assert result.ret == 0


def test_xfail(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.xfail
        def test_expected_failure():
            assert str(True) == 'Garble'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_xfail.py::test_expected_failure ... expected failure',
    ])

    assert result.ret == 0


def test_upass(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.xfail
        def test_unexpected_success():
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_upass.py::test_unexpected_success ... ok',
    ])

    assert result.ret == 0


def test_upass_strict(testdir):
    testdir.makepyfile("""
        import pytest

        @pytest.mark.xfail(strict=True)
        def test_unexpected_success():
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_upass_strict.py::test_unexpected_success ... unexpected success',
    ])

    assert result.ret == 1
