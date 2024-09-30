import pandas as pd
import numpy as np
import re

from scipy.stats import skew
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

class DataLoader(object):
    def fit(self, dataset):
        self.dataset = dataset.copy()

    def load_data(self):
        
        # columns combination
        self.dataset['TotalSF'] = self.dataset['TotalBsmtSF'] + self.dataset['1stFlrSF'] + self.dataset['2ndFlrSF']
        
        # fill Nan with custom
        for col in ('PoolQC', 'MiscFeature', 'Alley', 'FireplaceQu', 'Fence', 'MSSubClass', 
            'GarageType', 'GarageFinish', 'GarageQual', 'GarageCond', 'MasVnrType',
            'BsmtQual', 'BsmtCond', 'BsmtExposure', 'BsmtFinType1', 'BsmtFinType2'):
        
            self.dataset[col] = self.dataset[col].fillna('None')
        
        self.dataset["Functional"] = self.dataset["Functional"].fillna('Typ')
        
        # fill Nan with mode
        for col in ('MSZoning', 'Electrical', 'KitchenQual', 
            'Exterior1st', 'Exterior2nd', 'SaleType'):
            
            self.dataset[col] = self.dataset[col].fillna(self.dataset[col].mode()[0])
        
        # fill Nan with median
        self.dataset["LotFrontage"] = self.dataset.groupby("Neighborhood")["LotFrontage"].transform(lambda x: x.fillna(x.median()))
        
        # fill Nan with zero
        for col in ('GarageYrBlt', 'GarageArea', 'GarageCars', 'MasVnrArea',
           'BsmtFinSF1', 'BsmtFinSF2', 'BsmtUnfSF','TotalBsmtSF', 
            'BsmtFullBath', 'BsmtHalfBath'):
            
            self.dataset[col] = self.dataset[col].fillna(0)
        
        # drop columns
        drop_elements = ['Id', 'Utilities']

        self.dataset = self.dataset.drop(drop_elements, axis=1)
        
        #drop outliers
        self.dataset = self.dataset.drop(self.dataset[(self.dataset['GrLivArea']>4000) & (self.dataset['SalePrice']<300000)].index)
        
        #log transform skewed columns
        numeric_feats = self.dataset.dtypes[self.dataset.dtypes != "object"].index
        
        skewed_feats = self.dataset[numeric_feats].apply(lambda x: skew(x.dropna())).sort_values(ascending=False)
        skewness = pd.DataFrame({'Skew' :skewed_feats})
        
        skewness = skewness[abs(skewness) > 0.75]
        skewed_index = skewness.index
        
        self.dataset[skewed_index] = np.log1p(self.dataset[skewed_index])
        
        # encode labels
        lbl = LabelEncoder()
        
        cols = ('FireplaceQu', 'BsmtQual', 'BsmtCond', 'GarageQual', 'GarageCond', 
        'ExterQual', 'ExterCond','HeatingQC', 'PoolQC', 'KitchenQual', 'BsmtFinType1', 
        'BsmtFinType2', 'Functional', 'Fence', 'BsmtExposure', 'GarageFinish', 'LandSlope',
        'LotShape', 'PavedDrive', 'Street', 'Alley', 'CentralAir', 'MSSubClass', 'OverallCond', 
        'YrSold', 'MoSold')
        
        # process columns, apply LabelEncoder to categorical features
        for c in cols:
            lbl.fit(self.dataset[c]) 
            self.dataset[c] = lbl.transform(self.dataset[c])
        
        # apply one-hot-encoding
        self.dataset = pd.get_dummies(self.dataset)
        
        return self.dataset
        
    def split_data(self, test_size = 0.2, random_state = 13):
        self.train, self.val = train_test_split(self.dataset, test_size = test_size, random_state = random_state)
        
        return self.train, self.val