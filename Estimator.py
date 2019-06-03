# -*- coding: utf-8 -*-
#!usr/bin/env python

import VALS
import numpy
import myThread
import timeit
import multiprocessing

def seq_Estimate():
    print("TBH")
            
def parallel_Estimate():
    threads = {}
    
    totalTime = 0
    Q  = multiprocessing.Queue()
    for iter in range (0,VALS.iters):
        start = timeit.default_timer()
        print("Sampling: Iteration Number: "+str(iter+1))
        for i in range(0,VALS.num_Threads):
            threads[i] = myThread.myThread(i+1,"Thread-"+str(i+1),Q)
            
        for i in range(0,VALS.num_Threads):
            threads[i].start()
        
        
        temp_NPK = numpy.zeros([VALS.n_NP,VALS.K],dtype=float)
        temp_VPK = numpy.zeros([VALS.n_VP,VALS.K],dtype=float)
        temp_NPK_Sum = numpy.zeros([VALS.K],dtype=float)
        temp_VPK_Sum = numpy.zeros([VALS.K],dtype=float)
        
        track =0
        while 1:
            if track == VALS.num_Threads:
                break
            else:
                track += 1
                print("Tracking:"+str(track))
                vals_dict = Q.get()
                ID = vals_dict['ID']
                for ci in range(vals_dict['startCI,'+ID],vals_dict['endCI,'+ID]):
                    VALS.z_CI[ci]=vals_dict['z_CI,'+ID][ci]
                    VALS.n_CIK[ci]=vals_dict['n_CIK,'+ID][ci]
                for trp in range(vals_dict['startTrp,'+ID],vals_dict['endTrp,'+ID]):
                    VALS.z_Trp[trp]=vals_dict['z_Trp,'+ID][trp]
                    VALS.n_TK[trp]=vals_dict['n_TK,'+ID][trp]
                for doc in range(vals_dict['startDoc,'+ID],vals_dict['endDoc,'+ID]):
                    VALS.zDocNP[doc]=vals_dict['zDocNP,'+ID][doc]
                    VALS.zDocVP[doc]=vals_dict['zDocVP,'+ID][doc]
                    VALS.n_docK[doc]=vals_dict['n_docK,'+ID][doc]
                temp_NPK += vals_dict['n_NPK,'+ID] - VALS.n_NPK
                temp_VPK += vals_dict['n_VPK,'+ID] - VALS.n_VPK
                temp_NPK_Sum += vals_dict['n_NPK_sum,'+ID] - VALS.n_NPK_sum
                temp_VPK_Sum += vals_dict['n_VPK_sum,'+ID] - VALS.n_VPK_sum
            
        VALS.n_NPK += temp_NPK        
        VALS.n_VPK += temp_VPK
        VALS.n_NPK_sum += temp_NPK_Sum
        VALS.n_VPK_sum += temp_VPK_Sum
        stop = timeit.default_timer()
        totalTime += stop - start
        print("Time Elapsed for Iteration-"+str(iter)+": "+str(stop-start))
        
    print("Total Estimating Time: "+str(totalTime))

def computeParams():
    ## Compute Sigma
    VALS.sigma = numpy.zeros([VALS.n_NP,VALS.K],dtype=float)
    for np in range(0,VALS.n_NP):
        for k in range(0,VALS.K):
            VALS.sigma[np][k] = (VALS.n_NPK[np][k]+VALS.gamma_I)/(VALS.n_NPK_sum[k]+VALS.n_NP*VALS.gamma_I)
            
    ## Compute Delta
    VALS.delta = numpy.zeros([VALS.n_VP,VALS.K],dtype=float)
    for vp in range(0,VALS.n_VP):
        for k in range(0,VALS.K):
            VALS.delta[vp][k] = (VALS.n_VPK[vp][k]+VALS.gamma_R)/(VALS.n_VPK_sum[k]+VALS.n_VP*VALS.gamma_R)
            
    ## Compute Theta
    VALS.theta = numpy.zeros([VALS.M,VALS.K],dtype=float)
    for doc in range(0,VALS.M):
        for k in range(0,VALS.K):
            VALS.theta[doc][k] = (VALS.n_docK[doc][k]+VALS.alpha_D)/(sum(VALS.n_docK[0:VALS.M][k])+VALS.K*VALS.alpha_D)
    
    ## Compute pi_O
    VALS.pi_O = numpy.zeros([VALS.K,VALS.K],dtype=float)
    for z_C in range(0,VALS.K):
        for z_I in range(0,VALS.K):
            temp  = numpy.sum(VALS.n_CIK)
            VALS.pi_O[z_C][z_I] = (sum(VALS.n_CIK[0:VALS.CI][z_C][z_I])+VALS.alpha_O)/(temp + VALS.K*VALS.K*VALS.alpha_O)
    
    ## Compute pi_R
    VALS.pi_R=numpy.zeros([VALS.K,VALS.K,VALS.K],dtype=float)
    tripleCounts = numpy.zeros([VALS.K,VALS.K,VALS.K],dtype=float)
    for trp in range(0,VALS.T):
        temp = VALS.n_TK[trp]
        for topic in temp:
            count = temp[topic]
            topic_triple = VALS.dictID2TopicTriple[topic]
            topic_triple = topic_triple.split(",")
            tripleCounts[int(topic_triple[0])][int(topic_triple[1])][int(topic_triple[2])] += count
    for z_S in range(0,VALS.K):
        for z_V in range(0,VALS.K):
            for z_O in range(0,VALS.K):
                temp1 = numpy.sum(tripleCounts)
                VALS.pi_R[z_S][z_V][z_O] = (tripleCounts[z_S][z_V][z_O])/(temp1 + VALS.K*VALS.K*VALS.K*VALS.alpha_R)
