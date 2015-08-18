import pandas as pd
import datetime

def generate_features(dataframe = None):
    names = ['EquipID','Year','Make','Model','Description','Dept','SalePrice','SaleDate','AuctionHouse']
    sold = dataframe
    

    # Calculate the Age of the vehicle and only take the useful fields
    #
    useful = sold[['Year', 'Make', 'Model', 'SalePrice', 'SaleDate', 'AuctionHouse']]
    useful['SaleDate'] = pd.to_datetime(useful['SaleDate'])
    useful['SaleDateYear'] = useful['SaleDate'].map(lambda d: d.year)
    useful['VehicleAge'] = useful['SaleDateYear'] - useful['Year']
    useful = useful[['VehicleAge', 'SalePrice', 'AuctionHouse', 'Make', 'Model']]

    # Turn the feature matrix into a representation
    # that a standard scikit-learn algorithm can handle
    #
    data = pd.get_dummies(useful,
                          prefix=['AH', 'Make', 'Model'],
                          columns=['AuctionHouse', 'Make', 'Model'])

    return data
