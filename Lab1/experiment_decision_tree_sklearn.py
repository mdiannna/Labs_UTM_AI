from sklearn.tree import DecisionTreeClassifier
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import numpy as np

df = pd.read_csv('dataset.csv')
print(df.head())

clf = DecisionTreeClassifier(random_state=0)
X = df[['Skin Color', 'Language', 'Comes from', 'Nr of legs', 'Nr of arms', 'Clothes', 'Wears sunglasses', 'Walking speed', 'Weight', 'Hair color', 'Wears mask']]
y = df['Type'].values.flatten()

print("x:", X)
print("y:", y)


X = X.fillna('-')

print("x:", X)
print("y:", y)

X_tr = X.apply(LabelEncoder().fit_transform)

X_tr[X_tr=='-']  = np.nan

print("X transf:", X_tr)
print(clf.fit(X_tr, y))

y_pr = clf.predict(X_tr)
print("Y_pr:", y_pr)
print("Yreal:", y)

X_test = [[0,2,4,0,0,0,2,1,0,3,1]]
print("y_real:", "Loonie", "y pred:", clf.predict(X_test))

X_test = [[0,2,4,0,0,0,2,1,0,0,0]]
print("y_real:", "Loonie", "y pred:", clf.predict(X_test))

X_test = [[0,0,4,0,0,0,2,1,0,0,0]]
print("y_real:", "Loonie", "y pred:", clf.predict(X_test))
