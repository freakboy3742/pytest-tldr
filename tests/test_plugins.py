
def test_coverage(testdir):
    testdir.makepyfile("""
        def test_coverage():
            assert str(True) == 'True'
    """)

    result = testdir.runpytest('-v', '--cov=.')
    result.stdout.fnmatch_lines([
        'test_coverage.py::test_coverage ... ok',
        '---------- coverage: platform *',
        'Name               Stmts   Miss  Cover',
        '--------------------------------------',
        'test_coverage.py       2      0   100%',
    ])

    assert result.ret == 0
