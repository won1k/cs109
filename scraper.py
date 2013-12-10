import urllib
import urllib2 
from bs4 import BeautifulSoup
import html2text
import json
import ast
import requests
import os
import numpy as np

LIST_OF_GENRES = ["Action & Adventure","Animation",
"Art House & International","Classics","Comedy","Cult Movies",
"Documentary","Drama","Horror","Kids & Family",
"Musical & Performing Arts","Mystery & Suspense","Romance",
"Science Fiction & Fantasy","Special Interest","Television","Western"]


def scrape_daily_script(Request,urlopen,imdb_num_list):
    listOfUrls = ['http://www.dailyscript.com/movie.html', 'http://www.dailyscript.com/movie_n-z.html']
    homepage = "http://www.dailyscript.com/"

    imdbNumDict = {}

    for each_page in listOfUrls:
        theurl = each_page
        txdata = None                                                                           # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
        txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}          # fake a user agent, some websites (like google) don't like automated exploration

        try:
            req = Request(theurl, txdata, txheaders)            # create a request object
            handle = urlopen(req)                               # and open it to return a handle on the url
        except IOError, e:
            print 'We failed to open "%s".' % theurl
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code

        sHTML = handle.read()
        sHTML = sHTML.replace('ISO-8859-1', 'utf-8')
        soup = BeautifulSoup(sHTML, "html5lib")
        movieLinks = soup.find_all("p")
        for elem in movieLinks:
            if "scripts" in str(elem):
                links = elem.find_all("a")
                for link in links:
                    if "scripts" in str(link):
                        scriptlink =  homepage + link['href']
                        title = link.get_text()
                        title = title.replace("/","-")
                    if "imdb" in str(link):
                        imdb_link = link['href']
                        #grab the imdb number from the link
                        imdbNum = imdb_link[-imdb_link[::-1].find("?"):]
        
                #doctype (e.g. pdf, html, txt) is gonna be grabbed as the 
                #letters after the LAST period in the link to the script
                doctype = scriptlink[-scriptlink[::-1].find("."):]
                doctype = doctype.lower()

                if doctype <> "pdf" and doctype <> "doc" and len(imdbNum) > 1:
                    try:
                        if imdbNum not in imdbNumDict.keys():
                            imdbNumDict[imdbNum] = "1"
                            req = Request(scriptlink, txdata, txheaders)
                            handle = urlopen(req)
                            sHTML_script = handle.read()
                            if doctype == "html" or doctype == "htm":
                                 sHTML_script = html2text.html2text(sHTML_script)
                                 doctype = "txt"
                            
                            if len(sHTML_script) > 10000:
                                if title.encode('ascii', 'replace') == title:
                                    f = open("output/" + imdbNum + "." + doctype, 'w')
                                    f.write(sHTML_script)
                                    f.close()
                                    imdb_num_list.append(imdbNum)
                                    print imdbNum
                    except:
                        pass
    return imdb_num_list


