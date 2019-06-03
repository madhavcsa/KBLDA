# KB-LDA
This is my implementation of the work [1]. For any questions regarding the work, please contact the original authors of the paper. 

## Setup:

To get the project's source code, clone the github repository:

    $ git clone https://github.com/madhavcsa/KBLDA.git
    
 ### Dependencies:

Please install the following dependencies for KBLDA to run:
numpy, scipy, scikit-learn, joblib.


## Usage:

To use kblda, you can start with these following samples commands:

     $ python KBLDA.py <TriplesFile> <CIFile> <NPFile> <VPFile>
     
### Positional Arguments:
  * TriplesFile          Enter the path to Triples File
  * CIFile               Enter the path to Hearst Patterns File
  * NPFile               Enter the path to file corresponding to Noun Phrases of
                       Documents
  * VPFile               Enter the path to file corresponding to Verb Phrases of
                       Documents
                       
### Optional Arguments:                       

  * -h, --help           show this help message and exit
  * --alpha_R ALPHA_R    Enter the alpha for SVO
  * --alpha_O ALPHA_O    Enter the alpha for Ontology
  * --alpha_D ALPHA_D    Enter the alpha for Documents
  * --gamma_I GAMMA_I    Enter the gamma for Noun phrases
  * --gamma_R GAMMA_R    Enter the gamma for Verb Phrases
  * --K K                Enter the number of Topics, default 100
  * --iters ITERS        Enter the maximum number of iterations, default 2000
  * --Odir ODIR          Enter the output directory to which the results will be
                       saved
  * --sampling SAMPLING  Enter seq for sequential and parallel for distributed;
                       parallel is faster and is default choice
  * --Threads THREADS    Enter number of threads
  
  
# Refernce  
  
  [1] Dana Moshkovitz-Attias and William W. Cohen. Kb-lda: Jointly learning a knowledge base of hierarchy, relations, and facts. Proceedings of ACL, 2015.



    


