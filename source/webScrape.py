from newspaper import Article
from summarize import summarize

def getArticle(url):

	article = Article(url)
	article.download()
	article.parse()

	title = article.title
	body = article.text

	return [title, body]