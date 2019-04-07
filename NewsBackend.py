from newsapi.newsapi_client import NewsApiClient
import pprint
#import readline


#https://pythonprogramminglanguage.com/pyqt-textarea/
#https://newsapi.org/

API_KEY = "37cab213e3624194972d9fdde5013cc2"
API = NewsApiClient(api_key=API_KEY)
DEFAULT_SOURCE = 0

FORMAT = [	"source",
			"description",
			"url",
			"title",
			"publishedAt",
			"author",
			"content",
			"urlToImage"
		]

SOURCES = [	 "bloomberg",
			 "bbc-news",
			 "business-insider" ,
			 "financial-times",
			 "the-economist"
		  ]

#Format
pp = pprint.PrettyPrinter(indent=4)

def GetNews(company_name, choice = DEFAULT_SOURCE):
	archive = {}
	news = None

	for source in SOURCES:
		API.get_top_headlines(sources=SOURCES[choice])
		news = API.get_everything(q=company_name)
		for article in news["articles"]:
			if article["title"] not in archive:
				archive[article["title"]] = article

	return archive

def GetArticles(company_name, choice = DEFAULT_SOURCE):
	newsinfo = GetNews(company_name, choice)

	lst = []


	for article in newsinfo:
		h = {}
		h["title"] = article
		h['author'] = newsinfo[article]["author"]
		h['description'] = newsinfo[article]["description"]
		h['url'] = newsinfo[article]["url"]
		lst.append(h)

	return GetArticlesFormatted(lst)

def GetArticlesFormatted(lst):
	string = ""

	if not lst:
		return ""

	for article in lst:

		if article["title"]:
			string += "TITLE: " + article["title"] + "\n"

		if article["author"]:
			string += "AUTHOR: " + article["author"] + "\n"


		if article["description"]:
			string += "DESCRIPTION: " + article["description"] + "\n"

		if article["url"]:
			string += "READ MORE: " + article["url"] + "\n\n\n"

	return string
