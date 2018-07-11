#!/usr/bin/python

import sys, time, getopt
import matplotlib.pyplot as plt
from prep_terrain_data import makeTerrainData
from class_vis import prettyPicture
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

script_name = 'ran_forest_terrain'

#################################################################
#Functions and classes
#################################################################
def usage():
    print """
Usage:\n
%s -n <number of points> [--debug]
    - n         number of points to be generated for sample
    - debug     currently does not do anything
    """ % sys.argv[0]
    sys.exit(1)
    
class Ran_forest_terrain:

    # Constructor
    def __init__(self, N_points):
        self.features_train, self.labels_train, self.features_test, self.labels_test = makeTerrainData(N_points)

    # Logging function, just keep it simple for now and print text
    def log(self, text):
        print text

    # Main Script Logic
    def run(self):
        start_time = time.time()
        self.log("****** {0} has started. ******".format(script_name))
        
        subset_count = 25
        self.log("Random forest subsets set to {0}".format(subset_count))
        
        # Train the Random forest terrain
        clf = RandomForestClassifier(n_estimators=subset_count, min_samples_split=5)
        clf.fit(self.features_train, self.labels_train)

        #Predict the test data
        self.pred = clf.predict(self.features_test)
        
        ### the training data (features_train, labels_train) have both "fast" and "slow"
        ### points mixed together--separate them so we can give them different colors
        ### in the scatterplot and identify them visually
        grade_fast = [self.features_train[ii][0] for ii in range(0, len(self.features_train)) if self.labels_train[ii]==0]
        bumpy_fast = [self.features_train[ii][1] for ii in range(0, len(self.features_train)) if self.labels_train[ii]==0]
        grade_slow = [self.features_train[ii][0] for ii in range(0, len(self.features_train)) if self.labels_train[ii]==1]
        bumpy_slow = [self.features_train[ii][1] for ii in range(0, len(self.features_train)) if self.labels_train[ii]==1]
        
        
        #### initial visualization
        plt.xlim(0.0, 1.0)
        plt.ylim(0.0, 1.0)
        plt.scatter(bumpy_fast, grade_fast, color = "b", label="fast")
        plt.scatter(grade_slow, bumpy_slow, color = "r", label="slow")
        plt.legend()
        plt.xlabel("bumpiness")
        plt.ylabel("grade")
        plt.show()
        ################################################################################


        ### your code here!  name your classifier object clf if you want the 
        ### visualization code (prettyPicture) to show you the decision boundary
        try:
            prettyPicture(clf, self.features_test, self.labels_test)
        except NameError, e:
            self.log("Failed to visualize the feature - {0}".format(e))


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
    N_points = 1000


    try:
        optlist, args = getopt.getopt(sys.argv[1:], "n:", ('debug'))
    except:
        usage()

    for o, a in optlist:
        if o in ('--debug',):
            debug = 1
        elif o == '-n':
            N_points = a

    # Initialize the script with the required variables
    job = Ran_forest_terrain(N_points)

    # Run the script
    if debug:
        job.run()
    else:
        job()
