import urllib2, re, json, unidecode, time
from lxml import html
import helper
from math import floor

#Class to run through the SCOTUS volumes and collect the Case Names and URLS
class VolScraper(object):
	"""Class to Scrape the case names and urls from Justia's Volume Pages"""
  def __init__(self, startVol, stopVol, baseURL):
		self.sttV = startVol
		self.stpV = stopVol
		self.bURL = baseURL

	def scrapeVolumes(self):
          """Scraper Method for the volumes"""
          casesUrls = []
          for i in xrange(self.sttV, (self.stpV + 1)):
              vn = str(i)
              if i % 5 == 0:
                    print "Current Volume: " + str(vn)
              vol = urllib2.urlopen(self.bURL+"/cases/federal/us/"+vn+"/").read()
              #print vol
              ### Parse to find all opinion links
              volTree = html.fromstring(vol)
              #for link in volTree.cssselect('div.result a'):
              for res in volTree.cssselect('div.result'):
                   #print res.text_content()
                   dat = " "
                   ##
                   if i > 105:
                        #Grab Date for volumes over 105
                        text = unidecode.unidecode(res.text_content())
                        d = re.findall('[A-Z][a-z]+ \d{1,2}, \d{4}', text )
                        if len(d) > 0:
                             dat = d[0]
                   for link in res.cssselect('a'):
                        linkText = link.text_content().split(':')
                        cName = linkText[0].strip()
                        ### Append link to cases
                        if cName != "https":
                             casesUrls.append({'url': link.get('href'), 'vol': i, 'caseName': cName, 'date': dat})
          print "Volumes Scraped"
          return casesUrls
#print casesUrls


###Case Build Scraper Class###
class CaseScraper(object):
    """Class to scrape individual case urls and case subpages from a corpus of caseurls
    Args:
        Expects the output from the VolScraper.scrapeVolumes 
    """
    def __init__(self, stopCase, caseLinks, outfile, emails, baseurl):
        self.stopCase = stopCase
        self.caseLinks = caseLinks
        self.outfile = outfile
        self.emails = emails
        self.baseURL = baseurl

    ### Scrape citations
    def caseExtract(self, case):
              x = re.findall('(?<!Page )\d{1,3} U. ?S.,? \d{1,4}', case)
              v = []

              ### Get Volume
              for c in x:
                   d = re.findall('^\d{1,3}', c)
                   s = re.findall('(?<= )\d{1,4}$', c)
                   v.append([int(d[0]), int(s[0])])
              return v

    ### Get Case numbers
    def urlParse(self, url):
         spl = url.split("/")
         spl2 = spl[-2].split("-")
         dock = spl2[-1]
         if re.match('\d*orig', dock):
             dock = dock
         else:
             dock = int(dock)
         return dock
    #print urlParse(casesUrls[0]['url'])

    def caseParse(self, case):
        cTree = html.fromstring(case)
        opinion = cTree.cssselect('div#opinion')
        #should handle error if does not have an opinion page
        op = ""
        for o in opinion:
             op = op + o.text_content()
        unicodeCaseText = unidecode.unidecode(op)
        caseRef = self.caseExtract(unicodeCaseText)
        return unicodeCaseText, caseRef

    def setUrls(self, v):
         suffix = [""]
         if v < 540:
              suffix.append("case")
         elif v < 565:
              suffix = suffix + ["opinion", "concurrence", "dissent"]
         else:
              suffix= suffix + ["opinion3", "concur4", "concur5", "dissent5", "dissent6"]
         return suffix

    def fetchCaseText(self, caseUrl, suffix):
      url = self.baseURL + caseUrl+suffix+".html"
      try:
        cResp = urllib2.urlopen(url).read()
      except urllib2.HTTPError, e:
        return None, None
      else:
        txt, citations = self.caseParse(cResp)
        return txt, citations

    ### Grab Cases
    def getCases(self):
         lt = time.asctime(time.localtime(time.time()))
         problemCases, cases = [], []
         cL = self.caseLinks
         if self.stopCase == False:
              end = len(cL)
              print "Number of cases " + str(end)
         else:
              end = self.stopCase
          # for sometimes count variables to only print once
         lastVol, lastPer = 0, -1
         # Loop through cases
         for c in xrange(end):
              vol = cL[c]['vol']
              dock = self.urlParse(cL[c]['url'])
              cNum = [vol, dock]
              if vol % 5 == 0 and vol > lastVol:
                   print "Volume " + str(vol)
                   lastVol = vol
              #iterate through all of the pages
              links = self.setUrls(vol)
              text = ""
              cites = []
              #Loop through each set of urls to scrape
              for l in xrange(len(links)):
                txt, citations = self.fetchCaseText(cL[c]['url'], links[l])
                if txt != None:
                  text = text + txt
                  cites = cites + citations
              #Add to the list of cases the case information
              cases.append({'name': cL[c]['caseName'], 'url': cL[c]['url'], 'txt': text, 'number': cNum, 'citations': cites, 'vol': cL[c]['vol'], 'date': cL[c]['date']})
              #Save every hunderd cases
              if c % 100 == 0:
                with open(self.outfile, 'w') as fp:
                  json.dump(cases, fp, indent=2)

              #Email every 10% of cases
              per = int(floor((float(c)/float(end)*100)))
              if per % 10 == 0 and self.emails and per > lastPer:
                helper.sendEmail(per, c,end, lt)
                lastPer = per
        #Save at the end of the loop
         with open(self.outfile, 'w') as fp:
              json.dump(cases, fp, indent=2)
         print problemCases
         return cases

