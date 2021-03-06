# Import models from sklearn
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.svm import NuSVC
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import BaggingClassifier
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from datetime import datetime
import os
from sklearn.ensemble import VotingClassifier
from cfg import ml_cfg

from feature_processing_3 import load_and_process_data_set

df_train, df_test = load_and_process_data_set()


def prep_evidence(df, feat):
    primary_list = df[feat].values.tolist()
    evidence_list = []
    for ev in primary_list:
        temp = []
        for element in ev:
            if type(element) != list:
                temp.append(element)
            else:
                for number in element:
                    temp.append(number)
        evidence_list.append(temp)
    return evidence_list

features = ['Sex', 'Age_StdSc', 'Pclass_Scale', 'Fare_StdSc', 'SibSp', 'Parch']

X_train = prep_evidence(df_train, features)
y_train = df_train["Survived"].values.tolist()

X_test = prep_evidence(df_test, features)

# Split the data randomly into training and test set
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.3, stratify=y_train)#, random_state=50)

# Specify the models
dtc = DecisionTreeClassifier(criterion=ml_cfg["dtc"]["criterion"], max_features=ml_cfg["dtc"]["max_features"])

knn = KNeighborsClassifier(n_neighbors=ml_cfg["knn"]["n_neighbors"], weights=ml_cfg["knn"]["weights"],
                           algorithm=ml_cfg["knn"]["algorithm"], leaf_size=ml_cfg["knn"]["leaf_size"])

svc = SVC(kernel=ml_cfg["svc"]["kernel"], gamma=ml_cfg["svc"]["gamma"], probability=ml_cfg["svc"]["probability"],
          C=ml_cfg["svc"]["C"])

nusvc = NuSVC(nu=ml_cfg["nusvc"]["nu"], kernel=ml_cfg["nusvc"]["kernel"], gamma=ml_cfg["nusvc"]["gamma"],
              probability=ml_cfg["nusvc"]["probability"])

rf = RandomForestClassifier(n_estimators=ml_cfg["rf"]["n_estimators"], max_depth=ml_cfg["rf"]["max_depth"],
                            min_samples_leaf=ml_cfg["rf"]["min_samples_leaf"], criterion=ml_cfg["rf"]["criterion"],
                            max_features=ml_cfg["rf"]["max_features"])

gbc = GradientBoostingClassifier(n_estimators=ml_cfg["gbc"]["n_estimators"], learning_rate=ml_cfg["gbc"]["learning_rate"],
                                 criterion=ml_cfg["gbc"]["criterion"], max_depth=ml_cfg["gbc"]["max_depth"],
                                 loss=ml_cfg["gbc"]["loss"])

bc = BaggingClassifier(base_estimator=svc)

abc = AdaBoostClassifier(base_estimator=dtc, algorithm="SAMME")

eclf = VotingClassifier(estimators=[('knn', knn), ('svc', svc), ('nusvc', nusvc), ("rf", rf), ("gbc", gbc), ("bc", bc)],
                        voting='hard')

# Select and fit model
model = eclf
model.fit(X_train, y_train)

# Make predictions on the testing set
predictions = model.predict(X_val)

# Compute how well we performed
correct = (y_val == predictions).sum()
incorrect = (y_val != predictions).sum()
total = len(predictions)

# Print results
print(f"Results for model {type(model).__name__}")
print(f"Correct: {correct}")
print(f"Incorrect: {incorrect}")
print(f"Accuracy: {100 * correct / total:.2f}%")