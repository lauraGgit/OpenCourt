import regex, json, unidecode, time

class citations(object):
	"""A separate class to just build and validate the case citations"""
	def __init__(self, cases, outfile):
		self.cases = cases
		self.outfile = outfile+".json"

	@staticmethod
	def extractCitations(case):
		""" Uses Regular expressions to extract the estimated citations from the case text
		Previously from the scrapers class as caseExtract
		Args:
			The text of a case
		Returns:
			A list of citations

		"""
		x = regex.findall('(?<!Page|P.) \d{1,3} U. S. \d{1,4}', case)
		v = []

		### Get Volume
		for c in xrange(len(x)):
			d = regex.findall('^\d{1,3}', x[c][1:])
			s = regex.findall('(?<= )\d{1,4}$', x[c][1:])
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
		return 0, None

   	def citeToName(self, cite):
   		"""Checks if a citation links to a casename"""
   		for c in self.cases:
   			#print nameList[c]['number']
   			if cite == c['number']:
   				return c['name']
   		return None

	def validateName(self, name, caseToCheck):
		if caseToCheck.lower().find(name.lower()) != -1:
			return True
		else:
			return False

	def buildVolCaseList(self):
		"""Assign each case to a nested Volume List for faster hashing"""
		vols, cL = [], []
		for i in xrange(575):
			vols.append([])
		for c in self.cases:
			v = c['number'][0] - 1
			vols[v].append(c['number'][1])
			cL.append(c['number'])
		for i in xrange(575):
			vols[i].sort()
		return vols, cL

	def matchMetrics(self, totalCitations, modified, validated, errs):
		"""Evaluate the performance of the mathcing algorthims"""
		tc = float(totalCitations)
		return [tc, float(modified)/tc, float(validated)/tc, float(errs)/tc]

	def processText(self, save_text):
		"""Scaffold for the class"""
		vols, caseList = self.buildVolCaseList()
		case_citations = []
		for case in self.cases:
			cites = self.extractCitations(case['txt'])
			cleaned = []
			### Metrics for how many citations were modified tc= Total Citations/ MC modified/ vC Validated
			tC, mC, vC, eC = 0, 0, 0, 0
			for c in xrange(len(cites)):
				tC = tC + 1
				x, chckd = self.cascadeCase(cites[c], caseList, vols)
				mC = mC + x
				if (chckd == None):
					eC = eC + 1
				else:
					if chckd[0] != case['vol'] and chckd[1] != case['number']:
						n = self.citeToName(chckd)
						if n != None:
							valC = self.validateName(n, case['txt'])
							if valC:
								vC = vC + 1
							if chckd not in cleaned:
								cleaned.append(chckd)
						else:
							eC = eC + 1
			# if len(cleaned) > 0:
			# 	print cleaned
			if save_text:
				case_citations.append({'name': case['name'], 'url': case['url'], 'txt': case['txt'], 'number': case['number'], 'citations': cleaned, 'vol': case['vol'], 'date': case['date']})
			else:
				case_citations.append({'name': case['name'], 'url': case['url'], 'number': case['number'], 'citations': cleaned, 'vol': case['vol'], 'date': case['date']})
		with open(self.outfile, 'w') as fp:
			json.dump(case_citations, fp, indent=2)
		metrics = self.matchMetrics(tC, mC, vC)
		return case_citations, metrics



