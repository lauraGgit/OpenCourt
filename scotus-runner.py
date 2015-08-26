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
      """Pulling and cleaning the CLI parameters"""
      parser = argparse.ArgumentParser()
      parser.add_argument("-p", "--phase", help="Start With 1 - scrape, 2 - citation building, 3- graph building. Default 2.", type=int, default=2)
      parser.add_argument("-s", "--vStart", help="The volume to start", type=int, default=1)
      parser.add_argument("-t", "--vStop", help="The volume to stop, if omitted will be start", type=int, default=1)
      parser.add_argument("-o", "--output", help="The outputfile", default="cases.json")
      parser.add_argument("-x", "--stopCase", help="Number of cases to run through per volume. If value is False then will run whole volume.", default=30)
      parser.add_argument("-i", "--input", help="Draw Graph from file", default="cases.json")
      parser.add_argument("-c", "--citeOutput", help="Output for the citation step", default="cites")
      parser.add_argument("-g", "--graphOutput", help="Graph output prifix for gml and json", default="graph")
      parser.add_argument("-e", "--emailsend", help="Send emails to mark progress", default=True)
      parser.add_argument("-f", "--format", help="File formats for graph output. 0 = .json only 1 = .gml only 2= output .json and .gml", type=int, default=0)
      args = parser.parse_args()
      args.emailsend = False if args.emailsend != True else True
      if args.format == 2 or args.format == 1:
            args.form = args.format
      else:
            args.format = 0
      if (args.stopCase == "False"):
          args.stopCase = False
      else:
          args.stopCase = int(args.stopCase)
      return args

def main():
     """Main function to scaffold functions"""
     args = parseArgs()

     # See if scraping has been called
     if (args.phase == 1):
        scrape = scrapers.VolScraper(args.vStart, args.vStop, baseURL)
        caseUrls = scrape.scrapeVolumes()

        #Grab cases
        cScraper = scrapers.CaseScraper(args.stopCase, caseUrls, args.output, args.emailsend, baseURL)
        cases = cScraper.getCases()
        print "Cases scraped"
     #or load from json
     else:
          try:
               with open(args.input, 'r') as fp:
                    cases = json.load(fp)
                    #print cases
                    print "yeha! Json loaded"
          except EnvironmentError:
               print "Select select a valid load file."
     if (args.phase < 3):
          CB = citation_builders.citations(cases, args.citeOutput)
          cites, metrics = CB.processText(True)
          #print cites
          print metrics
     else:
          cites = cases
          
     grapher.GraphBuilder(cites, args.graphOutput, args.format, baseURL).drawGraph()
     print "done"
     if args.emailsend:
          helper.emailSend('Your Script done', "ALL DONE")

if __name__ == "__main__":
   main()
