# homework 4
# goal: ranked retrieval, PageRank, crawling
# exports:
#   student - a populated and instantiated cs525.Student object
#   PageRankIndex - a class which encapsulates the necessary logic for
#     indexing and searching a corpus of text documents and providing a
#     ranked result set

# ########################################
# first, create a student object
# ########################################

import cs525
MY_NAME = "Fangling Zhang"
MY_ANUM  = 708310359 # put your UID here
MY_EMAIL = "fzhang2@wpi.edu"
import numpy as np

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = []

# Set the I_AGREE_HONOR_CODE to True if you agree with the following statement
# "An Aggie does not lie, cheat or steal, or tolerate those who do."
I_AGREE_HONOR_CODE = True

# this defines the student object
student = cs525.Student(
    MY_NAME,
    MY_ANUM,
    MY_EMAIL,
    COLLABORATORS,
    I_AGREE_HONOR_CODE
    )


# ########################################
# now, write some code
# ########################################

import bs4 as BeautifulSoup  # you will want this for parsing html documents
import urllib.request
from urllib.parse import urljoin
import numpy as np
import re

# our index class definition will hold all logic necessary to create and search
# an index created from a web directory
#
# NOTE - if you would like to subclass your original Index class from homework
# 1 or 2, feel free, but it's not required.  The grading criteria will be to
# call the index_url(...) and ranked_search(...) functions and to examine their
# output.  The index_url(...) function will also be examined to ensure you are
# building the index sanely.

class PageRankIndex(object):
    def __init__(self):
        # you'll want to create something here to hold your index, and other
        # necessary data members
        self.index={}
        self.link_matrix=[]
        self.pages=[]
    # index_url( url )
    # purpose: crawl through a web directory of html files and generate an
    #   index of the contents
    # preconditions: none
    # returns: num of documents indexed
    # hint: use BeautifulSoup and urllib
    # parameters:
    #   url - a string containing a url to begin indexing at
    def index_url(self, url):
        # ADD CODE HERE        
        lis=[]
        c0=urllib.request.urlopen(url)
        soup0=BeautifulSoup.BeautifulSoup(c0.read(),"html.parser")
        links0=soup0.find_all('a')
        for link0 in links0:
            if 'href' in link0.attrs:                 
                lis.append(link0['href'])
                newurl=urljoin(url,link0['href']) 
                self.pages.append(newurl)
        self.pages.append(url)
        n=len(self.pages)
        self.link_matrix=np.zeros((n,n))
        self.link_matrix[:,-1]=1  #the root node
        num_files=0
        for j,page in enumerate(self.pages[:-1]):
            try:
              c=urllib.request.urlopen(page)
            except:
              print ("Could not open %s" % page)
              continue
            try:
              soup=BeautifulSoup.BeautifulSoup(c.read(),"html.parser")                
              text=soup.get_text()
              tokens=self.tokenize(text)
              if tokens:
                  num_files+=1
                  for term in set(tokens):
                      if term in self.index:
                          self.index[term].append(page)
                      else:
                          self.index[term]=[page]
              links=soup.find_all('a')
              for link in links:
                  if 'href' in link.attrs:
                    k=lis.index(link['href'])
                    self.link_matrix[k,j]=1  
            except:
              print ("Could not parse page %s" % page)
        return num_files
        


    # tokenize( text )
    # purpose: convert a string of terms into a list of terms 
    # preconditions: none
    # returns: list of terms contained within the text
    # parameters:
    #   text - a string of terms
    def tokenize(self, text):
        tokens = []
        pattern = r'\W+|_'
        words=re.split(pattern, text)
        tokens=[w.lower() for w in words]
        return tokens
    # ranked_search( text )
    # purpose: searches for the terms in "text" in our index and returns
    #   AND results for highest 10 ranked results
    # preconditions: .index_url(...) has been called on our corpus
    # returns: list of tuples of (url,PageRank) containing relevant
    #   search results
    # parameters:
    #   text - a string of query terms
    def ranked_search(self, text):
        n=len(self.link_matrix)
        for i in range(n):
            self.link_matrix[i,:]=self.link_matrix[i,:]/sum(self.link_matrix[i,:]) 
        teleport_matrix=np.ones((n,n))/n
        p=0.9*self.link_matrix+0.1*teleport_matrix
        vec=[1/n]*n
        dif=1
        while dif>10**(-n):
            vec1=np.dot(vec,p)
            dif = sum(map(lambda x: (x[0]-x[1])**2, zip(vec1, vec)))
            vec=vec1
            #print(vec)
        score_dic={}
        for i in range(n):
            score_dic[self.pages[i]]=vec[i]
            
        qs=self.tokenize(text)
        pages=self.index[qs[0]]
        if len(qs)>1:
            for i in range(1,len(qs)):
                pages=set(pages)&set(self.index[qs[i]]) 
        results=[]
        for page in pages:
            results.append((page,score_dic[page]))
        return sorted(results,key=lambda d:d[1],reverse=True)[:10]


# now, we'll define our main function which actually starts the indexer and
# does a few queries
def main(args):
    print(student)
    index = PageRankIndex()
    url = 'http://web.cs.wpi.edu/~kmlee/cs525/new10/index.html'
    num_files = index.index_url(url)
    search_queries = (
       'palatial', 'college ', 'palatial college', 'college supermarket', 'famous aggie supermarket'
        )
    for q in search_queries:
        results = index.ranked_search(q)
        print("searching: %s -- results: %s" % (q, results))


# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

