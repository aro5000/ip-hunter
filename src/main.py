##########################################################################
# IP-HUNTER                                                              #
#                                                                        #
# This tool will query various DNS servers in hopes of getting all IP's  #
# a particular domain resolves to.                                       #
#                                                                        #
# Made by: Aaron Stults                                                  #
##########################################################################

# Imports
import argparse
from multiprocessing import Pool
import time


def processor(resolver):

    # Set up searcher object
    from searcher import Searcher
    searcher = Searcher(args.target)

    if resolver == 'google':
        try:
            searcher.googledns()
        except Exception as e:
            print(e)
            print('[!] Failure querying Google DNS')

    elif resolver == 'cloudflare':
        try:
            searcher.cloudflaredns()
        except Exception as e:
            print(e)
            print('[!] Failure querying Cloudflare DNS')

    elif resolver == 'local':
        try:
            searcher.localresolver()
        except Exception as e:
            print(e)
            print('[!] Failure querying local DNS')

    return searcher.results


if __name__ == "__main__":
    # Start a timer for benchmarking
    start = time.time()

    # Set up argparser to get which type of query to run
    parser = argparse.ArgumentParser()
    parser.add_argument("target", help="Enter the domain or subdomain you want to query")
    args = parser.parse_args()

    finalresults = []
    strbuilder = "[+] IP's found for " + args.target + ": "

    with Pool(3) as p:
        results = p.map(processor, ['google', 'cloudflare', 'local'])
    for i in results:
        for o in i:
            finalresults.append(o)

    # Remove duplicates
    finalresults = list(set(finalresults))

    if len(finalresults) < 1:
        strbuilder = '[!] There were no results found for: ' + args.target
    else:
        for i in finalresults:
            if finalresults.index(i) < (len(finalresults) - 1):
                strbuilder += i + " | "
            else:
                strbuilder += i

    print(strbuilder)

    end = time.time()
    #print('[+] Time taken: ' + str(end-start))
