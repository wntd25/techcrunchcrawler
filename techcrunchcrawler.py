import csv
import dryscrape
import sys
import datetime
from bs4 import BeautifulSoup

class TechcrunchCrawler:

    def __init__(self, url='https://techcrunch.com'):
        self.url = url
        self.results = []
        now = datetime.datetime.now()
        self.year = now.year
        # encode in unicode
        reload(sys)
        sys.setdefaultencoding('utf-8')

    def find_all_links(self):
        # set up a web scraping session
       session = dryscrape.Session()
       # we don't need images
       session.set_attribute('auto_load_images', False)
       session.visit(self.url)
       response = session.body()
       soup=BeautifulSoup(response,"lxml")
       links = soup.find_all('a')
       return links

    def filter_links(self,links):
        """Filter links that begin with base url and year only
               """
        filtered_links = set()
        for a in links:
            if a.has_attr('href'):
                if a['href'].startswith(self.url + '/' + str(self.year)) and a['href'].endswith('/'):
                    filtered_links.add(a['href'])
        return filtered_links

    def get_link_details(self,url):
        """Get details from given link
               """
        result = {}
        session = dryscrape.Session()
        # we don't need images
        session.set_attribute('auto_load_images', False)
        session.visit(url)
        response = session.body()
        soup=BeautifulSoup(response,"lxml")
        result['article title']=soup.find('h1').string if soup.find('h1') else 'n/a'
        result['company name']=soup.find(name='a', attrs={'class': 'cb-card-title-link'}).text.strip() if soup.find(name='a', attrs={'class': 'cb-card-title-link'}) else 'n/a'
        info= soup.find("ul", attrs={'class':'card-info'}).findAll("a") if soup.find("ul", attrs={'class':'card-info'}) else ''
        result['company website'] = info[-2].string if len(info)>2 else 'n/a'
        result['article url']=url
        return result

    def csv_output(self,filehandler):
        """Write the processed rows to the given filename
               """
        FIELDNAMES = ['article title', 'article url', 'company name', 'company website']

        writer = csv.DictWriter(filehandler, delimiter=',', fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(self.results)

if __name__ == '__main__':
    tc = TechcrunchCrawler('https://techcrunch.com')

    links = tc.find_all_links()
    links = tc.filter_links(links)
    for link in links:
       tc.results.append(tc.get_link_details(link))
    tc.csv_output(sys.stdout)