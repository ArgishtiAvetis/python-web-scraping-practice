from __future__ import print_function
from bs4 import BeautifulSoup
import mysql.connector
import urllib2
import requests


# 1. install (using pip), import dependencies
# 2. read BeautifulSoup, urllib & mysql.connector documentation

# This is a sample (not too simple, nor too complex) code snippet that 
# 1. goes to the main_source and scrapes all the links from it, pushes them into an array
# 2. goes through the links in the array and scrapes more data
# 3. in the end, puts the Link, Title and Description of the webpage into the DB

# http = urllib3.PoolManager()

# you'll need to have a MySQL installed (mine was through XAMPP apache server)
# and a database
cnx = mysql.connector.connect(user='root', database='__py_websites')
cursor = cnx.cursor()

# main source; all the other sources will be scraped from this location
main_source = 'http://www.moo-directory.com/index.php?go=results&search=a&Submit=Search+Now'

html = requests.get(main_source).content
soup = BeautifulSoup(html, "html.parser")

# find all links
external_links = soup.find_all('a')

sources = []

for e_links in external_links:
  # detect if the HREF attribute is the "full" URL like "http://example.com/dir/file.html"
  # if not, add the protocol and the domain name yourself
  if 'http' in e_links.get('href'):
    print("\n has HTTP(s) \n")
    valid_link = e_links.get('href')
  else:
    print("\n ADDING HTTP(s) \n")
    valid_link = "http://moo-directory.com" + e_links.get('href')

  print("Link --->>> " + valid_link)
  sources.append(valid_link)

for source in sources:
  links = []

  html = requests.get(source).content
  soup = BeautifulSoup(html, "html.parser")


  listings = soup.find_all('a')
  for listing in listings:
    link = listing.get('href')

    if 'http' in link:
      print("\n has HTTP(s) \n")
      valid_link = link
    else:
      print("\n ADDING HTTP(s) \n")
      valid_link = source
    links.append(valid_link)
    print(valid_link)

  for link in links:
    #if http.request('GET', link).status == 200:
    print("trying..." + link)

    # tried to implement "link cheking"
    # some type of errors are skipped (which is good) but there are some exceptions that need to be handled
    try:
      urllib2.urlopen(link)
      print("Link working :) ")
    except urllib2.URLError:
      print("Link not working :( ")
      continue

    html = requests.get(link).content
    soup = BeautifulSoup(html, "html.parser")

    # if the webpage has <title> and <meta name="description"> tags, go ahead and scrape them
    # otherwise insert "not provided" into the DB

    if soup.title:
      title = soup.title.get_text().encode('utf-8').strip()
    else:
      title = "No title provided."
    print(len(soup.find_all('meta', attrs={'name': 'description'})))
    if soup.find('meta', attrs={'name': 'description'}) is not None and soup.find('meta', attrs={'name': 'description'}).get('content') is not None:
      description = soup.find('meta', attrs={'name': 'description'}).get('content').encode('utf-8').strip()
    else:
      description = "Not provided."
    add_website= ("INSERT INTO websites "
                   "(url, title, description) "
                   "VALUES (%s, %s, %s)")
    data_website = (link, title, description)
    # Insert new website
    print("\n-- Title -- \n" + title + "\n -- Description -- \n" + description + "\n")
    cursor.execute(add_website, data_website)

  # Make sure data is committed to the database
  cnx.commit()

cursor.close()
cnx.close()