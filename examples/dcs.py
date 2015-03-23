from brew.selection.dynamic.ola import OLA
from brew.selection.dynamic.ola import OLA2
from brew.selection.dynamic.lca import LCA
from brew.selection.dynamic.lca import LCA2
from brew.selection.dynamic.knora import *
from brew.selection.dynamic.probabilistic import *

from brew.generation.bagging import Bagging
from brew.base import EnsembleClassifier

import numpy as np

import sklearn
from sklearn import datasets
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import zero_one_loss
from sklearn.cross_validation import train_test_split

N = 1000
dt = DecisionTreeClassifier(max_depth=9, min_samples_leaf=1)

X, y = datasets.make_hastie_10_2(n_samples=N, random_state=1)
for i, yi in enumerate(set(y)):
    y[y == yi] = i

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
X_train, X_val, y_train, y_val = train_test_split(X_train, y_train, test_size=0.30)

bag = Bagging(base_classifier=dt, n_classifiers=10)
bag.fit(X_val, y_val)


dcs_list = [OLA(X_val, y_val),
            LCA(X_val, y_val),
            KNORA_ELIMINATE(X_val, y_val), 
            KNORA_UNION(X_val, y_val),
            Priori(X_val, y_val),
            Posteriori(X_val, y_val)
            ]

dcs_names = ['ola', 'lca', 'KE', 'KU', 'aPriori', 'aPosteriori']


print('-----------------ERROR RATE----------------------')
for dcs, name in zip(dcs_list, dcs_names):
    mcs = EnsembleClassifier(bag.ensemble, selector=dcs)
    y_pred = mcs.predict(X_test)
    print('{}, {}'.format(name, zero_one_loss(y_pred, y_test)))
print ('------------------------------------------------')
