import os
import urllib
import urllib2
import dryscrape
import requests
from bs4 import BeautifulSoup
dryscrape.start_xvfb()
session = dryscrape.Session()

#####################################################

def getHTML(start):
	testmsg = ""
	for j in range(start,len(html)):
		if html[j] == '"':
			break
		testmsg += html[j]
	return testmsg

def downloader(file_name, image_url):
	r = requests.get(image_url, allow_redirects=True)
	if len(r.content) < 10:
		downloader(file_name, image_url)
	else:
		open(file_name +'.jpg', 'wb').write(r.content)

def read_unicode(text, charset='utf-8'):
    if isinstance(text, basestring):
        if not isinstance(text, unicode):
            text = unicode(obj, charset)
    return text

def get_title(text, keywords,endword):
	tmp=""
	for i in range(0,len(text)):
		if text[i:i+len(keywords)] == keywords:
			for k in range(0,len(text)):
				if i+len(keywords)+k == len(text):
					return 0
				else:
					if not text[i+len(keywords)+k:i+len(keywords)+k+len(endword)] == endword:
						tmp += text[i+len(keywords)+k]
					else:
						return tmp

#####################################################

url = 'http://www.kanman.com/'
bookno = raw_input("Comics Number: ")
response = urllib2.urlopen(url+bookno)
html = response.read()

#####################################################

tmpno = 0
booklist = []
booklisttitle = []

titlename = get_title(html, 'de">',"<")
print(titlename)

for i in range(0,len(html)):
	if html[i:i+12] == "chapter-list":
		tmpno=i
		while not get_title(html[tmpno:tmpno+300],'</','>') == "ul":
			tmp1 = get_title(html[tmpno:tmpno+300],'href="','"')
			tmp2 = get_title(html[tmpno:tmpno+300],'title="','">')
			if not (tmp1 == 0 or tmp2 == 0 or tmp1 is None or tmp2 is None):
				booklist.append(tmp1)
				booklisttitle.append(tmp2)
				print("[" + `len(booklist)` + "]" + booklisttitle[len(booklist)-1] + " | " + booklist[len(booklist)-1])	
				while get_title(html[tmpno:tmpno+300],'title="','">') == booklisttitle[len(booklist)-1] :
					if not html[tmpno:tmpno+5] == "</ul>":
						tmpno += 1
					else:
						break
			else:
				tmpno += 1
		break

################################################### 

chapno = raw_input("Chapter ID: ")
start = 0
end = 0

if chapno == "all":
	start = 0
	end = len(booklist)
else:
	chapno = int(chapno)-1
	start = int(chapno)
	end = start + 1

for chapno in range(start,end):
	if not os.path.exists(titlename + "/" + booklist[int(chapno)].split(".")[0]):
		session.visit(url+bookno+"/"+booklist[int(chapno)])
		response = session.body()
		html = BeautifulSoup(response, "lxml")
		if len(html.select('.mh_comicpic')) == 0:
			chapno -= 1
			continue			
		pagelimt = str(html.select('.mh_comicpic')[0])
		if pagelimt[-17:-14] == "spa":
			chapno -= 1
			continue
		chapurl = html.select('.mh_comicpic')[0].img['src']			
		pagelimt = (int(pagelimt[-17:-14]))
		firsthalf = ""
		secondhalf = ""
		os.makedirs(titlename + "/" + booklist[int(chapno)].split(".")[0])
		for num in range(0,len(chapurl)):
			if chapurl[num:num+3] == "%2F":
				firsthalf = chapurl[:num+3]
				if chapurl[-1:] == "e":
					secondhalf = chapurl[-15:]
				else:
					secondhalf = chapurl[-4:]
		for pagenum in range(1,pagelimt+1):
			index = ""
			if pagenum < 10:
				index = "00" + str(pagenum)
			else:
				if pagenum < 100:
					index = "0" + str(pagenum)				
			downloader(titlename + "/" + booklist[int(chapno)].split(".")[0] + "/" + index, firsthalf + str(pagenum) + secondhalf)
		print(titlename + ": " + booklist[int(chapno)] + "Done!")
print(titlename + "Downloaded ALL!")