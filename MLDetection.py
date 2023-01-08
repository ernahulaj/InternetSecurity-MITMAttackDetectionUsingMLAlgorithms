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

data1 = pd.DataFrame(read_data['encryption'])
print(hash_col(data1, 'encryption',5))
read_data = pd.concat([read_data,data1],axis=1)

data2 = pd.DataFrame(read_data['connection_mode'])
print(hash_col(data2, 'connection_mode',8))
read_data = pd.concat([read_data,data2],axis=1)

#Filtrimi per te perfshire vetem kolonat qe kane vleren 0 
target=read_data['result']
outliers = target[target == 0]  
print("outliers.shape", outliers.shape)  
print("outlier fraction", outliers.shape[0]/target.shape[0])

read_data.info()

# Lista e emrave te kolonave qe do te permbaje DataFrame
applicable_features1 = ["authentication_0",
                        "authentication_1",
                        "authentication_3",
                        "authentication_3",
                        "authentication_4",
                        "authentication_5",
                        "authentication_6",
                        "authentication_7",
                        "encryption_0",
                        "encryption_1",
                        "encryption_2",
                        "encryption_3",
                        "encryption_4",
                        "connection_mode_0",
                        "connection_mode_1",
                        "connection_mode_2",
                        "phy_type_id",
                        "capabilities",
                        "channel_center_freq_khz",
                        "mac"]

# Normalizimi i te dhenave (konvertimi mes tipeve te te dhenave per eficience)
read_data['channel_center_freq_khz'] = read_data['channel_center_freq_khz'].astype(float)
read_data['mac'] = read_data['mac'].astype(float)
read_data['phy_type_id'] = read_data['phy_type_id'].astype(float)
read_data['capabilities'] = read_data['capabilities'].astype(float)

# Filtrimi i kolonave
read_data = read_data[applicable_features1]
read_data.info()
print("read_data.shape ", read_data.shape)
print(read_data)

# Ndarja e read_data dhe target data ne training dhe test sets
# Parametri train_size percakton madhesine e training set si 80% e data
train_data, test_data, train_target, test_target = train_test_split(read_data, target, train_size=0.8)
print(test_data)

# Proporcioni i outliers ne dataset
nu = outliers.shape[0] / target.shape[0]
print("The calculated values of nu is:", nu)

# Anomaly detection dhe Classification si ML Algorithms
model = svm.OneClassSVM(nu=nu, kernel='rbf', gamma=0.00005)
model.fit(train_data)
