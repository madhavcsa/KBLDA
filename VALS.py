# -*- coding: utf-8 -*-
#!usr/bin/env python
import numpy as np

def init():
        ## various Dictionaries
        global dictNP2ID ## NP -> ID
        dictNP2ID = {}
        global dictID2NP ## ID -> NP
        dictID2NP = {}
        global CIdict ## Dictionary of CI pairs
        CIdict = {}
        global dictCI2ID ## CI -> ID
        dictCI2ID = {}
        global dictID2CI ## ID -> CI
        dictID2CI = {}
        global Triplesdict ## Dictionary of Triples
        Triplesdict = {}
        global dictTrp2ID ## Triples -> ID
        dictTrp2ID = {}
        global dictID2Trp ## ID -> Triples
        dictID2Trp = {}
        global dictVP2ID ## VP -> ID
        dictVP2ID = {}
        global dictID2VP ## ID -> VP
        dictID2VP = {}
        global dictDoc2ID ## DOC -> ID
        dictDoc2ID = {}
        global dictID2Doc ## ID -> DOC
        dictID2Doc = {}
        
        ## Global Variables
        global M ##no of docs
        M = 0 
        global T ##no of Triples
        T = 0 
        global CI ##no of CI pairs
        CI = 0 
        global K ##no of Topics
        K = 0 
        global n_NP ## Size of NP dictionary (Instance Dictionary)
        n_NP =0
        global n_VP ## Size of VP dictionary (Relation Dictionary)
        n_VP =0
        global iters ##no of iterations
        iters = 0 
        global docNP ##NPs in docs 
        docNP = {}
        global docVP ##VPs in docs
        docVP= {}
        global Odir #output directory
        Odir = '' 
        
        ## Hyper-Parameters
        global alpha_O
        alpha_O = 1
        global alpha_D
        alpha_D = 1
        global alpha_R
        alpha_R = 1
        global gamma_I
        gamma_I = 1
        global gamma_R
        gamma_R = 1


        ## Parameter Variables
        global sigma
        sigma = np.zeros([len(dictID2NP),K],dtype=float)
        global delta
        delta = np.zeros([len(dictVP2ID),K],dtype=float)
        global pi_O
        pi_O = np.zeros([K,K],dtype=float)
        global pi_R
        pi_R = np.zeros([K,K,K],dtype=float)
        global theta
        theta = np.zeros([M,K],dtype=float)
        
        ## Count Variables
        global n_NPK ## number of times a topic is assigned to a noun phrase
        n_NPK =[]
        global n_VPK ## number of times a topic is aasigned to a verb phrase
        n_VPK = []
        global n_docK ## number of times a topic is assigned in a doc
        n_docK = []
        global n_CIK ## number of times a topic pair is assigned to a CI pair
        n_CIK = []
        global n_TK ## number of times a topic triple is assigned to a Triple
        n_TK = []
        global n_NPK_sum ## Topic Wise sum of NP counts
        n_NPK_sum = []
        global n_VPK_sum ## Topic Wise sum of VP counts
        n_VPK_sum=[]
        
        ## Topic Assignment Variables
        global z_CI ## Current Topic assignment of a CI pair
        z_CI = {}
        global z_Trp ## Current Topic assignment of a Triple
        z_Trp = {}
        global zDocNP ## Current Topic Assignment of Noun Phrases in DOCS
        zDocNP = {}
        global zDocVP ## Current Topic Assignment of Verb Phrases in DOCS
        zDocVP = {}
        global dictID2TopicPair ## ID -> Topic CI Pair
        dictID2TopicPair = {}
        global dictID2TopicTriple ## ID -> Topic Triple
        dictID2TopicTriple = {}
        
        ## Auxiliary Variables
        global num_Threads ## Total number of threads
        num_Threads = 0
        global thread_NPK
        thread_NPK = {}
        global thread_VPK
        thread_VPK = {}
        global thread_NPK_sum
        thread_NPK_sum = {}
        global thread_VPK_sum
        thread_VPK_sum = {}
