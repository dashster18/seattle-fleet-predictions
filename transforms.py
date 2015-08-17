import pandas as pd
import datetime

# The script MUST contain a function named azureml_main
# which is the entry point for this module.
#
# The entry point function can contain up to two input arguments:
#   Param<dataframe1>: a pandas.DataFrame
#   Param<dataframe2>: a pandas.DataFrame
def azureml_main(dataframe1 = None, dataframe2 = None):

    # Execution logic goes here

    # AzureML internally converts DateTimes to time from epoch
    # When passing into a python module.
    #
    # Here we reconvert back to DateTime
    dataframe1['SaleDate'] = dataframe1['SaleDate'].map(lambda d: datetime.datetime.fromtimestamp(d))

    # Read in the data
    #
    names = ['EquipID','Year','Make','Model','Description','Dept','SalePrice','SaleDate','AuctionHouse']
    sold = dataframe1
    

    # Calculate the Age of the vehicle and only take the useful fields
    #
    useful = sold[['Year', 'Make', 'Model', 'SalePrice', 'SaleDate', 'AuctionHouse']]
    useful['SaleDate'] = pd.to_datetime(useful['SaleDate'])
    useful['SaleDateYear'] = useful['SaleDate'].map(lambda d: d.year)
    useful['VehicleAge'] = useful['SaleDateYear'] - useful['Year']
    useful = useful[['VehicleAge', 'SalePrice', 'AuctionHouse', 'Make', 'Model']]


    # Turn the categorical variables (AuctionHouse, Make, and Model) into
    # indicator variables
    #
    data = useful[['SalePrice', 'VehicleAge']]
    AHs = pd.get_dummies(useful['AuctionHouse'], prefix='AH')
    makes = pd.get_dummies(useful['Make'], prefix='Make')
    models = pd.get_dummies(useful['Model'], prefix='Model')

    # Join all of the continuous variables with the indicator variables
    # to produce a design matrix to feed into ML models
    #
    data = data.join(AHs, how='inner')
    data = data.join(makes, how='inner')
    data = data.join(models, how='inner')

    dataframe1 = data

    # If a zip file is connected to the third input port is connected,
    # it is unzipped under ".\Script Bundle". This directory is added
    # to sys.path. Therefore, if your zip file contains a Python file
    # mymodule.py you can import it using:
    # import mymodule
    
    # Return value must be of a sequence of pandas.DataFrame
    return dataframe1,

