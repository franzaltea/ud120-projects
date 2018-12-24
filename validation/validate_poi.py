#!/usr/bin/python


"""
    Starter code for the validation mini-project.
    The first step toward building your POI identifier!

    Start by loading/formatting the data

    After that, it's not our code anymore--it's yours!
"""

import sys, getopt, time
import pickle
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn import tree
from sklearn.metrics import accuracy_score
from sklearn.cross_validation import train_test_split

script_name = 'validate_poi'


### it's all yours from here forward!
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

class DT_validate_poi:

    # Constructor
    def __init__(self, labels, features):
        self.labels = labels
        self.features = features

        # Split into a training and testing set
        self.features_train, self.features_test, self.labels_train, self.labels_test = train_test_split(self.features, self.labels, test_size=0.3, random_state=42)

    # Logging function, just keep it simple for now and print text
    def log(self, text):
        print text

    # Main Script Logic
    def run(self):
        start_time = time.time()
        self.log("****** {0} has started. ******".format(script_name))

        # Train the svm
        clf = tree.DecisionTreeClassifier()
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

    data_dict = pickle.load(open("../final_project/final_project_dataset.pkl", "r") )

    ### first element is our labels, any added elements are predictor
    ### features. Keep this the same for the mini-project, but you'll
    ### have a different feature list when you do the final project.
    features_list = ["poi", "salary"]

    data = featureFormat(data_dict, features_list)
    labels, features = targetFeatureSplit(data)


    try:
        optlist, args = getopt.getopt(sys.argv[1:], "", ('debug'))
    except:
        usage()

    for o, a in optlist:
        if o in ('--debug',):
            debug = 1

    # Initialize the script with the required variables
    job = DT_validate_poi(labels, features)

    # Run the script and if required, add the database
    if debug:
        job.run()
    else:
        job()

