from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer
import subprocess
import re

# STATION ELEVEN: http://www.8novels.net/classics/u6082.html

####################################### FUNCTIONS ###############################################

def read_html(url):
	# Open and parse the page
	html = urlopen(url).read()

	return html

def get_url(y):
	# Add end 'index' code if code not included
	h = y.rfind('.html')

	if h == -1:
		y = str(y + 'index.html')

	# Isolate 'code' (page identifier) for processing
	f = y.rfind('_')
	g = y.rfind('/')

	if f == -1:
		start1 = y.rfind('/') + 1
		end1 = y.find('.html')
		code = y[start1:end1]

	elif f !=-1 and (f < g):
		start1 = y.rfind('/') + 1
		end1 = y.find('.html')
		code = y[start1:end1]

	else:
		start1 = y.rfind('/') + 1
		end1 = y.rfind('_')
		code = y[start1:end1]

	# Identify 'path' (rest of url) using code
	start = y.find('www.')
	end = y.find(str(code))
	path = y[start:end]

	return path, code

def get_title(html):
	# Find Title element
	title_text = SoupStrainer("title")
	title_soup = str(BeautifulSoup(html, "html.parser", parse_only=title_text))

	# Isolate actual title
	title_start = title_soup.find('Read ') + 5
	title_end = title_soup.find(' online')
	title = title_soup[title_start:title_end]

	return title

def get_pages(html):
	# Find text in which the number of pages is wrapped
	page_text = SoupStrainer("ul", {'class':'pagelist'})
	page_soup = str(BeautifulSoup(html, "html.parser", parse_only=page_text))

	# Isolate number of pages
	pages_start = page_soup.find('<ul class="pagelist"><li><a>') + 28
	pages_end = page_soup.find('pages:')
	pages = page_soup[pages_start:pages_end]

	return pages

def make_file(name):
	# Create filename based on book title and directory
	title = str(name)
	path = '/Users/annabelle_strong/Documents/Bin/Extracted Texts/'
	filename = str(path + title + ".txt")

	# 'Open' (or create if nonexistent) file
	file = open(filename,"w")

	return file, filename

def split_chapters(text):
	index = text.find("Chapter")

	if index != -1:
		text = text[:index - 1] + " " + text[index:]

		subtext = text[index:index + 15].split(" ")

		print(subtext)

		caps = re.findall('([A-Z])', subtext[1])

		print(caps)

		word_1_index = subtext[1].find(caps[0])

		if len(caps) > 1:
			word_2_index = subtext[1].find(caps[1])

		if word_1_index != 0:
			subtext[1] = subtext[1][:word_1_index] + " " + subtext[1][word_1_index:]
		else:
			subtext[1] = subtext[1][:word_2_index] + " " + subtext[1][word_2_index:]

		subtext = str(' '.join(subtext))

		print(subtext)

		text = text[:index] + subtext + text[index + 15:]

	return text

########################################## LOGIC ###############################################

# Get full url
address = input("What's the url of the book you want to parse? ")

# Split url for page looping and processing
raw_url = get_url(address)
path = raw_url[0]
code = raw_url[1]

# Load webpage with full url
url = Request('http://' + str(path) + str(code) +'.html', headers={'User-Agent': 'Mozilla/5.0'})

# Parse page
setup_html = read_html(url)

# Get name of book
title = get_title(setup_html)

# Create .txt file
txt = make_file(title)
file = txt[0]
filename = str(txt[1])

# Get number of pages
pages = int(get_pages(setup_html))


# Loop through pages
for a in range(1, pages+1):
	if a != 1:
		# Load new url based on page number
		new_url = Request('http://' + str(path) + str(code) + '_' + str(a) +'.html', headers={'User-Agent': 'Mozilla/5.0'})
		# Read updated html
		html = read_html(new_url)
	else:
		html = setup_html

	# Filter paragraph text and parse page
	p = SoupStrainer("p")

	soup = BeautifulSoup(html, "html.parser", parse_only=p)

	# Remove all script and style elements
	for script in soup(["script", "style"]):
	    script.extract()    # rip it out

	# Remove copyright line
	for p in soup.find_all("p", {'class':'info'}):
	    p.decompose()

	# Extract text
	text = soup.get_text()

	text = split_chapters(text)

	# Write text to document
	file.write(text)


# Print confirmation
print("Text extraction complete.")

# Open file location
subprocess.call(["open", "-R", filename])
