import requests
from bs4 import BeautifulSoup as BSoup
import lxml
import sys
import os #this is needed to allow the user to make their own custom directory
import io

#first set up the global variables
BASE_URL = "https://www.wuxiaworld.com"
DEFAULT_DIRECTORY = "stories"

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

def print_help( ):
	print("Usage: python mangaread.py <Directory that you want to save the stories in>")

def main( ):
	try:
		directory = sys.argv[1]
		if directory=="-h":
			print_help( )
			exit(0)
	except IndexError:
		directory = DEFAULT_DIRECTORY
	os.system("mkdir "+directory) #reEE command injection vulnerability
	stories = get_all_tags(BASE_URL+"/tag/completed", "text-white")
	for i, story in enumerate(stories): #(use enumerate so I can have more verbosity)
		print("[*] Getting {}, story number {}".format(story.text.strip(), i+1))
		#For some reason using open doesn't work on windows, but usign io.open and specifying an encoding does.
		with io.open("{}/{}.txt".format(directory, story.text.strip()), "w", encoding="utf-8") as f:
			f.write(str(get_story(story["href"])))

if __name__=='__main__':
	main( )