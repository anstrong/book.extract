from urllib.request import Request, urlopen
from bs4 import BeautifulSoup, SoupStrainer

# https://www.8novels.net/classics/u6082.html

# Get url
y = input("What's the url of the book you want to parse? ")

# Get number of pages
x = int(input("How many pages in the book? "))

# Get name
z = input("What's the name of the book? ")

# Create .txt file
path = '/Users/annabelle_strong/Documents/Bin/Extracted Texts/'
filename = str(z)

file = open(path + filename,"w") 

# Split url
f = y.find('_')

if f == -1:
	start1 = y.rfind('/') + 1
	end1 = y.find('.html')
	code = y[start1:end1]

else:
	start1 = y.rfind('/') + 1
	end1 = y.find('_') 
	code = y[start1:end1]

start = y.find('www.')
end = y.find(str(code)) 
path = y[start:end]

# Loop through pages
for a in range(1, x+1):
	# Use split url to form complete url
	if a == 1:
		url = Request('http://' + str(path) + str(code) + '.html', headers={'User-Agent': 'Mozilla/5.0'})
	else:
		url = Request('http://' + str(path) + str(code) + '_' + str(a) +'.html', headers={'User-Agent': 'Mozilla/5.0'})
	
	# Read html
	html = urlopen(url).read()

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

	# Write text to document
	file.write(text)

print("Text extraction complete.")






