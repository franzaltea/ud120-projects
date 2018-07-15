#!/usr/bin/python

""" 
    Starter code for exploring the Enron dataset (emails + finances);
    loads up the dataset (pickled dict of dicts).

    The dataset has the form:
    enron_data["LASTNAME FIRSTNAME MIDDLEINITIAL"] = { features_dict }

    {features_dict} is a dictionary of features associated with that person.
    You should explore features_dict as part of the mini-project,
    but here's an example to get you started:

    enron_data["SKILLING JEFFREY K"]["bonus"] = 5600000
    
"""

import pickle, time, getopt, sys


script_name = 'explore_enron_data'

#################################################################
#Functions and classes
#################################################################
def usage():
    print """
Usage:\n
%s [--debug]
    - debug     currently does not do anything
    """ % sys.argv[0]
    sys.exit(1)
    
class Explore_enron_data:

    # Constructor
    def __init__(self):
        pass

    # Logging function, just keep it simple for now and print text
    def log(self, text):
        print text

    # Main Script Logic
    def run(self):
        start_time = time.time()
        self.log("****** {0} has started. ******".format(script_name))

        self.enron_data = pickle.load(open("../final_project/final_project_dataset.pkl", "r"))

        print "Number of people: {0}".format(len(self.enron_data))

        number_of_poi = 0
        number_of_known_salary = 0
        number_of_known_email = 0
        number_of_unknown_payments = 0
        n_of_poi_up = 0
        for key, value in self.enron_data.iteritems():
            if value['poi']:
                number_of_poi += 1
            if value['salary'] != 'NaN':
                number_of_known_salary += 1
            if value['email_address'] != 'NaN':
                number_of_known_email += 1
            if value['total_payments'] == 'NaN':
                number_of_unknown_payments += 1
                if value['poi']:
                    n_of_poi_up += 1
            
            if key == 'PRENTICE JAMES':
                print "Total stock value for {0} is ${1}".format(key, value['total_stock_value'])
            elif key == 'SKILLING JEFFREY K':
                print "Stop option value for {0} is ${1}".format(key, value['exercised_stock_options'])
            elif key == 'COLWELL WESLEY':
                print "Total emails from {0} to POI is {1}".format(key, value['from_this_person_to_poi'])

            if key in ('SKILLING JEFFREY K', 'LAY KENNETH L', 'FASTOW ANDREW S'):
                print "Total Payment for {0} is ${1}".format(key, value['total_payments'])

        print "Number of POI: {0}".format(number_of_poi)
        print "Number of Known Salary: {0}".format(number_of_known_salary)
        print "Number of Known Email: {0}".format(number_of_known_email)
        print "Number of unknown payments is {0} which is {1}% from total".format(
                number_of_unknown_payments, float(number_of_unknown_payments)/len(self.enron_data)*100)
        print "Number of pois with unknown payment is {0} which is {1}% from total".format(
                n_of_poi_up, float(n_of_poi_up)/number_of_poi*100)
        
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

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "n:", ('debug'))
    except:
        usage()

    for o, a in optlist:
        if o in ('--debug',):
            debug = 1

    # Initialize the script with the required variables
    job = Explore_enron_data()

    # Run the script
    if debug:
        job.run()
    else:
        job()