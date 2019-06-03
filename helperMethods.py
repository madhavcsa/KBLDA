# -*- coding: utf-8 -*-
#!usr/bin/env python

import VALS
import sys
import numpy as np
import os
from random import randint

def readDocs(NPFile,VPFile):
    try:
        id = 0
        with open(NPFile) as fp:
            for line in fp:                    
                temp = line.split(",")
                if temp[0] not in VALS.dictDoc2ID:
                    VALS.dictDoc2ID[temp[0]]=id
                    VALS.dictID2Doc[id] = temp[0]
                    VALS.docNP[id] = []
                    VALS.docVP[id] = []
                    if temp[1] in VALS.dictNP2ID:
                        for i in range(0,int(temp[2])):
                            VALS.docNP[id].append(VALS.dictNP2ID[temp[1]])
                    id = id + 1
                else:
                    if temp[1] in VALS.dictNP2ID:
                        for i in range(0,int(temp[2])):
                            VALS.docNP[VALS.dictDoc2ID[temp[0]]].append(VALS.dictNP2ID[temp[1]])
        VALS.M = id
                                
        
    except IOError:
        print ("Error reading NP file")
        sys.exit()
        
    try:        
        id = VALS.M
        with open(VPFile) as fp:
            for line in fp:
                temp = line.split(",")
                if temp[0] in VALS.dictDoc2ID:
                    #VALS.dictDoc2ID[temp[0]]=id
                    #VALS.dictID2Doc[id] = temp[0]
                    if temp[0] not in VALS.docVP:
                        VALS.docVP[VALS.dictDoc2ID[temp[0]]] = []
                    if temp[1] in VALS.dictVP2ID:
                        for i in range(0,int(temp[2])):
                            VALS.docVP[VALS.dictDoc2ID[temp[0]]].append(VALS.dictVP2ID[temp[1]])  
                else:
                    VALS.dictDoc2ID[temp[0]]=id
                    VALS.dictID2Doc[id] = temp[0]
                    VALS.docVP[id] = []
                    VALS.docNP[id] = []
                    if temp[1] in VALS.dictVP2ID:
                        for i in range(0,int(temp[2])):
                            VALS.docVP[id].append(VALS.dictVP2ID[temp[1]])
                    id = id + 1
        VALS.M = id
                    
    except IOError:
        print ("Error reading VP file")
        sys.exit()
    
    
    
def readCIFile(CIFile):
    try:
        id =0
        CI_id = 0
        with open(CIFile) as fp:
            for line in fp:
                temp = line.split(",")
                if temp[1] not in VALS.dictNP2ID:
                    VALS.dictNP2ID[temp[1]]=id
                    VALS.dictID2NP[id] = temp[1]
                    id = id+1
                if temp[2] not in VALS.dictNP2ID:
                    VALS.dictNP2ID[temp[2]] = id
                    VALS.dictID2NP[id]=temp[2]
                    id=id+1
                pair = temp[1]+","+temp[2]
                if pair not in VALS.CIdict:
                    VALS.CIdict[pair]=temp[3]
                    VALS.dictCI2ID[pair] = CI_id
                    VALS.dictID2CI[CI_id] = pair
                    CI_id += 1
        VALS.CI = CI_id
        VALS.n_NP = len(VALS.dictID2NP)
    except IOError:
        print("Error reading CIFile")
        sys.exit()
        
def readTriplesFile(TriplesFile):
    try:
        id =0
        T_id = 0
        with open(TriplesFile) as fp:
            for line in fp:
                temp = line.split(",")
                if temp[2] not in VALS.dictVP2ID:
                    VALS.dictVP2ID[temp[2]] = id
                    VALS.dictID2VP[id]=temp[2]
                    id = id + 1
                VALS.Triplesdict[temp[1]+","+temp[2]+","+temp[3]] = temp[4]
                VALS.dictTrp2ID[temp[1]+","+temp[2]+","+temp[3]] = T_id
                VALS.dictID2Trp[T_id] =temp[1]+","+temp[2]+","+temp[3]
                T_id += 1
        VALS.T = T_id
        VALS.n_VP = len(VALS.dictID2VP)
    except IOError:
        print("Error reading Triples File")
        sys.exit()
        
def initializeCounts():
    VALS.n_NPK =  np.zeros([len(VALS.dictID2NP),VALS.K],dtype=float)
    VALS.n_VPK = np.zeros([len(VALS.dictID2VP),VALS.K],dtype=float)
    VALS.n_docK = np.zeros([VALS.M,VALS.K],dtype=float)
    VALS.n_CIK = np.zeros([len(VALS.dictCI2ID),VALS.K,VALS.K],dtype=float)
    VALS.n_TK = {}
    VALS.n_NPK_sum = np.zeros(VALS.K)
    VALS.n_VPK_sum = np.zeros(VALS.K)
    
