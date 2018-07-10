#!/usr/bin/python

""" 
    This is the code to accompany the Lesson 3 (decision tree) mini-project.

    Use a Decision Tree to identify emails from the Enron corpus by author:    
    Sara has label 0
    Chris has label 1
"""
    
import sys, getopt, time
sys.path.append("../tools/")
from email_preprocess import preprocess
from sklearn import tree
from sklearn.metrics import accuracy_score

script_name = 'dt_author_id'

#################################################################
#Functions and classes
#################################################################
def usage():
    print """
Usage:\n
%s -w <words_file> -a <authors_name>
    - w         words file to be processed
    - a         authors file to be processed
    - debug     currently does not do anything
    """ % sys.argv[0]
    sys.exit(1)
    
class DT_author_id:

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
        
        # Train the svm
        clf = tree.DecisionTreeClassifier(min_samples_split=40)
        clf.fit(self.features_train, self.labels_train)

        #Predict the test data
        self.pred = clf.predict(self.features_test)

        acc = accuracy_score(self.pred, self.labels_test)
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
    job = DT_author_id(words_file=words_file, authors_file=authors_file)

    # Run the script and if required, add the database
    if debug:
        job.run()
    else:
        job()

