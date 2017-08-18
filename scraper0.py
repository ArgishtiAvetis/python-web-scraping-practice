from bs4 import BeautifulSoup
import requests

# website source 
website = 'https://losangeles.craigslist.org/search/ant/eee?sale_date=2017-07-30'

html = requests.get(website).content
soup = BeautifulSoup(html, "html.parser")

#  finds <a> tags with class="hdrlnk"
raw_links = soup.find_all('a', attrs={'class': 'hdrlnk'})

links = []
for link in raw_links:
	if 'http' in link.get('href'):
		links.append(link.get('href'))		
	else:
		link.append('https://losangeles.craigslist.org' + link.get('href'))

print(links)

file = open('events.txt', 'a')

# goes to the links and scrapes listing information :)
# soup.find()'s arguments might be different depending on what "type" of webpage is being scraped

for url in links:
	response = requests.get(url)
	html = response.content
	soup = BeautifulSoup(html, "html.parser")
	title = soup.find('span', attrs={'id': 'titletextonly'}).get_text()
	body = soup.find('section', attrs={'id': 'postingbody'}).get_text()
	file.write(title + '\n' + body + '\n')
	file.write('\n----------------------------\n')

file.close()