def initializeTopicAssignments():
    ## IDs for topic pairs    
    id=0
    for i in range(0,VALS.K):
        for j in range(0,VALS.K):
            VALS.dictID2TopicPair[id] = str(i)+","+str(j)
            id += 1
    ## Initialize with a random topic for CI pairs
    for i in range(0,VALS.CI):
        topic = randint(0,VALS.K*VALS.K-1)         
        VALS.z_CI[i] = topic
        Tpair = VALS.dictID2TopicPair[topic]
        Tpair = Tpair.split(",")
        VALS.n_CIK[i][int(Tpair[0])][int(Tpair[1])] += 1
        ## Increment counts for corresponding NPs
        CI_Pair = VALS.dictID2CI[i]
        CI_Pair = CI_Pair.split(",")
        VALS.n_NPK[VALS.dictNP2ID[CI_Pair[0]],int(Tpair[0])] += 1
        VALS.n_NPK[VALS.dictNP2ID[CI_Pair[1]],int(Tpair[1])] += 1
        VALS.n_NPK_sum[int(Tpair[0])] += 1
        VALS.n_NPK_sum[int(Tpair[1])] += 1
            
    ## IDs for Topic Triples
    id = 0
    for i in range(0,VALS.K):
        for j in range(0,VALS.K):
            for k in range(0,VALS.K):
                VALS.dictID2TopicTriple[id] = str(i)+","+str(j)+","+str(k)
                id += 1
                
    ## Initialize with a random topic for Triples
    for i in range(0,VALS.T):
        topic = randint(0,VALS.K*VALS.K*VALS.K-1)
        VALS.z_Trp[i] = topic
        Ttriple = VALS.dictID2TopicTriple[topic]
        Ttriple = Ttriple.split(",")
        # VALS.n_TK[i][int(Ttriple[0])][int(Ttriple[1])][int(Ttriple[2])] += 1
        temp={}
        temp[topic]=1
        VALS.n_TK[i]=temp
        ## Increment counts for corresponding NPs and VPs
        Trp_Triple = VALS.dictID2Trp[i]
        Trp_Triple = Trp_Triple.split(",")
        VALS.n_NPK[VALS.dictNP2ID[Trp_Triple[0]]][int(Ttriple[0])] += 1
        VALS.n_VPK[VALS.dictVP2ID[Trp_Triple[1]]][int(Ttriple[1])] += 1
        VALS.n_NPK[VALS.dictNP2ID[Trp_Triple[2]]][int(Ttriple[2])] += 1
        VALS.n_NPK_sum[int(Ttriple[0])] += 1
        VALS.n_NPK_sum[int(Ttriple[2])] += 1
        
        
    ## Initialize Doc NP topic assignments
    for i in range(0,VALS.M):
        tempNP = VALS.docNP[i]
        VALS.zDocNP[i]=[]
        for j in range(0,len(tempNP)):
            topic = randint(0,VALS.K-1)
            VALS.zDocNP[i].append(topic)
            VALS.n_NPK[int(tempNP[j])][topic] += 1
            VALS.n_NPK_sum[topic] += 1
            VALS.n_docK[i][topic] += 1
            
    ## Initialize Doc VP topic assignments
    for i in range(0,VALS.M):
        tempVP = VALS.docVP[i]
        VALS.zDocVP[i]=[]
        for j in range(0,len(tempVP)):
            randint(0,VALS.K)
            topic = randint(0,VALS.K-1)
            VALS.zDocVP[i].append(topic)
            VALS.n_VPK[int(tempVP[j])][topic] += 1
            VALS.n_VPK_sum[topic] += 1
            VALS.n_docK[i][topic] += 1
            

def saveModel():
    ## Save the Model
    oFile = open(os.path.join(VALS.Odir,"model.txt"),"w")
    oFile.write("K  "+str(VALS.K)+"\n")
    oFile.write("iterations "+str(VALS.iters)+"\n")
    oFile.write("aplha_R    "+str(VALS.alpha_R)+"\n")
    oFile.write("aplha_O    "+str(VALS.alpha_O)+"\n")
    oFile.write("aplha_D    "+str(VALS.alpha_D)+"\n")
    oFile.write("gamma_R    "+str(VALS.gamma_R)+"\n")
    oFile.write("gamma_I    "+str(VALS.gamma_I)+"\n")
    oFile.close()
    
    ## Print Top 10 words per each topic
    oFile = open(os.path.join(VALS.Odir,"Instance_Topics.txt"),"w")
    Transpose = VALS.sigma.transpose()
    for k in range(0,VALS.K):
        temp = Transpose[0:VALS.n_NP][k]
        temp = np.argsort(temp)
        oFile.write("Topic-"+str(k)+":  ")
        for i in range(0,10):
            oFile.write(VALS.dictID2NP[temp[VALS.n_NP-1-i]]+"   ")
        oFile.write("\n")
        
    oFile.close()
    
    oFile = open(os.path.join(VALS.Odir,"Relation_Topics.txt"),"w")
    Transpose = VALS.delta.transpose()
    for k in range(0,VALS.K):
        temp = Transpose[0:VALS.n_VP][k]
        temp = np.argsort(temp)
        oFile.write("Topic-"+str(k)+":  ")
        for i in range(0,10):
            oFile.write(VALS.dictID2VP[temp[VALS.n_VP-1-i]]+"   ")
        oFile.write("\n")
        
    oFile.close()
    
    
    np.save(os.path.join(VALS.Odir,"Pi_O"),VALS.pi_O)
    np.save(os.path.join(VALS.Odir,"Pi_R"),VALS.pi_R)
    
    oFile = open(os.path.join(VALS.Odir,"Top_SVO_Topics.txt"),"w")
    
    indices = np.argsort(VALS.pi_R,axis=None)    
    TT = VALS.K**3
    for i in range(0,100):
        oFile.write(VALS.dictID2TopicTriple[indices[TT-i]]+"\n")
    
    oFile.close()