import re, json, unidecode, time

class citations(object):
	"""A separate class to just build and validate the case citations"""
	def __init__(self, cases, outfile):
		self.cases = cases
		self.outfile = outfile

	@staticmethod
	def extractCitations(case):
		""" Uses Regular expressions to extract the estimated citations from the case text
		Previously from the scrapers class as caseExtract
		Args:
			The text of a case
		Returns:
			A list of citations

		"""
		x = re.findall('(?<!Page )\d{1,3} U. ?S.,? \d{1,4}', case)
		v = []

		### Get Volume
		for c in x:
			d = re.findall('^\d{1,3}', c)
			s = re.findall('(?<= )\d{1,4}$', c)
			v.append([int(d[0]), int(s[0])])
		return v

	def cascadeCase(self, citation, caseDict, volumes):
		""" Find the case from the page of the citation (first page of the case)
		Previously "checkCase" in the Grapher Class
		"""
		if citation in caseDict:
			return 1, citation
		else:
		#where volume == citation[0], case where floor of case
		#limit search to this volume
			v = citation[0] - 1
			#assign to the lower case
			for c in volumes[v]:
				if citation[1] > c:
					lowCite = [citation[0], c]
					return 0, lowCite
		return 0, "NULL"

   	def citeToName(self, cite):
   		"""Checks if a citation links to a casename"""
   		for c in xrange(len(self.nameList)):
   			#print nameList[c]['number']
   			if cite == self.cases['number']:
   				return self.cases['name']
   		return None

	def validateName(self, name, caseToCheck):
		if caseToCheck.lower().find(name.lower()) != -1:
			return True
		else:
			return False

	def buildVolList(self):
		"""Assign each case to a nested Volume List for faster hashing"""
		vols = []
		for i in xrange(575):
			vols.append([])
		for c in self.cases:
			v = c['number'][0] - 1
			vols[v].append(c['number'][1])
		for i in xrange(575):
			vols[i].sort()
		return vols

	def matchMetrics(self, totalCitations, modified, validated):
		"""Evaluate the performance of the mathcing algorthims"""
		return [totalCitations, float(modified)/float(totalCitations), float(validated)/float(totalCitations)]

	def processText(self, save_text):
		"""Scaffold for the class"""
		vols = buildVolList()
		case_citations = [] 
		for case in self.cases:
			cites = self.extractCitations(case['txt'])
			cleaned = []
			### Metrics for how many citations were modified tc= Total Citations/ MC modified/ vC Validated
			tC, mC, vC = 0, 0, 0
			for cite in xrange(len(cites)):
				tC = tC + 1
				x, checkedCite = self.cascadeCase(cite, cases, vols)
				mC = mC + x
				n = self.citeToName(checkedCite)
				val = validateName(n, case['txt'])
				if val:
					vC = vC + 1
				cleaned.append(checkedCite)
			if save_text:
				case_citations.append({'name': case['name'], 'url': case['url'], 'txt': case['txt'], 'number': case['number'], 'citations': cleaned, 'vol': case['vol'], 'date': case['date']})
			else:
				case_citations.append({'name': case['name'], 'url': case['url'], 'number': case['number'], 'citations': cleaned, 'vol': case['vol'], 'date': case['date']})
		metrics = self.matchMetrics(tC, mC, vC)
		return case_citations, metrics



