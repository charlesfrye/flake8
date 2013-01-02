from __future__ import with_statement
import re
import os

pep8style = None


def skip_warning(warning, ignore=[]):
    # XXX quick dirty hack, just need to keep the line in the warning
    if not hasattr(warning, 'message'):
        # McCabe's warnings cannot be skipped afaik, and they're all strings.
        return False
    if warning.message.split()[0] in ignore:
        return True
    if not os.path.isfile(warning.filename):
        return False

    # XXX should cache the file in memory
    with open(warning.filename) as f:
        line = f.readlines()[warning.lineno - 1]

    return skip_line(line)


def skip_line(line):
    return line.strip().lower().endswith('# noqa')


_NOQA = re.compile(r'flake8[:=]\s*noqa', re.I | re.M)


def skip_file(path):
    """Returns True if this header is found in path

    # flake8: noqa
    """
    if not os.path.isfile(path):
        return False
    f = open(path)
    try:
        content = f.read()
    finally:
        f.close()
    return _NOQA.search(content) is not None


def _initpep8():
    # default pep8 setup
    global pep8style
    import pep8
    if pep8style is None:
        pep8style = pep8.StyleGuide(config_file=True)
    pep8style.options.physical_checks = pep8.find_checks('physical_line')
    pep8style.options.logical_checks = pep8.find_checks('logical_line')
    pep8style.options.counters = dict.fromkeys(pep8.BENCHMARK_KEYS, 0)
    pep8style.options.messages = {}
    pep8style.options.max_line_length = 79
    pep8style.args = []
    return pep8style
