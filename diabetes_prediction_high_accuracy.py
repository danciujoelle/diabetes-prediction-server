# -*- coding: utf-8 -*-
"""diabetes-prediction-high-accuracy.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1zZrdRcc6EIxxDUvZwOqH7053s-vpdovE

# **Step 1: import the libraries**
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import confusion_matrix,classification_report,roc_curve,accuracy_score,auc
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from keras.utils import np_utils
from keras.models import Sequential, load_model
from keras.layers import Dense, Dropout, Activation, Conv2D,MaxPooling2D, Flatten
from imblearn.combine import SMOTETomek ##For upsampling

import pickle #for serialization
from sklearn.tree import DecisionTreeClassifier
from sklearn import metrics

"""# Step 2: import the **dataset**"""

dataset=pd.read_csv("Diabetes.csv")

title_mapping = {'YES':1,'NO':0}
dataset[' Class variable']=dataset[' Class variable'].map(title_mapping)

"""# **Checking how many result we have of each outcome**

Zeros Count in Data
"""

zeros=(X == 0).sum(axis=0)
zeros=pd.DataFrame(zeros)
zeros.columns=['Zeros Count']
# zeros.drop(' Class variable',inplace=True)
zeros.plot(kind='bar',stacked=True, figsize=(10,5),grid=True)

col=['n_pregnant','glucose_conc','bp','skin_len','insulin','bmi','pedigree_fun','age','Output']
dataset.columns=col
dataset.head()

diabetes_true_count = len(dataset.loc[dataset['Output'] == True])
diabetes_false_count = len(dataset.loc[dataset['Output'] == False])
(diabetes_true_count,diabetes_false_count)

"""# **Data** **Processing**

**Step 3: replace the null values with the respective mean **
"""

col=['glucose_conc','bp','insulin','bmi','skin_len']
for i in col:
    X[i].replace(0, np.nan, inplace= True)
X.isnull().sum()

def median_target(var):   
    temp = dataset[dataset[var].notnull()]
    temp = temp[[var, 'Output']].groupby(['Output'])[[var]].median().reset_index()
    return temp

median_target('glucose_conc')

median_target('bmi')

median_target('bp')

median_target('skin_len')

median_target('insulin')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['insulin'].isnull()), 'insulin'] = 102.5
dataset.loc[(dataset['Output'] == 1 ) & (dataset['insulin'].isnull()), 'insulin'] = 169.5
dataset.loc[(dataset['Output'] == 0 ) & (dataset['glucose_conc'].isnull()), 'glucose_conc'] = 107
dataset.loc[(dataset['Output'] == 1 ) & (dataset['glucose_conc'].isnull()), 'glucose_conc'] = 140
dataset.loc[(dataset['Output'] == 0 ) & (dataset['skin_len'].isnull()), 'skin_len'] = 27
dataset.loc[(dataset['Output'] == 1 ) & (dataset['skin_len'].isnull()), 'skin_len'] = 32
dataset.loc[(dataset['Output'] == 0 ) & (dataset['bp'].isnull()), 'bp'] = 70
dataset.loc[(dataset['Output'] == 1 ) & (dataset['bp'].isnull()), 'bp'] = 74.5
dataset.loc[(dataset['Output'] == 0 ) & (dataset['bmi'].isnull()), 'bmi'] = 30.1
dataset.loc[(dataset['Output'] == 1 ) & (dataset['bmi'].isnull()), 'bmi'] = 34.3

"""**Checking if the null values were replaced**"""

dataset.isnull().sum()

"""# **Step4: Checking the presence of outliers in the data using BOX PLOT**"""

plt.style.use('ggplot') # Using ggplot2 style visuals 

f, ax = plt.subplots(figsize=(11, 15))

ax.set_facecolor('#fafafa')
ax.set(xlim=(-.05, 200))
plt.ylabel('Variables')
plt.title("Overview Data Set")
ax = sns.boxplot(data = dataset, 
  orient = 'h', 
  palette = 'Set2')

"""**Correcting the outliers using the median**"""

sns.boxplot(dataset.n_pregnant)

dataset['n_pregnant'].value_counts()

