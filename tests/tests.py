import unittest
from lib import grapher, helper, scrapers, citation_builders

class TestOCMethods(unittest.TestCase):
    """Tests for OpenCourt"""
    @classmethod
    def setUpClass(cls):
        cls._citation = citation_builders.citations([], 'outfile.txt')

    def test_citeToName(self):
        self.assertEqual(self._citation, )