import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
import pickle
import csv


    
dataset=pd.read_csv('training-0.csv')
dataset['Label']=dataset['Label'].replace([0.0,1.0,2.0,3.0],['fear','sad','joy','anger'])
dataset=dataset.dropna()
X=dataset.drop(["Label"],axis=1)
Y=dataset["Label"]
gbModel=GradientBoostingClassifier(n_estimators=120,max_features="sqrt",random_state=42, subsample=1.0)
gbModel.fit(X,Y)
importance=gbModel.feature_importances_
featureCek=pd.Series(importance)
featurePenting=featureCek.nlargest(235)
indexFeaturePenting=featurePenting.index.array
# print(featurePenting)
pd.DataFrame(indexFeaturePenting).to_csv('sample.csv')  

X_fit=X.iloc[:,indexFeaturePenting]
Xtrain,Xtest,Ytrain,Ytest=train_test_split(X_fit,Y,test_size=0.1,random_state=42, stratify=Y)
# print (type(X_fit))
# print (list(X_fit))
        # print(Ytest)
        # import collections
        # counter=collections.Counter(Ytest)
        # print(counter)

gbModel.fit(Xtrain,Ytrain)

fileModel='modelGB.sav'
pickle.dump(gbModel,open(fileModel,'wb'))


loadModel=pickle.load(open(fileModel,'rb'))
hasil=loadModel.score(Xtest,Ytest)

print(hasil)