median_target('n_pregnant')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['n_pregnant']>13), 'n_pregnant'] = 2
dataset.loc[(dataset['Output'] == 1 ) & (dataset['n_pregnant']>13), 'n_pregnant'] = 4

dataset['n_pregnant'].value_counts()

sns.boxplot(dataset.bp)

median_target('bp')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['bp']<40), 'bp'] = 70
dataset.loc[(dataset['Output'] == 1 ) & (dataset['bp']<40), 'bp'] = 74.5
dataset.loc[(dataset['Output'] == 0 ) & (dataset['bp']>103), 'bp'] = 70
dataset.loc[(dataset['Output'] == 1 ) & (dataset['bp']>103), 'bp'] = 74.5

sns.boxplot(dataset.bp)

sns.boxplot(dataset.skin_len)

median_target('skin_len')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['skin_len']>38), 'skin_len'] = 27
dataset.loc[(dataset['Output'] == 1 ) & (dataset['skin_len']>38), 'skin_len'] = 32
dataset.loc[(dataset['Output'] == 0 ) & (dataset['skin_len']<20), 'skin_len'] = 27
dataset.loc[(dataset['Output'] == 1 ) & (dataset['skin_len']<20), 'skin_len'] = 32

sns.boxplot(dataset.bmi)

median_target('bmi')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['bmi']>48), 'bmi'] = 30.1
dataset.loc[(dataset['Output'] == 1 ) & (dataset['bmi']>48), 'bmi'] = 34.3

sns.boxplot(dataset.pedigree_fun)

median_target('pedigree_fun')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['pedigree_fun']>1), 'pedigree_fun'] = 0.336
dataset.loc[(dataset['Output'] == 1 ) & (dataset['pedigree_fun']>1), 'pedigree_fun'] = 0.449

sns.boxplot(dataset.age)

median_target('age')

dataset.loc[(dataset['Output'] == 0 ) & (dataset['age']>61), 'age'] = 27
dataset.loc[(dataset['Output'] == 1 ) & (dataset['age']>61), 'age'] = 36

"""# **Step 4 : Splitting the data**"""

X = dataset.drop(['Output'], 1)
y = dataset['Output']

x_train,x_test,y_train,y_test=train_test_split(X,y,test_size=0.25,random_state=0)

print(x_train)

print(y_train)

"""# **Support Vector Machine with Radial Basis Function Kernel**"""

model=SVC(kernel='rbf')
model.fit(x_train,y_train)

y_pred=model.predict(x_test)

accuracy_score(y_test,y_pred)

confusion_matrix(y_test,y_pred)

print(classification_report(y_test,y_pred))

"""# **Random Forest Classifier**"""

classifier=RandomForestClassifier()
x_train = x_train.values
classifier.fit(x_train,y_train)

Y_pred=classifier.predict(x_test)
confusion_matrix(y_test,Y_pred)

accuracy_score(y_test,Y_pred)

print(classification_report(y_test,Y_pred))

fpr,tpr,_=roc_curve(y_test,Y_pred)
#calculate AUC
roc_auc=auc(fpr,tpr)
print('ROC AUC: %0.2f' % roc_auc)
#plot of ROC curve for a specified class
plt.figure()
plt.plot(fpr,tpr,label='ROC curve(area= %2.f)' %roc_auc)
plt.plot([0,1],[0,1],'k--')
plt.xlim([0.0,1.0])
plt.ylim([0.0,1.05])
plt.xlabel('False positive rate')
plt.ylabel('True positive rate')
plt.title('ROC curve')
plt.legend(loc='lower right')
plt.grid()
plt.show()

model_file=open("modelupdated.pkl","wb")##to serialize
pickle.dump(classifier,model_file)
model_file.close()##always remember to close it

"""# **Decision Tree**"""

dtree = DecisionTreeClassifier()
dtree.fit(x_train, y_train)

predictions = dtree.predict(x_test)
print("Accuracy Score =", format(metrics.accuracy_score(y_test,predictions)))

"""# **XGBoost**"""

from xgboost import XGBClassifier

xgb_model = XGBClassifier(gamma=0)
xgb_model.fit(x_train, y_train)

xgb_pred = xgb_model.predict(x_test)
print("Accuracy Score =", format(metrics.accuracy_score(y_test, xgb_pred)))