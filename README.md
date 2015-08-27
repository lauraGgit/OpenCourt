# OpenCourt

##Intro
This is a repo for a the [OpenCourt Project](lgerhardt.com/OpenCourtSite) python scraper from Justia.com to build a corpus of U.S. Supreme Court Cases and then build a network graph from the citations. The motivation for this project was a recent Administrative Law School class and my discovery that there are no publically available machine readable versions of the Supreme Court Cases.

The output of this scraper can be used to generate a network graph visualization in D3 or using [Gephi](http://gephi.github.io/) visualization. The results, pending citation building refinements, will soon be posted!

While not scalable for the full corpus, the repo also includes some server-side D3.js rendering for the resulting graph json.

##The Scraper

The process has three major components separated into modules in the `lib` directory:

1. `scrapers` Run through the specified range of Supreme Court Volumes to collect the case names and URLs from Justia.com. Then Scrape through all of the Case URLs generated in Step 1 to build a corpus of Supreme Court Cases.

2. `citation_builder` Scrape through all of the case text to develop a list of citations for each case.

3. `grapher` Build a network graph file (in json or gml format) of the relationship of the cases based on their textual citations.

### Installing the scraper

Install the dependencies:

    pip install -r requirements.txt

Copy the `sample_config.py` into a config.py and add in the following to be able to email yourself notifications:

    server = 'smtp.emailserver.com'
    frm_addr = 'from_email_address@yourdomain.com'
    to_addr = ['to_email_address@yourdomain.com']
    user = 'user.for_email_acount'
    passw = 'email_password'

Make the `vis` directory for the output of the graph.json

    mkdir vis

###Running the scraper CLI

####Running Step 1-3 Example - Scraping and Building the Graph

    python scotus-runner.py -p 1 -s 1 -t 5 -x False -o cases -g graph_08_15 -f 0

It can be helpful to run the scraper in the background using nohup, as the process on a single core takes upwards of 11 hours. There is no explicit logging in the code but the following command will rewrite out the standard out, errors, and cases.json to a log file.

    nohup python scotus-runner.py parms &> log.txt

####Running Step 3 Example - Building the Graph and output files in both json and gml

    python scotus-runner.py -p 3 -i preScrapedcases.json -g graphtiny -f 2 -e False

####CLI Parameters

`"-p", "--phase`": What Phase of the Program to begin at. This corresponds to the major components listed above. The options include 1.) Running the whole program (Scrape, Citation, Graph) 2.) Start at the citation building 3.) Just graph.

`"-s", "--vStart"`: This is the SCOTUS volume to start scraping case names from. The default is 1 (FUN FACT: The early volumes were actually the Supreme Court of the Commonwealth of Pennslyvania and predate the United States)


`"-t", "--vStop"`: This is the volume that the scraper will stop collecting case urls from. If ommitted it will default to 1.

`"-o", "--output"`: The outputfile of the cases scraper. Default is cases.json

`"-x", "--stopCase"`: The number of cases to run scrape after the volume scraper has collected the case URLS. If value is False then will scrape the text of all the cases urls collected in the volume scrape. If not False, the CLI expects an integer value. Default is 30.

`"-i", "--input"`: If GetCase is false, the program will look for a json file to read in the cases from to build the network graph json or gml file. The default file is cases

`"-g", "--graphOutput"`: The filename for the graph output files. This will be the prefix for both the json and the gml file. "graph"+extension

`"-e", "--emailsend"`: Because the scraper is timely and memory intensive and can be run remotely. This option allows you to send emails to mark progress". Default is true.

`"-f", "--format"`: File format Output options for the grapher class. 0 = .json only 1 = .gml only 2= output .json and .gml. The program defaults to only JSON.
      
