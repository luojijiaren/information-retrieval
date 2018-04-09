# homework 4
# goal: k-means clustering on vectors of TF-IDF values,
#   normalized for every document.
# exports: 
#   student - a populated and instantiated cs525.Student object
#   Clustering - a class which encapsulates the necessary logic for
#       clustering a set of documents by tf-idf 


# ########################################
# first, create a student object
# ########################################

import cs525
MY_NAME = "Fangling Zhang"
MY_ANUM  = 708310359 # put your UID here
MY_EMAIL = "fzhang2@wpi.edu"

# the COLLABORATORS list contains tuples of 2 items, the name of the helper
# and their contribution to your homework
COLLABORATORS = [ 
    ]

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
import os
import re
import collections
import random
import numpy as np
from pandas import DataFrame
# Our Clustering object will contain all logic necessary to crawl a local
# directory of text files, tokenize them, calculate tf-idf vectors on their
# contents then cluster them according to k-means. The Clustering class should
# select r random restarts to ensure getting good clusters and then use RSS, an
# internal metric, to calculate best clusters.  The details are left to the
# student.

class Clustering(object):
    # hint: create something here to hold your dictionary and tf-idf for every
    #   term in every document
    def __init__(self):
        pass       

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

    # consume_dir( path, k )
    # purpose: accept a path to a directory of files which need to be clustered
    # preconditions: none
    # returns: list of documents, clustered into k clusters
    #   structured as follows:
    #   [
    #       [ first, cluster, of, docs, ],
    #       [ second, cluster, of, docs, ],
    #       ...
    #   ]
    #   each cluster list above should contain the document name WITHOUT the
    #   preceding path.  JUST The Filename.
    # parameters:
    #   path - string path to directory of documents to cluster
    #   k - number of clusters to generate
    def consume_dir(self, path, k):
        documents=os.listdir(path)
        #calculate tf-idf vectors of each document
        d={} #dictionary (document name: tokens)
        allTerms=[]
        docTfIdf=collections.OrderedDict() 
        for doc in documents:
            with open(path+doc,'r',encoding='utf-8') as f:
                strings=f.read().strip()
                tokens=self.tokenize(strings)
                d[doc]=tokens
                allTerms.extend(tokens)
        dfDic=collections.Counter(allTerms)
        for doc in d:
            tfDic=collections.Counter(d[doc])
            lis=[]
            for term in dfDic:
                lis.append(tfDic.get(term,0)/dfDic[term])
            docTfIdf[doc]=lis
        #K-mean
        
        #initiate
        vecs=list(docTfIdf.values())
        r=30
        restart=0
        bestRSS=float('inf')
        bestCats=collections.defaultdict(list)
        while restart<r:
        
            centers=random.sample(vecs,k)
            while True:
                #send documents to its nearest center using Euclidean distance
                cats=collections.defaultdict(list)
                for i,vec in enumerate(vecs):
                    cat=np.argmin([sum((np.array(vec)-np.array(c))**2)**0.5 for c in centers])
                    cats[cat].append(i)
                #recalculate the centers
                newCenters=[]
                for cat in cats:
                    arrList=[vecs[i] for i in cats[cat]]
                    newCenters.append(list((DataFrame(arrList).mean())))
                dif=abs((np.array(newCenters)-np.array(centers)).sum())
                #print(dif)
                if dif<1e-5:
                    break
                else:
                    centers=newCenters
            #calculate the RSS
            RSS=0
            for cat,center in enumerate(newCenters):
                for i in cats[cat]:
                    RSS+=sum((np.array(vecs[i])-np.array(center))**2)
            #record better clustering      
            if RSS<bestRSS:
                bestRSS=RSS
                #r=restart
                bestCats=cats
            #print('current best RSS: ', bestRSS)
            restart+=1
            #if bestRSS does change after restarting more than 30 times, end
            #if restart-r>30:
            #    print(restart)
            #    break
        res=[]
        for i in bestCats.values():
            res.append([list(docTfIdf.keys())[k] for k in i])
                
        return res


# now, we'll define our main function which actually starts the clusterer
def main(args):
    print(student)
    clustering = Clustering()
    print("test 10 documents")
    print(clustering.consume_dir('test10/', 5))
    print("test 50 documents")
    print(clustering.consume_dir('test50/', 5))

# this little helper will call main() if this file is executed from the command
# line but not call main() if this file is included as a module
if __name__ == "__main__":
    import sys
    main(sys.argv)

