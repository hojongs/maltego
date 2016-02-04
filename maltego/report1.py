from MalwrAPI import MalwrAPI
import requests 
from bs4 import BeautifulSoup


api_authenticated = MalwrAPI(verbose=True, username='ssaemo', password='jeonflma')
#api_authenticated = MalwrAPI(verbose=True)

#res = api_authenticated.submit_sample(filepath='/tmp/waga.exe')
#print res

res = api_authenticated.search(search_word='name:SimDisk_setup.exe')
exit()
#print res
for i in res:
    print "HASH : ",i['hash']
headers = {'User-Agent': 'Mozila 5.0'}
url='https://malwr.com'+res[1]['submission_url']+'#network_http_tab'
r = requests.post(url, headers=headers)
soup = BeautifulSoup(r.text, "lxml") 
print soup
