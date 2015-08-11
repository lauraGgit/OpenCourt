import unittest
from lib import scrapers
import test_cases

class TestOCMethods(unittest.TestCase):
    """Tests for OpenCourt"""
    @classmethod
    def setUpClass(cls):
        cls._volScrape = scrapers.VolScraper(1, 5, "https://supreme.justia.com")
        cls._caseScrape = scrapers.CaseScraper(5, test_cases.caseUrls, "test_json.json", False, "https://supreme.justia.com")

    def test_scrapeVolumes(self):
        self.assertEqual(self._volScrape.scrapeVolumes(), test_cases.caseUrls)

    #Test CaseScrape Functions
    def test_urlParse(self):
    	self.assertEqual(self._caseScrape.urlParse('/cases/federal/us/1/39/'), 39)

    # def test_caseParse(self):
    # 	self.assertEqual(self._caseScrape.caseParse(), test_cases.nameList[0]['txt'])

    def test_suffix(self):
    	self.assertEqual(self._caseScrape.setUrls(47), ["", "case"])
    	self.assertEqual(self._caseScrape.setUrls(552), ["", "opinion", "concurrence", "dissent"])
    	self.assertEqual(self._caseScrape.setUrls(571), ["", "opinion3", "concur4", "concur5", "dissent5", "dissent6"])

    # def test_fetchCaseText(self):
    # 	self.assertEqual(self._caseScrape.fetchCaseText('/cases/federal/us/1/39/','case'), test_cases.rawHTML)

    def test_Disclamer(case):
    	self.assertEqual(self._caseScrape.deleteDisclamer(test_cases.nameList[0]['txt']), test_cases.noDisclaimer)


if __name__ == '__main__':
    unittest.main()