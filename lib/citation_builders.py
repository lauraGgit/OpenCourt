import re, json, unidecode, time

class citations(object):
	"""A separate class to just build and validate the case citations"""
	def __init__(self, cases, outfile):
		self.cases = cases
		self.outfile = outfile

	def extCite(self, case):
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

   	def citeToName(self, cite, nameList):
   		"""Checks if a citation links to a casename"""
   		for c in nameList:
   			if cite == nameList['number']:
   				return nameList['name']
   		return None

	def validateName(self, name, caseToCheck):
		if caseToCheck.find(name) != -1:
			return True
		else:
			return False



