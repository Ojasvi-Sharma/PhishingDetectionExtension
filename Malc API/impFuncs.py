import re
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup

from selenium import webdriver  
from selenium.common.exceptions import NoSuchElementException  
from selenium.webdriver.common.keys import Keys
import time

def getSoup(url):
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0'}
	#try:
	req = Request(url, headers=headers)
	req = urlopen(req)
	soup = BeautifulSoup(req, 'html.parser')
	#except:
	#	soup2 = -2
	return soup

def getDomain(url):
	if re.search('www', url):
		start = url.find('www') + 4
		stop = url[start:].find('/') + start
		return url[start:stop]
	elif re.search('http://', url):
		start = url.find('http://') + 7
		stop = url[start:].find('/') + start
		return url[start:stop]
	elif re.search('https://', url):
		start = url.find('https://') + 8
		stop = url[start:].find('/') + start
		return url[start:stop]
	else:
		return ''

def prefixSuffix(url):
	domain = getDomain(url)
	if re.search('-', domain):
		return -1
	else:
		return 1

def checkSubdomains(url):
	domain = getDomain(url)
	res = len(domain.split('.'))
	return (res- 2.78)/0.78

def checkSSL(url):
	lnk = 'https://www.sslshopper.com/ssl-checker.html#hostname='+url
	browser = webdriver.Chrome(executable_path='C:/chromedriver.exe')  
	browser.get(lnk)
	time.sleep(10)
	html_source = browser.page_source  
	browser.quit()

	rc = BeautifulSoup(html_source, 'html.parser')
	try:
		val = rc.find('table', {'class':'checker_messages'})
		res1 = val.findAll('span')[0].text
		restmp = val.findAll('td', {'class':'failed'})
		if restmp == []:
			res2 = 0
		else:
			res2 = 1
		res = [res1, res2]
	except:
		res = ['-1','-1']

	return res

def hasDoubleSlashes(url):
	if url.rfind('//') > 6:
		return -1
	else:
		return 1

def checkAnchors(url):
	no = ['#', 'javascript', 'mailto']
	soup = getSoup(url)
	if soup == -1:
		return 'Nope'
	domain = getDomain(url)
	yes = [domain, url]
	ls = soup.find_all('a', href=True)
	mal = 0
	if len(ls) == 0:
		return (1- 215.22)/90.4
	for a in ls:
		for i in no:
			if i in a['href'].lower():
				mal += 1
		for i in yes:
			if i not in a['href']:
				mal += 1
	danger = (mal/len(ls))*100
	return (danger - 215.22)/90.4

def checkServerForm(url):
	soup = getSoup(url)
	if soup == -1:
		return 'Nope'
	domain = getDomain(url)
	ls = soup.find_all('form', action=True)
	for i in ls:
		if i['action'] =="" or i['action'] == "about:blank":
			return -1
		if domain not in i['action'] or url not in i['action']:
			return 0
	return 1

def isIpAddress(url):
	ip4 = re.match('([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])\.([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])\.([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])\.([0-2]?[0-5]{1,2}|[0-1]?[0-9]{1,2}|[0-2]?[0-4][0-9])$', url)
	ip6 = re.match('([0-9A-Fa-f]{1,4}\:){1,7}[0-9A-Fa-f]{1,4}$|([0-9A-Fa-f]{1,4}\:){1,7}\:$', url)
	if ip6 or ip4:
		return -1
	else:
		return 1

def checkHTTPSinURL(url):
	if url[0:5] == 'https':
		return 1
	else:
		return -1