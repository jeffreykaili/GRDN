'''
Webscraper that was used to retrieve all the names, addresses and coordinates of all the farmers markets used within our map 
'''
from bs4 import BeautifulSoup 
import requests
import re
url = requests.get("https://www.farmersmarketsontario.com/find-a-farmers-market/").content
pageContent = BeautifulSoup(url, "lxml")
pageInfo = pageContent.find("tbody")
coordPos = pageInfo.findAll("tr", {"class:", "market-row"})
latitude = []
longitude = []
nameList = []
hrefList = []
cnt = 0
for each in coordPos:
	coords = re.findall(r'[-]*\d+[.]\d+',str(each).split(">")[0])
	if not(len(coords)):continue
	latitude.append(float(coords[0]))
	longitude.append(float(coords[1]))
	name = each.find("a").getText()
	nameList.append(name)
	href = re.findall(r'["][^"]+["]',str(each.find("a")))[0][1:-1]
	hrefList.append(href)
#Full Address Handling
fAddress = []
for link in hrefList:
	url = requests.get("https://www.farmersmarketsontario.com/" + link).content
	pageContent = BeautifulSoup(url, "lxml").find("tbody")
	fullAddress = re.findall(r'<td>.*</td>',re.findall(r'Address.*?</td>',str(pageContent))[0].replace("<br/>", ""))[0].replace("<td>","").replace("</td>","")
	fAddress.append(fullAddress)