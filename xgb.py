# -*- coding: utf-8 -*-
"""
Created on Sun Oct 23 14:58:55 2022

@author: dberf
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.preprocessing import scale, StandardScaler
from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score 
from sklearn.metrics import confusion_matrix,classification_report, accuracy_score,mean_squared_error,r2_score, roc_auc_score,roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from xgboost import XGBClassifier

import warnings
warnings.filterwarnings("ignore" , category=DeprecationWarning)
warnings.filterwarnings("ignore" , category=FutureWarning)


data=pd.read_csv("diabetes.csv")

y = data["Outcome"]
x = data.drop(["Outcome"], axis=1)
x_train, x_test, y_train, y_test=train_test_split(x,y,test_size=0.30,random_state=42)

xgb_model=XGBClassifier().fit(x_train,y_train)
y_pred=xgb_model.predict(x_test)
print("Accuracy:" , accuracy_score(y_test, y_pred))

xgb=XGBClassifier()

xgb_params={"n_estimators":[100,500,1000,2000],
            "subsample":[0.6,0.8,1],
            "max_depth":[3,5,7],
            "learning_rate":[0.1,0.001,0.01]}

xgb_cv_model=GridSearchCV(xgb, xgb_params,cv=10, n_jobs=-1,verbose=2).fit(x_train, y_train)
print("Best Params:" , xgb_cv_model.best_params_)

#final model
xgb_tuned_model=XGBClassifier(learning_rate= 0.001, max_depth= 5, n_estimators= 2000, subsample= 1).fit(x_train, y_train)
y_pred_tuned=xgb_tuned_model.predict(x_test)
print("Tuned Accuracy:" , accuracy_score(y_test, y_pred_tuned))


#degisken onem duzeyleri
feature_imp=pd.Series(xgb_tuned_model.feature_importances_,index=x_train.columns).sort_values(ascending=False)
sns.barplot(x=feature_imp, y=feature_imp.index)
plt.xlabel("Degisken Onem Skorlari")
plt.ylabel("Degiskenler")
plt.title("Degisken Onem Duzeyleri")
plt.show()
