#!/usr/bin/python 

""" 
    Skeleton code for k-means clustering mini-project.
"""




import pickle
import numpy
import matplotlib.pyplot as plt
import sys, getopt, time
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit
from sklearn.cluster import KMeans
from sklearn import preprocessing

#################################################################
#Functions and classes
#################################################################
def usage():
    print """
Usage:\n
%s -n <num_clusters> -f <feature_list> --debug
    - n         number of clusters
    - f         list of features to be added (needs at least 2)
    --scaled    specifies whether to do scaling on data or not
    - debug     currently does not do anything
    """ % sys.argv[0]
    sys.exit(1)

script_name = 'k_means_cluster'

def Draw(pred, features, poi, mark_poi=False, name="image.png", f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """

    ### plot each cluster with a different color--add more colors for
    ### drawing more than five clusters
    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])

    ### if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()

class K_means_cluster:

    # Constructor
    def __init__(self, n_clusters, features_list, scaled):
        self.n_clusters = n_clusters
        self.features_list = features_list
        self.scaled = scaled

        ### load in the dict of dicts containing all the data on each person in the dataset
        data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
        ### there's an outlier--remove it! 
        data_dict.pop("TOTAL", 0)

        data = featureFormat(data_dict, features_list )
        self.poi, self.finance_features = targetFeatureSplit( data )

    # Logging function, just keep it simple for now and print text
    def log(self, text):
        print text

    # Main Script Logic
    def run(self):
        start_time = time.time()
        self.log("****** {0} has started. ******".format(script_name))
        # scale the features if needed:
        if self.scaled:
            min_max_scaler = preprocessing.MinMaxScaler()
            scaled_feature = min_max_scaler.fit_transform(self.finance_features)
        else:
            scaled_feature = self.finance_features

        # Plots the first two features
        # Can change this to plot some other feature - add a new option which
        # specifies which feature to plot maybe
        for f in scaled_feature:
            plt.scatter( f[0], f[1] )
        plt.show()

        ### cluster here; create predictions of the cluster labels
        ### for the data and store them to a list called pred
        kmeans = KMeans(n_clusters=self.n_clusters)
        kmeans.fit(scaled_feature)
        pred = kmeans.predict(scaled_feature)

        ### rename the "name" parameter when you change the number of features
        ### so that the figure gets saved to a different file
        try:
            Draw(pred, scaled_feature, poi, mark_poi=False, name="clusters.pdf", f1_name= self.features_list[0], f2_name= self.features_list[1])
        except NameError:
            print "no predictions object named pred found, no clusters to plot"

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
    n = 3
    feature_1 = "salary"
    feature_2 = "exercised_stock_options"
    feature_3 = "total_payments"
    poi  = "poi"
    features_list = [poi, feature_1, feature_2, feature_3]
    f = ''
    scaled = False


    try:
        optlist, args = getopt.getopt(sys.argv[1:], "n:f:", ('debug'))
    except:
        usage()

    for o, a in optlist:
        if o in ('--debug',):
            debug = 1
        elif o == '-n':
            n = a
        elif o == '-f':
            f = a.split(',')
            features_list = [poi]
            features_list.extend(f)
        elif o == '--scaled':
            scaled = True


    # Initialize the script with the required variables
    job = K_means_cluster(n_clusters=n, features_list=features_list, scaled=scaled)

    # Run the script and if required, add the database
    if debug:
        job.run()
    else:
        job()
