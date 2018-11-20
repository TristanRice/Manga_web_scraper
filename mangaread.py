import requests
from bs4 import BeautifulSoup as BSoup
import lxml

#first set up the global variables
BASE_URL = "https://www.wuxiaworld.com"

class Story(Thread):

	def __init__(self, url):
		self.url = url
		self.chapters = self.get_chapters( )

	def get_chapters(self):
		r = requests.get(self.url)
		

	def get_text(self):
		pass

def get_all_a_tags(url, a_class=""):
	r = requests.get(url)
	soup = BSoup(r.text, "lxml")
	links = soup.find_all("a", class_=a_class)

	for link in links:
		yield {
			"url":url+link,
			"text":link.text
		}

def stories( ):
	url    = BASE_URL+"/tag/completed"
	r 	   = requests.get(url)
	soup   = BSoup(r.text, "lxml")
	titles = soup.find_all("a", class_="text-white")
	
	for title in titles:
		yield {"url":BASE_URL+title["href"], "name":title.text}


def main( ):
	
	for story in stories( ):
		s = Story(story["url"])

		with open(story["title"]+".txt", "w") as f:
			f.write(s.get_text( ))

if __name__=='__main__':
	main( )