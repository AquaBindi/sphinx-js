from os.path import dirname, join
from shutil import rmtree
from unittest import TestCase

from nose.tools import eq_
from sphinx.cmdline import main as sphinx_main
from sphinx.util.osutil import cd


class AutoFunctionTests(TestCase):
    """Tests for the ``js:autofunction`` directive"""

    @classmethod
    def setup_class(cls):
        cls.docs_dir = join(dirname(__file__), 'source', 'docs')
        with cd(cls.docs_dir):
            sphinx_main(['dummy', '-b', 'text', '-E', '.', '_build'])

    def _file_contents_eq(self, filename, contents):
        with open(join(self.docs_dir, '_build', '%s.txt' % filename)) as file:
            eq_(file.read(), contents)

    def test_autofunction_minimal(self):
        """Make sure we render correctly and pull the params out of the JS code
        when only the function name is provided."""
        self._file_contents_eq(
            'autofunction_minimal',
            'linkDensity(node)' + DESCRIPTION + FIELDS)

    def test_autofunction_explicit(self):
        """Make sure any explicitly provided params override the ones from the
        code, and make sure any explicit arbitrary RST content gets
        preserved."""
        self._file_contents_eq(
            'autofunction_explicit',
            'linkDensity2(snorko, borko[, forko])' + DESCRIPTION + FIELDS + CONTENT)

    def test_autofunction_short(self):
        """Make sure the ``:short-name:`` option works."""
        self._file_contents_eq(
            'autofunction_short',
            'someMethod(hi)\n\n   Here.\n')

    def test_autofunction_long(self):
        """Make sure instance methods get converted to dotted notation which
        indexes better in Sphinx."""
        self._file_contents_eq(
            'autofunction_long',
            'ContainingClass.someMethod(hi)\n\n   Here.\n')

    def test_autoclass(self):
        """Make sure classes show their class comment and constructor
        comment."""
        self._file_contents_eq(
            'autoclass',
            'class ContainingClass(ho)\n\n   Class doc.\n\n   Constructor doc.\n\n   Arguments:\n      * **ho** -- A thing\n')

    @classmethod
    def teardown_class(cls):
        rmtree(join(cls.docs_dir, '_build'))


DESCRIPTION = """

   Return the ratio of the inline text length of the links in an
   element to the inline text length of the entire element."""

FIELDS = """

   Arguments:
      * **node** (*Node*) -- Something of a single type

   Throws:
      **PartyError|FartyError** -- Something with multiple types

   Returns:
      **Number** -- What a thing
"""

# Oddly enough, the text renderer renders these bullets with a blank line
# between, but the HTML renderer does make them a single list.
CONTENT = """
   Things are "neat".

   Off the beat.

   * Sweet

   * Fleet
"""
