import joblib
import numpy as np
import pandas as pd
from sklearn import svm
from sklearn.svm import OneClassSVM
from sklearn.model_selection import cross_val_score, train_test_split, GridSearchCV
from sklearn import metrics
pd.options.mode.chained_assignment = None 

#Leximi i te dhenave nga Dataset.csv 
read_data = pd.read_csv(r"C:\Users\Administrator\OneDrive\Desktop\Dataset.csv", nrows=200, engine="python")

#Lista e emrave te kolonave ne DataFrame qe duhet te merren parasysh
applicable_features = ["ssid_name",
                       "phy_type_id",
                       "capabilities",
                       "channel_center_freq_khz",
                       "connection_mode",
                       "authentication",
                       "encryption",
                       "vendor_name",
                       "bssid",
                       "mac",
                       "result"]

#Filtrimi i kolonave te DataFrame per te perfshire vetem kolonat e listuara me larte
read_data = read_data[applicable_features]
read_data.info()

#Rishikimi i DataFrame-it
read_data.head()

#Krijimi nje DataFrame te re qe permban vetem kolonen 'authentication' te read_data DataFrame
data = pd.DataFrame(read_data['authentication'])

#Definimi i funksionit per hashimin e kolonave 
def hash_col(df, col, N):
    cols = [col + "_" + str(i) for i in range(N)]

    def xform(x):
        tmp = [0 for i in range(N)]
        tmp[hash(x) % N] = 1
        return pd.Series(tmp,index=cols)
         
    df[cols] = df[col].apply(xform)
    return df.drop(col,axis=1)

#DataFrame qe rezulton sipas funksionit hash_col printohet ne ekran dhe me pas lidhen DataFrames 'data1' me 'read_data'
print(hash_col(data, 'authentication',8))
read_data = pd.concat([read_data,data],axis=1)
print(read_data)
print(read_data.info())

