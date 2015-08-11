import unittest
from lib import citation_builders
import test_cases
class TestOCMethods(unittest.TestCase):
    """Tests for OpenCourt"""
    @classmethod
    def setUpClass(cls):
        cls._citation = citation_builders.citations([], 'outfile.txt')

    def test_citeToName(self):
  
        self.assertEqual(self._citation.citeToName([1,2],test_cases.nameList), "BETHEL v. LLOYD")
        self.assertEqual(self._citation.citeToName([475,8],test_cases.nameList), None)

if __name__ == '__main__':
    unittest.main()