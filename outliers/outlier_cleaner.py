#!/usr/bin/python


def outlierCleaner(predictions, ages, net_worths):
    """
        Clean away the 10% of points that have the largest
        residual errors (difference between the prediction
        and the actual net worth).

        Return a list of tuples named cleaned_data where 
        each tuple is of the form (age, net_worth, error).
    """
    
    cleaned_data = []

    least_squares = (net_worths - predictions)**2
    cleaned_data = [(ages[i], net_worths[i], least_squares[i]) for i in range(0,len(ages))]
    cleaned_data.sort(key=lambda x: x[2])
    remove_index = int(len(ages)*0.90)


    return cleaned_data[0:remove_index]

