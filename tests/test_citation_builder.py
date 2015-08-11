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

    def test_validateName(self):
    	self.assertTrue(self._citation.validateName("Respublica v. Roberts", test_cases.case39))
        self.assertFalse(self._citation.validateName("Romer v. Evans", test_cases.case39))
    

if __name__ == '__main__':
    unittest.main()