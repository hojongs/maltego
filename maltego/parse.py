import requests
from bs4 import BeautifulSoup
#vt_url ='https://www.virustotal.com/en/search/'
vt_url='http://localhost/login.php'
vt_url='https://malwr.com/analysis/search/'
#headers=''
#postdata=''
headers = {'User-Agent': 'Mozila 5.0'}
postdata = {'query': 'HASH_VALUE_OF_MALWARE_SAMPLE'}
r = requests.post(vt_url, headers=headers, data=postdata)
soup = BeautifulSoup(r.text,"lxml")
print soup
exit()
strongs = soup.find_all("strong", text="URL:") #<strong>URL:</strong>
#print strongs
for strong in strongs:
    """
    print strong.find_parent().contents
    num=0
    for i in strong.find_parent().contents:
        print str(num)+":",i
        num+=1
    """
    print strong.find_parent().contents[3]
#    print strong.find_parent().contents[3].strip()
