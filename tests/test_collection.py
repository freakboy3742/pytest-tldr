
def test_global_import_error(testdir):
    testdir.makepyfile("""
        import does_not_exist

        def test_problem():
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'CRITICAL: test_global_import_error.py',
        'Ran 0 tests in *',
    ])

    assert result.ret == 2


def test_local_import_error(testdir):
    testdir.makepyfile("""

        def test_problem():
            import does_not_exist
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'test_local_import_error.py::test_problem ... ERROR',
        'ERROR: test_local_import_error.py::test_problem',
    ])

    assert result.ret == 1


def test_global_syntax_error(testdir):
    testdir.makepyfile("""
        print(  # Deliberately unmatched parentheses

        def test_problem():
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'CRITICAL: test_global_syntax_error.py',
        'Ran 0 tests in *',
    ])

    assert result.ret == 2


def test_local_syntax_error(testdir):
    testdir.makepyfile("""

        def test_problem():
            print(  # Deliberately unmatched parentheses
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v')
    result.stdout.fnmatch_lines([
        'CRITICAL: test_local_syntax_error.py',
        'Ran 0 tests in *',
    ])

    assert result.ret == 2
