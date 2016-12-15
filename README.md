# techcrunchcrawler
Simple command line python app to go to techcrunch.com, read each article and determine which company (if any) is the primary subject matter of the article.
The output of the program will be a csv file with the following:
company name,company website,article title,article url
In the case where the company name and/or website cannot be determined then use n/a in place of the name or website.

You need dryscrape, bs4 python library installed.
