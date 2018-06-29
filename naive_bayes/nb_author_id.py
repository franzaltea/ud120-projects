#!/usr/bin/python
""" 
    This is the code to accompany the Lesson 1 (Naive Bayes) mini-project. 

    Use a Naive Bayes Classifier to identify emails by their authors
    
    authors and labels:
    Sara has label 0
    Chris has label 1
"""

import sys, getopt
import time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score

script_name = 'nb_author_id'



#################################################################
#Functions and classes
#################################################################
def usage():
    print """
Usage:\n
%s -w <merchant_id> -p <filename> [--debug]
    - w         words file to be processed
    - a         authors file to be processed
    - d         database to run the script against, defaults to cert_robot
    - debug     currently same as --nocron
    """ % sys.argv[0]
    sys.exit(1)

class NB_author_id:

    # Constructor
    def __init__(self, words_file, authors_file):
        self.words_file = "../tools/word_data.pkl"
        self.authors_file = "../tools/email_authors.pkl"
        ### features_train and features_test are the features for the training
        ### and testing datasets, respectively
        ### labels_train and labels_test are the corresponding item labels
        self.features_train, self.features_test, self.labels_train, self.labels_test = preprocess(words_file=self.words_file, authors_file=self.authors_file)

    # Logging function, just keep it simple for now and print text
    def log(self, text):
        print text

    # Main Script Logic
    def run(self):
        start_time = time.time()
        self.log("****** {0} has started. ******".format(script_name))
        self.log("words_file: {0}".format(self.words_file))
        self.log("authors_file: {0}".format(authors_file))

        clf = GaussianNB()

        # Train the Gaussian NB here
        time_train = time.time()
        clf.fit(self.features_train, self.labels_train)
        self.log("Training Time: {0}".format(round(time.time() - time_train, 3)))

        # Predict the test data
        time_test = time.time()
        pred = clf.predict(self.features_test)
        self.log("Test Time: {0}".format(round(time.time() - time_test, 3)))

        acc = accuracy_score(pred, self.labels_test)
        self.log("Accuracy is {0}".format(acc))
        self.log("")

        self.log("****** {0} finished. ******".format(script_name))
        self.log("       {0}".format(time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())))
        self.log("       Total Time: {0}".format(round(time.time() - start_time, 3)))

    def __call__(self):
        # In case we want debug mode to work differently from non debug mode
        self.run()

##################################################################
# Main Program
##################################################################
if __name__ == '__main__':
    # Can define variables here
    debug = False
    words_file = "../tools/word_data.pkl"
    authors_file = "../tools/email_authors.pkl"


    try:
        optlist, args = getopt.getopt(sys.argv[1:], "w:p:", ('debug'))
    except:
        usage()

    for o, a in optlist:
        if o in ('--debug',):
            debug = 1
        elif o == '-w':
            word_file = a
        elif o == '-p':
            process_file = a

    # Initialize the script with the required variables
    job = NB_author_id(words_file=words_file, authors_file=authors_file)

    # Run the script and if required, add the database
    if debug:
        job.run()
    else:
        job()
