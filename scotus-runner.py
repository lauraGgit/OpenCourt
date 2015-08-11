# -*- coding: utf-8 -*-
import networkx as nx
from networkx.readwrite import json_graph
import argparse, json
#import matplotlib.pyplot as plt
from lib import helper, scrapers, grapher, citation_builders


baseURL = "https://supreme.justia.com"
#stopCase = 100
### Iterate through Volumes to get cases

def parseArgs():
  """Operated the CLI parameters"""
      parser = argparse.ArgumentParser()
      parser.add_argument("-s", "--vStart", help="The volume to start", type=int, default=1)
      parser.add_argument("-t", "--vStop", help="The volume to stop, if omitted will be start", type=int, default=1)
      parser.add_argument("-g", "--getcase", help="Pull the case files from the internet. true/false", default="False")
      parser.add_argument("-o", "--output", help="The outputfile", default="cases.json")
      parser.add_argument("-x", "--stopCase", help="Number of cases to run through per volume. If value is False then will run whole volume.", default="30")
      parser.add_argument("-i", "--input", help="Draw Graph from file", default="cases.json")
      parser.add_argument("-j", "--jsonOutput", help="Filename for the output of the graph json", default="graph.json")
      parser.add_argument("-e", "--emailsend", help="Send emails to mark progress", default="True")
      parser.add_argument("-m", "--gml", help="Encode the graph as gml. 0 = encode just json 1 = encode just gml 2= encode both", default="0")
      args = parser.parse_args()
      args.emailsend = False if args.emailsend != 'True' else True
      if args.gml == '2':
            args.gml = 2
      elif args.gml == '1':
            args.gml = 1
      else:
            args.gml = 0
      if (args.stopCase == "False"):
          args.stopCase = False
      else:
          args.stopCase = int(args.stopCase)
      return args

def main():
  """Main function to scaffold functions"""
     args = parseArgs()

     # See if scraping has been called
     if (args.getcase == "True"):
        scrape = scrapers.VolScraper(args.vStart, args.vStop, baseURL)
        caseUrls = scrape.scrapeVolumes()
          #check for case limit

        #Grab cases
        cScraper = scrapers.CaseScraper(args.stopCase, caseUrls, args.output, args.emailsend, baseURL)
        cases = cScraper.getCases()
        print cases
        print "Cases scraped"
     #or load from json
     else:
          with open(args.input, 'r') as fp:
               cases = json.load(fp)
               #print cases
               print "yeha! Json loaded"
          
     grapher.GraphBuilder(cases, args.jsonOutput, args.gml, baseURL).drawGraph()
     print "done"
     if args.emailsend:
          helper.emailSend('Your Script done', "ALL DONE")

if __name__ == "__main__":
   main()



