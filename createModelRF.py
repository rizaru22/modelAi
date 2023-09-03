import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

dataset=pd.read_csv('training.csv')
dataset['Label']=dataset['Label'].replace([0.0,1.0,2.0,3.0],['fear','sad','joy','anger'])
dataset=dataset.dropna()
X=dataset.drop(["Label"],axis=1)
Y=dataset["Label"]
rfModel=RandomForestClassifier(n_estimators=100,max_features="sqrt",random_state=42)
rfModel.fit(X,Y)

importance=rfModel.feature_importances_
featureCek=pd.Series(importance)
featurePenting=featureCek.nlargest(256)
indexFeaturePenting=featurePenting.index.array

X_fit=X.iloc[:,indexFeaturePenting]
Xtrain,Xtest,Ytrain,Ytest=train_test_split(X_fit,Y,test_size=0.3,random_state=42)
rfModel.fit(Xtrain,Ytrain)

fileModel='modelRF.sav'
pickle.dump(rfModel,open(fileModel,'wb'))


loadModel=pickle.load(open(fileModel,'rb'))
hasil=loadModel.score(Xtest,Ytest)
print(hasil)