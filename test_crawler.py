import unittest
import techcrunchcrawler
import sys
from bs4 import BeautifulSoup
from StringIO import StringIO

class TestCrawler(unittest.TestCase):

    def setUp(self):
        self.tc = techcrunchcrawler.TechcrunchCrawler('http://test.com')
        result1={'company name':'abc', 'company website':'http://abc.com', 'article title':'On abc', 'article url':'http://abc.com/xyz'}
        self.expected_output1='company name,company website,article title,article url\r\nabc,http://abc.com,On abc,http://abc.com/xyz\r\n'
        self.expected_result2={'article url': 'https://techcrunch.com/2016/12/13/neveragain-muslim-registry/', 'company website': 'n/a', 'article title': u'Tech companies should probably come out against a Muslim registry now', 'company name': u'Donald J. Trump'}

        self.tc.results.append(result1)
        self.held, sys.stdout = sys.stdout, StringIO()

    def test_filter_links(self):
        links=BeautifulSoup('<a href="https://techcrunch.com/2016/fake/"></a><a href="https://fake.com/"></a>',"lxml")
        print self.tc.filter_links(links)
        self.assertEqual(len(links), 1, msg=None)

    def test_get_link_details(self):
        output = self.tc.get_link_details('https://techcrunch.com/2016/12/13/neveragain-muslim-registry/')
        self.assertEqual(output,self.expected_result2, msg=None)

    def test_csv_output(self):
        output = sys.stdout
        self.tc.csv_output(output)
        self.assertEqual(output.getvalue(), self.expected_output1, msg=None)


if __name__ == '__main__':
    unittest.main()