def scrape_simply_scripts(Request,urlopen,imdb_num_list):
    listOfUrls = ['http://www.simplyscripts.com/num.html', 
                  'http://www.simplyscripts.com/a.html',
                  'http://www.simplyscripts.com/b.html',
                  'http://www.simplyscripts.com/c.html',
                  'http://www.simplyscripts.com/d.html',
                  'http://www.simplyscripts.com/e.html',
                  'http://www.simplyscripts.com/f.html',
                  'http://www.simplyscripts.com/g.html',
                  'http://www.simplyscripts.com/h.html',
                  'http://www.simplyscripts.com/i.html',
                  'http://www.simplyscripts.com/j.html',
                  'http://www.simplyscripts.com/k.html',
                  'http://www.simplyscripts.com/l.html',
                  'http://www.simplyscripts.com/m.html',
                  'http://www.simplyscripts.com/n.html',
                  'http://www.simplyscripts.com/o.html',
                  'http://www.simplyscripts.com/p.html',
                  'http://www.simplyscripts.com/q.html',
                  'http://www.simplyscripts.com/r.html',
                  'http://www.simplyscripts.com/s.html',
                  'http://www.simplyscripts.com/t.html',
                  'http://www.simplyscripts.com/uvw.html',
                  'http://www.simplyscripts.com/xyz.html']
                  
    imdbNumDict = {}

    for each_page in listOfUrls:
        print each_page
        theurl = each_page
        txdata = None                                                                           # if we were making a POST type request, we could encode a dictionary of values here - using urllib.urlencode
        txheaders =  {'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}          # fake a user agent, some websites (like google) don't like automated exploration

        try:
            req = Request(theurl, txdata, txheaders)            # create a request object
            handle = urlopen(req)                               # and open it to return a handle on the url
        except IOError, e:
            print 'We failed to open "%s".' % theurl
            if hasattr(e, 'code'):
                print 'We failed with error code - %s.' % e.code

        sHTML = handle.read()
        sHTML = sHTML.replace('ISO-8859-1', 'utf-8')
        soup = BeautifulSoup(sHTML, "html5lib")
        movieLinks = soup.find_all("tr")
        
        for movie in movieLinks:
            imdbNum = ""
            if ("imdb" in str(movie) and "dailyscript" not in str(movie) 
                and ("in html format" in str(movie) or "in text format" 
                in str(movie))):
                
                links = movie.find_all("a")
                script_link = links[0]['href']
                for link in links:
                    if "imdb" in str(link):
                        sLink = link['href']
                        imdbNum = sLink[sLink.find("?")+1:]
                        
                #~ #doctype (e.g. pdf, html, txt) is gonna be grabbed as the 
                #~ #letters after the LAST period in the link to the script
                doctype = script_link[-script_link[::-1].find("."):]
                doctype = doctype.lower()
    
                if len(imdbNum) > 1 and imdbNum.isdigit(): #only grab scripts with valid IMDB numbers
                    try:
                        if imdbNum not in imdbNumDict.keys():
                            imdbNumDict[imdbNum] = "1"
                            req = Request(script_link, txdata, txheaders)
                            handle = urlopen(req)
                            sHTML_script = handle.read()
                            if "htm" in doctype:
                                 sHTML_script = html2text.html2text(sHTML_script)
                                 doctype = "txt"
                            if len(sHTML_script) > 10000:
                                
                                f = open("output/" + imdbNum + "." + doctype, 'w')
                                f.write(sHTML_script)
                                f.close()
                                imdb_num_list.append(imdbNum)
                                print imdbNum
                    except:
                        pass
    return imdb_num_list
    
def grab_rotten_tomatoes_info(dataList, datafile,box_office_dict,academy_award_dict):
    for elem in dataList:
        api_key = '6mhbr2qxeswq3znchkshxtta'
        imdb_id = elem  
        url = "http://api.rottentomatoes.com/api/public/v1.0/movie_alias.json?id=%s&type=imdb&apikey=%s" % (imdb_id,  api_key)
        data = requests.get(url).text
        data = json.loads(data)  # load a json string into a collection of lists and dicts
        if imdb_id <> "0000000" and os.path.getsize('output/'+str(imdb_id)+'.txt')>35000: #if script is less than 35kb, disregard it
            try:
                rt_id = json.dumps(data['id'])  
                genres = json.dumps(data['genres']).replace("[","").replace("]","").replace(chr(34),"").split(", ")
                ratings = data['ratings']
                ratingslist = []
                critics_score = ""
                critics_rating = ""
                audience_rating = ""
                audience_score = ""
                if "critics_score" in ratings.keys():
                    critics_score = str(ratings["critics_score"])
                if "critics_rating" in ratings.keys():
                    critics_rating = str(ratings["critics_rating"])
                if "audience_rating" in ratings.keys():
                    audience_rating = str(ratings["audience_rating"])
                if "audience_score" in ratings.keys():
                    audience_score = str(ratings["audience_score"])
                MPAA_Rating = json.dumps(data['mpaa_rating'])
                runtime = json.dumps(data['runtime']) 
                year = json.dumps(data['year']) 
                title = json.dumps(data['title'])
                characters = data['abridged_cast']
                datafile.write(imdb_id +  chr(9))
                datafile.write(rt_id  + chr(9))
                datafile.write(title + chr(9))
                for elem in LIST_OF_GENRES:
                    if elem in genres:
                        datafile.write("1" + chr(9))
                    else:
                        datafile.write("0" + chr(9))
                datafile.write(critics_score + chr(9))
                datafile.write(audience_score + chr(9))
                datafile.write(audience_rating + chr(9))
                datafile.write(critics_rating + chr(9))
                datafile.write(str(runtime) + chr(9))
                datafile.write(str(year) + chr(9))
                datafile.write(MPAA_Rating + chr(9))
                for i in range(5):
                    if i+1 > len(characters):
                        datafile.write("" + chr(9) + "" + chr(9))
                    else:
                        if "name" in characters[i].keys():
                            datafile.write(characters[i]["name"] + chr(9))
                        else:
                            datafile.write("" + chr(9))
                        if "characters" in characters[i].keys():
                            datafile.write(characters[i]["characters"][0] + chr(9))
                        else:
                            datafile.write("" + chr(9))
                if imdb_id in box_office_dict.keys():
                    datafile.write(box_office_dict[imdb_id][0] + chr(9))
                    datafile.write(box_office_dict[imdb_id][1] + chr(9))
                else:
                    datafile.write("" + chr(9))
                    datafile.write("" + chr(9))
                if imdb_id in academy_award_dict.keys():
                    datafile.write(academy_award_dict[imdb_id][0] + chr(9))
                    datafile.write(academy_award_dict[imdb_id][1] + chr(9))
                else:
                    datafile.write("" + chr(9))
                    datafile.write("" + chr(9))
                datafile.write("\n")
            except:
                pass    

#import box office info and put into dictionary
box_office_info = np.genfromtxt("boxoffice.csv", delimiter='\t', dtype=str,skip_header=1)
box_office_dict = {}
for elem in box_office_info:
    box_office_dict[elem[0]] = [elem[1],elem[2]]

#import academy award info and put into dictionary
academy_award_info = np.genfromtxt("OscarInfo.csv", delimiter='\t', dtype=str,skip_header=1)
academy_award_dict = {}
for elem in academy_award_info:
    academy_award_dict[elem[0]] = [elem[1],elem[2]]


imdb_num_list = []
datafile = open('MasterList.csv','w')
datafile.write("IMDB ID" + chr(9) + "Rotten Tomatoes ID" + chr(9) + 
                "Title" + chr(9))
for elem in LIST_OF_GENRES:
    datafile.write(elem + chr(9))
    
datafile.write("Critics Score" + chr(9) + "Audience Score" + chr(9) + 
    "Audience Rating" + chr(9) + "Critics Rating" + chr(9) + "runtime" + 
    chr(9) + "year" + chr(9) + "mpaa_rating" + chr(9)+ "actor1" + chr(9)
    + "character1" + chr(9) + "actor2" + chr(9) + "character2" + chr(9) 
    + "actor3" + chr(9) + "character3" + chr(9)
    + "actor4" + chr(9) + "character4" + chr(9)
    + "actor5" + chr(9) + "character5" + chr(9)
    + "Budget" + chr(9) + "Gross" + chr(9) + "Oscar Wins" 
    + chr(9) + "Oscar Nominations" + "\n")
    
urlopen = urllib2.urlopen
Request = urllib2.Request
imdb_num_list = scrape_daily_script(Request,urlopen,imdb_num_list)
imdb_num_list = scrape_simply_scripts(Request,urlopen,imdb_num_list)

imdb_num_list = list(set(imdb_num_list)) #remove any duplicates

grab_rotten_tomatoes_info(imdb_num_list,datafile,box_office_dict, academy_award_dict)

datafile.close()
