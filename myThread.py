# -*- coding: utf-8 -*-

import multiprocessing
import VALS
import numpy
import random
import math
import timeit

class myThread(multiprocessing.Process):
    def __init__(self, threadID, name, Q ):
        multiprocessing.Process.__init__(self)
        self.threadID = threadID
        self.name = name
        self.Q = Q
        
    def run(self):
        print ("Starting " + self.name)
        self.initializeLocal()
        self.sample()
        self.dict = {}
        ID = str(self.threadID)
        self.dict['ID']=ID
        self.dict['startCI,'+ID]= self.startCI
        self.dict['endCI,'+ID]=self.endCI
        self.dict['n_CIK,'+ID]= VALS.n_CIK
        self.dict['z_CI,'+ID]=VALS.z_CI
        self.dict['startTrp,'+ID]=self.startTrp
        self.dict['endTrp,'+ID] = self.endTrp
        self.dict['n_TK,'+ID]=VALS.n_TK
        self.dict['z_Trp,'+ID]=VALS.z_Trp
        self.dict['startDoc,'+ID]=self.startDoc
        self.dict['endDoc,'+ID]=self.endDoc
        self.dict['zDocNP,'+ID] = VALS.zDocNP
        self.dict['zDocVP,'+ID]=VALS.zDocVP
        self.dict['n_NPK,'+ID]=VALS.n_NPK
        self.dict['n_VPK,'+ID]=VALS.n_VPK
        self.dict['n_NPK_sum,'+ID]=VALS.n_NPK_sum
        self.dict['n_VPK_sum,'+ID]=VALS.n_VPK_sum
        self.dict['n_docK,'+ID]=VALS.n_docK
        self.Q.put(self.dict)
        print ("Exiting " + self.name)
        
        
    ## Intialize the thread specific local variables
    def initializeLocal(self):
        print(self.name+":Initializing locals")
        seed = math.floor(VALS.CI/VALS.num_Threads)
        self.startCI = (self.threadID-1)*seed
        temp = (self.threadID)*seed
        if VALS.CI-temp >= VALS.num_Threads:
            self.endCI = temp
        else:
            self.endCI = VALS.CI
        
        seed = math.floor(VALS.T/VALS.num_Threads)
        self.startTrp = (self.threadID-1)*seed
        temp = (self.threadID)*seed
        if VALS.T-temp >= VALS.num_Threads:
            self.endTrp = temp
        else:
            self.endTrp = VALS.T
        
        seed = math.floor(VALS.M/VALS.num_Threads)
        self.startDoc = (self.threadID-1)*seed
        temp = (self.threadID)*seed
        if VALS.M-temp >= VALS.num_Threads:
            self.endDoc = temp
        else:
            self.endDoc = VALS.M
        
        
        print(self.name+":Locals Initialized")
        
    def sample(self):
        ## Sampling for each CI pair
        print(self.name+":Starting sampling")
        
        begin = timeit.default_timer()
        for ci in range(self.startCI,self.endCI):
           # for i in range(0,int(VALS.CIdict[VALS.dictID2CI[ci]])):
            topic = self.sampleCI(ci)
            VALS.z_CI[ci] = topic
        end = timeit.default_timer()
        print(self.name+":Sampling done for CIs, time taken:"+ str(begin-end))
        
        ## Sampling for each Triple
        
        begin = timeit.default_timer()
        for trp in range(self.startTrp,self.endTrp):
            #for i in range(0,int(VALS.Triplesdict[VALS.dictID2Trp[trp]])):
            topic = self.sampleTrp(trp)
            VALS.z_Trp[trp] = topic
        end = timeit.default_timer()
        print(self.name+":Sampling done for Triples, time taken:"+ str(begin-end))
        
        ## Sampling for Documents
        begin = timeit.default_timer()
        for doc in range(self.startDoc,self.endDoc):
            tempNP = VALS.docNP[doc]            
            for np in range(0,len(tempNP)):
                topic = self.sampleDocNP(doc,np)
                VALS.zDocNP[doc][np] = topic
            tempVP = VALS.docVP[doc]
            for vp in range(0,len(tempVP)):
                topic = self.sampleDocVP(doc,vp)
                VALS.zDocVP[doc][vp] = topic
        end = timeit.default_timer()
        print(self.name+":Sampling done for docs, time taken:"+ str(begin-end))
       
       
    ## Sampling for CIs from P(Z_i^CI|...)
    def sampleCI(self,ci):
        topic = VALS.z_CI[ci]
        Tpair = VALS.dictID2TopicPair[topic]
        Tpair = Tpair.split(",")
        VALS.n_CIK[ci][int(Tpair[0])][int(Tpair[1])] -= 1
        
        ## Decrement counts for corresponding NPs
        CI_Pair = VALS.dictID2CI[ci]
        CI_Pair = CI_Pair.split(",")
        VALS.n_NPK[VALS.dictNP2ID[CI_Pair[0]],int(Tpair[0])] -= 1
        VALS.n_NPK[VALS.dictNP2ID[CI_Pair[1]],int(Tpair[1])] -= 1
        VALS.n_NPK_sum[int(Tpair[0])] -= 1
        VALS.n_NPK_sum[int(Tpair[1])] -= 1
    
        p = numpy.zeros(VALS.K * VALS.K)
    
        for k in range(0,VALS.K*VALS.K):
            Tpair = VALS.dictID2TopicPair[k]
            Tpair = Tpair.split(",")
            temp_CI = (VALS.n_CIK[ci][int(Tpair[0])][int(Tpair[1])]+VALS.alpha_O)
            temp_C = (VALS.n_NPK[VALS.dictNP2ID[CI_Pair[0]],int(Tpair[0])]+VALS.gamma_I)/(VALS.n_NPK_sum[int(Tpair[0])]+VALS.n_NP*VALS.gamma_I)
            temp_I = (VALS.n_NPK[VALS.dictNP2ID[CI_Pair[1]],int(Tpair[1])]+VALS.gamma_I)/(VALS.n_NPK_sum[int(Tpair[1])]+VALS.n_VP*VALS.gamma_I)
            p[k] = temp_CI * temp_C * temp_I
        
        ## Cumulate Multinomials
        for k in range(1,VALS.K*VALS.K):
            p[k] += p[k-1]
        
        u = random.uniform(0,p[VALS.K*VALS.K-1])
    
        for k in range(0,VALS.K*VALS.K):
            if p[k] > u:
                break
    
        topic = k
        Tpair = VALS.dictID2TopicPair[topic]
        Tpair = Tpair.split(",")
        VALS.n_CIK[ci][int(Tpair[0])][int(Tpair[1])] += 1
        ## Increment counts for corresponding NPs
        VALS.n_NPK[VALS.dictNP2ID[CI_Pair[0]],int(Tpair[0])] += 1
        VALS.n_NPK[VALS.dictNP2ID[CI_Pair[1]],int(Tpair[1])] += 1
        VALS.n_NPK_sum[int(Tpair[0])] += 1
        VALS.n_NPK_sum[int(Tpair[1])] += 1
    
    
        return topic
        
        
    ## Sampling for Triples from P(z_j^SVO|...)
    def sampleTrp(self,trp):
        topic = VALS.z_Trp[trp]
        Ttriple = VALS.dictID2TopicTriple[topic]
        Ttriple = Ttriple.split(",")
        #VALS.n_TK[trp][int(Ttriple[0])][int(Ttriple[1])][int(Ttriple[2])] -= 1
        temp = VALS.n_TK[trp]
        temp[topic] -= 1
        
        ## Decrement counts for corresponding NPs and VPs
        Trp_Pair = VALS.dictID2Trp[trp]
        Trp_Pair = Trp_Pair.split(",")
        VALS.n_NPK[VALS.dictNP2ID[Trp_Pair[0]],int(Ttriple[0])] -= 1
        VALS.n_VPK[VALS.dictVP2ID[Trp_Pair[1]],int(Ttriple[1])] -= 1
        VALS.n_NPK[VALS.dictNP2ID[Trp_Pair[2]],int(Ttriple[2])] -= 1
        VALS.n_NPK_sum[int(Ttriple[0])] -= 1
        VALS.n_NPK_sum[int(Ttriple[2])] -= 1
        VALS.n_VPK_sum[int(Ttriple[1])] -= 1
            
        p = numpy.zeros(VALS.K*VALS.K*VALS.K)
        
        for k in range(0,VALS.K*VALS.K*VALS.K):
            Ttriple = VALS.dictID2TopicTriple[topic]
            Ttriple = Ttriple.split(",")
            
            if k in temp:
                temp_SVO = temp[k]+VALS.alpha_R
            else:
                temp_SVO = VALS.alpha_R                
            
            # VALS.n_TK[trp][int(Ttriple[0])][int(Ttriple[1])][int(Ttriple[2])]+VALS.alpha_R
            temp_S = (VALS.n_NPK[VALS.dictNP2ID[Trp_Pair[0]],int(Ttriple[0])]+VALS.gamma_I)/(VALS.n_NPK_sum[int(Ttriple[0])]+VALS.n_NP*VALS.gamma_I)
            temp_V = (VALS.n_VPK[VALS.dictVP2ID[Trp_Pair[1]],int(Ttriple[1])]+VALS.gamma_R)/(VALS.n_VPK_sum[int(Ttriple[1])]+VALS.n_VP*VALS.gamma_R)
            temp_O = (VALS.n_NPK[VALS.dictNP2ID[Trp_Pair[2]],int(Ttriple[2])]+VALS.gamma_I)/(VALS.n_NPK_sum[int(Ttriple[2])]+VALS.n_NP*VALS.gamma_I)
            p[k] = temp_SVO * temp_S * temp_V * temp_O
        
        ## Cumulate Multinomials
        for k in range(1,VALS.K*VALS.K*VALS.K):
            p[k] += p[k-1]
            
        u = random.uniform(0,p[VALS.K*VALS.K*VALS.K-1])
        
        for k in range(0,VALS.K*VALS.K*VALS.K):
            if p[k] > u:
                break
        
        topic = k
        Ttriple = VALS.dictID2TopicTriple[topic]
        Ttriple = Ttriple.split(",")
        #VALS.n_TK[trp][int(Ttriple[0])][int(Ttriple[1])][int(Ttriple[2])] += 1
        if k not in temp:
            temp[k] = 1
        else:
            temp[k] += 1
        VALS.n_TK[trp]=temp
        
        ## Increment counts for Corresponding NPs and VPs        
        VALS.n_NPK[VALS.dictNP2ID[Trp_Pair[0]],int(Ttriple[0])] += 1
        VALS.n_VPK[VALS.dictVP2ID[Trp_Pair[1]],int(Ttriple[1])] += 1
        VALS.n_NPK[VALS.dictNP2ID[Trp_Pair[2]],int(Ttriple[2])] += 1
        VALS.n_NPK_sum[int(Ttriple[0])] += 1
        VALS.n_NPK_sum[int(Ttriple[2])] += 1
        VALS.n_VPK_sum[int(Ttriple[1])] += 1
        
        
        return topic

    ## Sampling for Instances in DOcs        
    def sampleDocNP(self,doc,np):
        topic = VALS.zDocNP[doc][np]
        np_ID = VALS.docNP[doc][np]
        VALS.n_docK[doc][int(topic)] -= 1
        VALS.n_NPK[np_ID][topic] -= 1
        VALS.n_NPK_sum[topic] -= 1
        
        p = numpy.zeros(VALS.K)
        
        for k in range(0,VALS.K):
            temp_doc = VALS.n_docK[doc][k]
            temp_np = (VALS.n_NPK[np_ID][k]+VALS.gamma_I)/(VALS.n_NPK_sum[k]+VALS.n_NP*VALS.gamma_I)
            p[k] = temp_doc * temp_np
        
        ## Cumulate Multinomials
        for k in range(1,VALS.K):
            p[k] += p[k-1]
        
        u = random.uniform(0,p[VALS.K-1])
        
        for k in range(0,VALS.K):
            if p[k]>u:
                break
            
        topic = k
        VALS.n_docK[doc][int(topic)] += 1
        VALS.n_NPK[np_ID][topic] += 1
        VALS.n_NPK_sum[topic] += 1
        
        return topic
        
    ## Sampling for Relations in DOcs
    def sampleDocVP(self,doc,vp):
        topic = VALS.zDocVP[doc][vp]
        vp_ID = VALS.docVP[doc][vp]
        VALS.n_docK[doc][int(topic)] -= 1
        VALS.n_VPK[vp_ID][topic] -= 1
        VALS.n_VPK_sum[topic] -= 1
        
        p = numpy.zeros(VALS.K)
        
        for k in range(0,VALS.K):
            temp_doc = VALS.n_docK[doc][k]
            temp_vp = (VALS.n_VPK[vp_ID][k]+VALS.gamma_R)/(VALS.n_VPK_sum[k]+VALS.n_VP*VALS.gamma_R)
            p[k] = temp_doc * temp_vp
        
        ## Cumulate Multinomials
        for k in range(1,VALS.K):
            p[k] += p[k-1]
        
        u = random.uniform(0,p[VALS.K-1])
        
        for k in range(0,VALS.K):
            if p[k]>u:
                break
            
        topic = k
        VALS.n_docK[doc][int(topic)] += 1
        VALS.n_VPK[vp_ID][topic] += 1
        VALS.n_VPK_sum[topic] += 1
        
        return topic
