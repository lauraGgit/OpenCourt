import networkx as nx
from networkx.readwrite import json_graph
import json
import re
#import matplotlib.pyplot as plt
import helper

#Class for converting Case Citations into Graph
class GraphBuilder(object):
    def __init__(self, caseDict, outfile, gml, baseURL):
      self.caseDict = caseDict
      self.outfile = outfile
      self.gml = gml
      self.baseURL = baseURL

    def getYear(self, dat):
      """Extract the Year from the Case Date"""
      if len(dat) > 1:
        yrs = re.findall('(?<= )\d{1,4}$', dat)
        return int(yrs[0])
      else:
        return 0

    def checkCase(self, citation, caseList, volumes):
      """ Find the case from the page of the citation (first page of the case)"""
      if citation in caseList:
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

    ### Develop visual Network graph
    ### use networkx
    def drawGraph(self):
         """Build a Network graph from the citations in a json-derived dictionary"""
         G=nx.Graph()
         cases = []
         vols = []
         cD = self.caseDict
         for i in xrange(575):
              vols.append([])
         print "Number of Cases: " + str(len(cD))
         #Iterate through cases to create Nodes and a volume dictionary to check cases against
         for case in cD:
              #nodeN= str(case['number'][0])
              c = case['number']
              cases.append(c)
              v = c[0] - 1
              vols[v].append(c[1])
              nodeN= str(c)
              yr = self.getYear(case['date'])
              G.add_node(nodeN, name=case['name'], url=self.baseURL+case['url'], vol=case['vol'], d=case['date'], year=yr)
         #print vols
         print cases
         for i in xrange(575):
              vols[i].sort()
         print "1st cases comp"
         #Iterate through cases to build edges (separate loop because of building the case list)
         #Set count for each citation to see if set lower
         sC, oC = 0, 0
         for case in cD:
              c = case['number']
              nodeN= str(c)
              for cite in case['citations']:
                   #print cite
                   if cite[0] > 0 and cite[0] < 576:
                        if cite != c:
                             x, checkedCite = self.checkCase(cite, cases, vols)
                             #print x
                             #print checkedCite
                             if x == 1:
                                  sC = 1 + sC
                             else:
                                  oC = 1 + oC
                             #sameCite = x + sameCite
                             targ = str(checkedCite)
                             G.add_edge(nodeN, targ)
              if oC % 300000 == 0 and oC != 0:
                   print "othC 300k"
         print str(sC)
         print "Percentage of samecitations " + str(float(sC)/float(sC+oC))
         if self.gml == 1 or self.gml == 2:
              nx.write_gml(G,'vis/'+self.outfile+'.gml')
              nx.write_gml(G,'vis/'+self.outfile+'.gml.gz')
         if self.gml != 1:
              d = json_graph.node_link_data(G)
              json.dump(d, open('vis/'+self.outfile+'.json','w'))
         #nx.draw(G)
         #plt.savefig("network.png")
