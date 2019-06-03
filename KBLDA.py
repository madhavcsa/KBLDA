# -*- coding: utf-8 -*-
#!usr/bin/env python

import argparse
import VALS
import helperMethods
import Estimator
import os

parser = argparse.ArgumentParser()


# // Read the command line options
parser.add_argument("TriplesFile",help="Enter the path to Triples File",type=str)
parser.add_argument("CIFile",help="Enter the path to Hearst Patterns File",type=str)
parser.add_argument("NPFile",help="Enter the path to file corresponding to Noun Phrases of Documents ",type=str)
parser.add_argument("VPFile",help="Enter the path to file corresponding to Verb Phrases of Documents ",type=str)
parser.add_argument("--alpha_R",type=float,help="Enter the alpha for SVO")
parser.add_argument("--alpha_O",type=float,help="Enter the alpha for Ontology")
parser.add_argument("--alpha_D",type=float,help="Enter the alpha for Documents")
parser.add_argument("--gamma_I",type=float,help="Enter the gamma for Noun phrases")
parser.add_argument("--gamma_R",type=float,help="Enter the gamma for Verb Phrases")
parser.add_argument("--K",type = int, default = 10,help="Enter the number of Topics, default 100")
parser.add_argument("--iters",type = int, default = 2000, help="Enter the maximum number of iterations, default 2000")
parser.add_argument("--Odir",help="Enter the output directory to which the results will be saved",type=str,default="OutPut")
parser.add_argument("--sampling",help="Enter seq for sequential and parallel for distributed; parallel is faster and is default choice",type=str, default="parallel")
parser.add_argument("--Threads",help="Enter number of threads",type=int,default=10)

args = parser.parse_args()


# // Load the input data

VALS.init()

VALS.K = args.K
VALS.iters = args.iters
VALS.Odir = args.Odir
VALS.num_Threads = args.Threads
VALS.alpha_R = args.alpha_R
VALS.alpha_O = args.alpha_O
VALS.alpha_D = args.alpha_D
VALS.gamma_I = args.gamma_I
VALS.gamma_R = args.gamma_R

if not os.path.exists(args.Odir):
    os.makedirs(args.Odir)

helperMethods.readCIFile(args.CIFile)
print("Number of CI Pairs:"+str(VALS.CI))
helperMethods.readTriplesFile(args.TriplesFile)
print("Number of Triples:"+str(VALS.T))
helperMethods.readDocs(args.NPFile,args.VPFile)
print("Number of Docs:"+str(VALS.M))
helperMethods.initializeCounts()
helperMethods.initializeTopicAssignments()

if args.sampling != "seq":
    Estimator.parallel_Estimate()
else:
    Estimator.seq_Estimate()
    
Estimator.computeParams()
helperMethods.saveModel()
