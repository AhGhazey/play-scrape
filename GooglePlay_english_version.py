import requests
import re
from optparse import OptionParser
from matplotlib.cbook import dedent
import json

def getGooglePlayReviews(id,page):


    data = {
        "reviewType": 0,
        "pageNum" :page,
        "id":id,
        "reviewSortOrder":4,
        "xhr": 1,        
        "hl":"en"
    }
    r = requests.post("https://play.google.com/store/getreviews?authuser=0",  data=data)
    revs = re.findall("(review-title)(.*?)(review-link)",r.text)
    stars = re.findall("Rated (.*?) stars out of five stars" ,r.text)
    x = []
    tmp = []
    [x.append(y) for (a,y,b) in revs]
    for i,rev in enumerate(x):
        tmp.append({"rating":int(stars[i]),"review":rev[25:-24].replace("span","")})
    print ("[*] Retrieved " + str(len(tmp)) + " reviews")
    return tmp

def getNPages(id,n):
    s = []
    [[s.append(x) for x in getGooglePlayReviews(id,i)] for i in range(n)]
    return s


def banner():
    banner = """
__________.__                   _________                                  
\______   \  | _____  ___.__.  /   _____/ ________________  ______   ____  
 |     ___/  | \__  \<   |  |  \_____  \_/ ___\_  __ \__  \ \____ \_/ __ \ 
 |    |   |  |__/ __ \\___  |  /        \  \___|  | \// __ \|  |_> >  ___/ 
 |____|   |____(____  / ____| /_______  /\___  >__|  (____  /   __/ \___  >
                    \/\/              \/     \/           \/|__|        \/ 
                    Author Ancarani Riccardo -- modified by Ahmed Ghazey"""
    print (banner)

def main():
    banner()
    parser = OptionParser(usage="usage: %prog [options] filename",
                          version="%prog 1.0")
    parser.add_option("-p", "--pages",
                      action="store", 
                      dest="pages",
                      default=20,
                      help="The number of pages you want to scrape",)
    parser.add_option("-i", "--id",
                      action="store", 
                      dest="app_id",
                      default="com.branch_international.branch.branch_demo_android",
                      help="The id of the app you want to scrape comments",)
    parser.add_option("-o", "--output",
                      action="store", 
                      dest="output",
                      default="output.json",
                      help="The output file where you want to dump results",)
    parser.add_option("-v", "--verbose",
                  action="store_false", dest="verbose", default=False,
                  help="Visualize the wordcloud associated with your results")
    (options, args) = parser.parse_args()
    print ("[*] Downloading the first " + str(options.pages) + " pages from: " + options.app_id)
    s = getNPages(options.app_id,int(options.pages))
    with open(options.output,"w+") as output_file:
        json.dump({"results": s},output_file)
    

if __name__ == '__main__':
    main()