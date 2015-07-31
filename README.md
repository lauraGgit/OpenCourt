# OpenCourt

##Intro
This is a repo for a python scraper from Justia.com to build a corpus of U.S. Supreme Court Cases and then build a network graph from the citations. The motivation for this project was a recent Administrative Law School class and my discovery that there are no publically available machine readable versions of the Supreme Court Cases.

The output of this scraper can be used to generate a network graph visualization in D3 or using [Gephi](http://gephi.github.io/) visualization. The results, pending citation building refinements, will soon be posted!

While not scalable for the full corpus, the repo also includes some server-side D3.js rendering for the resulting graph json.

##The Scraper

The process has three major components:

1. Run through the specified range of Supreme Court Volumes to collect the case names and URLs from Justia.com

2. Scrape through all of the Case URLs generated in Step 1 to build a corpus of Supreme Court Cases.

3. Build a network graph file (in json or gml format) of the relationship of the cases based on their textual citations.

### Installing the scraper

Install the dependencies:

    pip install -r requirements.txt

Copy the sample_config.py into a config.py and add in the following to be able to email yourself notifications:

    server = 'smtp.emailserver.com'
    frm_addr = 'from_email_address@yourdomain.com'
    to_addr = ['to_email_address@yourdomain.com']
    user = 'user.for_email_acount'
    passw = 'email_password'


###Running the scraper CLI

####Running Step 1-3 Example - Scraping and Building the Graph

    python scotus-runner.py -s 1 -t 5 -x False -g True -o casestiny.json -j graphtiny.json -m 0

####Running Step 3 Example - Building the Graph

    python scotus-runner.py -i Downloaded/cases.json -x False -j graphtiny.json -m 1

####CLI Parameters

"-s", "--vStart": This is the SCOTUS volume to start scraping case names from. The default is 1 (FUN FACT: The early volumes were actually the Supreme Court of the Commonwealth of Pennslyvania and predate the United States)


"-t", "--vStop": This is the volume that the scraper will stop collecting case urls from. If ommitted it will default to 1.


"-g", "--getcase": Whether or not to actually scrape for the cases. If True, will run the Volume and Case scraper to build a corpus. If False, it will use a json file as specified by the input file parameter to load in cases and build out the network graph. Defaults to False.

"-o", "--output": The outputfile of the cases scraper. Default is cases.json

"-x", "--stopCase": The number of cases to run scrape after the volume scraper has collected the case URLS. If value is False then will scrape the text of all the cases urls collected in the volume scrape. If not False, the CLI expects an integer value. Default is 30.

"-i", "--input": If GetCase is false, the program will look for a json file to read in the cases from to build the network graph json or gml file. The default file is cases.json

"-j", "--jsonOutput" The filename for the output of the graph json. (Result of Step 3)The default is "graph.json."

"-e", "--emailsend": Because the scraper is timely and memory intensive and can be run remotely. This option allows you to send emails to mark progress". Default is true.

"-m", "--gml": Options to encode the graph as gml. 0 = encode just json 1 = encode just gml 2= encode both", default="0")
      