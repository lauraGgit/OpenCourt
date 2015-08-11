import unittest
from lib import grapher
import test_cases

class TestOCMethods(unittest.TestCase):
    """Tests for OpenCourt"""
    @classmethod
    def setUpClass(cls):
        cls._grapher = grapher.GraphBuilder([], 'outfile.txt', 2,"https://supreme.justia.com")

    def test_getYear(self):
    	self.assertEqual(self._grapher.getYear("April 21, 2015"), 2015)

  	#def drawGraph(self):

if __name__ == '__main__':
    unittest.main()