import requests
from bs4 import BeautifulSoup as BSoup
import lxml
import re

#first set up the global variables
BASE_URL = "https://www.wuxiaworld.com"

def get_all_tags(url, element_class="", tag="a"):
	#General purpose function for getting all tags from a page
	r = requests.get(url)
	soup = BSoup(r.text, "lxml")
	return soup.find_all(tag, class_=element_class)

class Story:

	def __init__(self, url):
		self.url = BASE_URL+url
		self.chapters = self.get_chapters( )

	def get_chapters(self):
		all_links = get_all_tags(self.url, element_class="chapter-item", tag="li")
		return [li.findChildren("a")[0]["href"] for li in all_links]
		
	def get_text(self):
		return ''.join([get_all_tags(BASE_URL+i, "fr-view", "div")[0].text 
					   for i in self.chapters])

def main( ):
	stories = get_all_tags(BASE_URL+"/tag/completed", "text-white")
	for story in stories:
		s = Story(story["href"])
		with open(story.text.strip( )+".txt", "w") as f:
			f.write(str(s.get_text( )))

if __name__=='__main__':
	main( )