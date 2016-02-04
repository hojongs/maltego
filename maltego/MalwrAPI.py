"""
This is the (unofficial) Python API for malwr.com Website.
Using this code, you can retrieve recent analyses, domains, tags but also latest comments.
You can also submit files

"""
import hashlib

import re
import requests
from bs4 import BeautifulSoup

import requests

class MalwrAPI(object):
    """
        MalwrAPI Main Handler
    """
    session = None
    logged = False
    verbose = False

    url = "https://malwr.com"
    headers = {
        'User-Agent': "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:41.0) " +
                      "Gecko/20100101 Firefox/41.0"
    }

    def __init__(self, verbose=False, username=None, password=None):

        self.verbose = verbose
        self.session = requests.session()

        # Authenticate and store the session
        if username and password:

            soup = self.request_to_soup(self.url + '/account/login')
            csrf_input = soup.find(attrs=dict(name='csrfmiddlewaretoken'))
            csrf_token = csrf_input['value']
            payload = {
                'csrfmiddlewaretoken': csrf_token,
                'username': u'{0}'.format(username),
                'password': u'{0}'.format(password)
            }
            login_request = self.session.post("https://malwr.com/account/login/",
                                              data=payload, headers=self.headers)

            if login_request.status_code == 200:
                self.logged = True
            else:
                self.logged = False
                print "Not being able to log you"

    def request_to_soup(self, url=None):

        if not url:
            url = self.url

        req = self.session.get(url, headers=self.headers)
        soup = BeautifulSoup(req.content, "html.parser")

        return soup

    def display_message(self, s):

        if self.verbose:
            print '[verbose] %s' % s

    def get_latest_comments(self):

        res = []
        soup = self.request_to_soup()
        comments = soup.findAll('div', {'class': 'span6'})[3]

        for comment in comments.findAll('tr'):
            infos = comment.findAll('td')

            infos_to_add = {
                'comment': infos[0].string,
                'comment_url': infos[1].find('a')['href']
            }
            res.append(infos_to_add)

        return res

    def get_recent_domains(self):

        res = []
        soup = self.request_to_soup()

        domains = soup.findAll('div', {'class': 'span6'})[1]
        for domain in domains.findAll('tr'):
            infos = domain.findAll('td')

            infos_to_add = {
                'domain_name': infos[0].find('span').string,
                'url_analysis': infos[1].find('a')['href']
            }
            res.append(infos_to_add)

        return res

    def get_public_tags(self):

        res = []
        soup = self.request_to_soup()

        tags = soup.findAll('div', {'class': 'span6'})[2]
        for tag in tags.findAll('a', {'class': 'tag-label'}):
            res.append(tag.string)

        return res

    def get_recent_analyses(self):

        res = []
        soup = self.request_to_soup()

        submissions = soup.findAll('div', {'class': 'span6'})[0]
        for submission in submissions.findAll('tr'):
            infos = submission.findAll('td')

            infos_to_add = {
                'submission_time': infos[0].string,
                'hash': infos[1].find('a').string,
                'submission_url': infos[1].find('a')['href']
            }
            res.append(infos_to_add)

        return res

    def submit_sample(self, filepath, analyze=True, share=True, private=True):

        s = self.session
        req = s.get(self.url + '/submission/', headers=self.headers)

        soup = BeautifulSoup(req.content, "html.parser")

        # TODO: math_captcha_question might be unused. Remove.
        # math_captcha_question = soup.find('input', {'name': 'math_captcha_question'})['value']

        pattern = '(\d [-+*] \d) ='
        data = {
            'math_captcha_field': eval(re.findall(pattern, req.content)[0]),
            'math_captcha_question': soup.find('input', {'name': 'math_captcha_question'})['value'],
            'csrfmiddlewaretoken': soup.find('input', {'name': 'csrfmiddlewaretoken'})['value'],
            'share': 'on' if share else 'off',  # share by default
            'analyze': 'on' if analyze else 'off',  # analyze by default
            'private': 'on' if private else 'off'  # private by default
        }

        req = s.post(self.url + '/submission/', data=data, headers=self.headers,
                     files={'sample': open(filepath, 'rb')})

        # TODO: soup might be unused. Remove.
        # soup = BeautifulSoup(req.content, "html.parser")

        # regex to check if the file was already submitted before
        pattern = '(\/analysis\/[a-zA-Z0-9]{12,}\/)'
        submission_links = re.findall(pattern, req.content)

        res = {
            'md5': hashlib.md5(open(filepath, 'rb').read()).hexdigest(),
            'file': filepath
        }

        if len(submission_links) > 0:
            self.display_message('File %s was already submitted, taking last analysis' % filepath)
            res['analysis_link'] = submission_links[0]
        else:
            pattern = '(\/submission\/status\/[a-zA-Z0-9]{12,}\/)'
            submission_status = re.findall(pattern, req.content)

            if len(submission_status) > 0:
                res['analysis_link'] = submission_status[0]
            elif 'file like this waiting for processing, submission aborted.' in req.content:
                self.display_message('File already submitted, check on the site')

                return None
            else:
                self.display_message('Error with the file %s' % filepath)

                return None

        return res

    def search(self, search_word):

        # Do nothing if not logged in
        if not self.logged:
            return []

        search_url = self.url + '/analysis/search/'
        c = self.request_to_soup(search_url)

        csrf_input = c.find(attrs=dict(name='csrfmiddlewaretoken'))
        csrf_token = csrf_input['value']
        payload = {
            'csrfmiddlewaretoken': csrf_token,
            'search': u'{}'.format(search_word)
        }
        sc = self.session.post(search_url, data=payload, headers=self.headers)
        ssc = BeautifulSoup(sc.content, "html.parser")

        res = []
        submissions = ssc.findAll('div', {'class': 'box-content'})[0]
        sub = submissions.findAll('tbody')[0]
        for submission in sub.findAll('tr'):
            infos = submission.findAll('td')
            infos_to_add = {
                'submission_time': infos[0].string,
                'hash': infos[1].find('a').string,
                'submission_url': infos[1].find('a')['href'],
                'file_name': infos[2].string
            }
            res.append(infos_to_add)

#        return res

	print 'search:','\''+search_word+'\''
	print

	for i in res: #1
	    print "hash:",i['hash']

	    anal_url = self.url + i['submission_url'] #2
	    print 'url:',anal_url
	    c = self.request_to_soup(anal_url)

	    #dropped = c.find(id='dropped')
	    dropped = c.find_all(text='MD5')
	    print type(dropped)
	    for j in dropped:
		j.find_parent()
		print type(j)
		print j
	        #j = j.findAll('td')
	    #print dropped
	    exit()
	    for j in dropped:
	        k=j.find_all('b')
	        if k:
	            print 'drop:',''.join(k[0])
	    ipv4 = c.find(id='network')
	    ipv4 = ipv4.find(id='hosts')
	    ipv4 = ipv4.find('td')
	    print 'ipv4address:',''.join(ipv4)
	    #print 'ipv4address:',''.join(ipv4[12])i
	    filename = c.find(id='file').find('td')
	    print ''.join(filename)
	    print
	"""
	dropped = c.find_all("div", class_="container-fluid")
	
	dropped = dropped.find_all("div")
	print 'center:',dropped
	dropped = dropped.find_all('div', class_="tab-content")
	dropped = dropped.find_all('div', id_="dropped")
	dropped = dropped.find_all('div', class_="box")
	dropped = dropped.find_all('div', class_="box-content")
	dropped = dropped.find_all('table', class_="table")
	dropped = dropped.find_all('tbody')
	dropped = dropped.find_all('tr')
	"""

        #print 'drop:',dropped

