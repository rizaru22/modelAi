import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import csv

namaFile='rangking_fitur_estimator1.csv'
with open(namaFile,'a',newline='')as f:
    writer=csv.writer(f,lineterminator='\n')
    header=['N Estimator','Jumlah Fitur','Nilai Akurasi']
    writer.writerow(header)
    
dataset=pd.read_csv('training-1.csv')
dataset['Label']=dataset['Label'].replace([0.0,1.0,2.0,3.0],['fear','sad','joy','anger'])
dataset=dataset.dropna()
X=dataset.drop(["Label"],axis=1)
Y=dataset["Label"]
for n_estimate in range(100,150):
    gbModel=GradientBoostingClassifier(n_estimators=n_estimate,max_features="sqrt",random_state=42, subsample=1.0)
    gbModel.fit(X,Y)

    importance=gbModel.feature_importances_
    featureCek=pd.Series(importance)
    for jumlahFeature in range(230,260):
        featurePenting=featureCek.nlargest(jumlahFeature)
        indexFeaturePenting=featurePenting.index.array


        X_fit=X.iloc[:,indexFeaturePenting]
        Xtrain,Xtest,Ytrain,Ytest=train_test_split(X_fit,Y,test_size=0.1,random_state=42, stratify=Y)
        # print(Ytest)
        # import collections
        # counter=collections.Counter(Ytest)
        # print(counter)

        gbModel.fit(Xtrain,Ytrain)

        fileModel='modelGB.sav'
        pickle.dump(gbModel,open(fileModel,'wb'))


        loadModel=pickle.load(open(fileModel,'rb'))
        hasil=loadModel.score(Xtest,Ytest)

        with open(namaFile,'a',newline='')as f:
            writer=csv.writer(f,lineterminator='\n')
            data=[n_estimate,jumlahFeature,hasil]
            writer.writerow(data)