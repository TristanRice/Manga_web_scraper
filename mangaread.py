import requests
from bs4 import BeautifulSoup as BSoup
import lxml
import sys
import os #this is needed to allow the user to make their own custom directory

#first set up the global variables
BASE_URL = "https://www.wuxiaworld.com"
DEFAULT_DIRECTORY = "stores"

def get_all_tags(url, element_class="", tag="a"):
	#General purpose function for getting all tags from a page
	print("[*] Getting data from {}".format(url))
	r = requests.get(url)
	soup = BSoup(r.text, "lxml")
	return soup.find_all(tag, class_=element_class)

def get_story(url):
	#frst get the URLs for each chapter in the story 
	all_links = get_all_tags(BASE_URL+url, element_class="chapter-item", tag="li")
	#since the a tags have no classes, I need to get the li tags taht they are under
	chapters  = [li.findChildren("a")[0]["href"] for li in all_links]
	#go through each chapter, and get the text
	return '\n'.join([get_all_tags(BASE_URL+i, "fr-view", "div")[0].text for i in chapters])

def main( ):
	try:
		directory = sys.argv[1]
	except IndexError:
		directory = DEFAULT_DIRECTORY
	os.system("mkdir "+directory)
	stories = get_all_tags(BASE_URL+"/tag/completed", "text-white")
	for i, story in enumerate(stories): #(use enumerate so I can have more verbosity)
		print("[*] Getting {}, story number {}".format(story.text.strip(), i+1))
		with open("{}/{}.txt".format(directory, story.text.strip()), "w") as f:
			f.write(str(get_story(story["href"])))

if __name__=='__main__':
	main( )