import pandas as pd
from sklearn.multioutput import MultiOutputClassifier
from sklearn.linear_model import LogisticRegression

# test example
# 10 & 0 = none
# 1 = leona
# 2 = braum
# 3 = yuumi
# 4 = taric

# some repositioning and adding (buying) taric
dic = {'par_1': [0, 10, 0, 10, 0, 10, 0],
       'par_2': [10, 10, 10, 3, 3, 3, 4],
       'par_3': [10, 1, 1, 1, 1, 10, 10],
       'par_4': [1, 10, 2, 2, 2, 2, 2],
       'par_5': [2, 2, 10, 10, 10, 1, 1],
       'par_6': [3, 3, 3, 10, 4, 4, 3],
       'par_7': [0, 10, 0, 10, 0, 10, 0],
       'outcome1': [0, 10, 0, 10, 0, 10, 0],
       'outcome2': [10, 10, 3, 3, 3, 4, 4],
       'outcome3': [1, 1, 1, 1, 10, 10, 10],
       'outcome4': [10, 2, 2, 2, 2, 2, 2],
       'outcome5': [2, 10, 10, 10, 1, 1, 1],
       'outcome6': [3, 3, 10, 4, 4, 3, 10],
       'outcome7': [0, 10, 0, 10, 0, 10, 0]}

df = pd.DataFrame(dic)

variables = df.iloc[:,0:7]
results = df.iloc[:, 7:14]

# print(df)

multi_output_clf = MultiOutputClassifier(LogisticRegression(solver='lbfgs'))
multi_output_clf.fit(results,variables)

prediction = multi_output_clf.predict([[3, 2, 10, 10, 10, 10, 1]])

print(prediction)