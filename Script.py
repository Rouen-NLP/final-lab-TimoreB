#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 18 15:06:57 2018

@author: tbernard
"""

#%%
import numpy as np 
import pandas as pd
import os
import seaborn as sns
import sklearn
from sklearn.feature_extraction.text import CountVectorizer,TfidfVectorizer,TfidfTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.naive_bayes import MultinomialNB
from sklearn.neural_network import MLPClassifier
import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.pipeline import Pipeline
from pprint import pprint
from time import time
import logging


#%%

#On définit deux fonctions pour entrainer et tester notre modele bayesien

def vectorizer(X_train, max_features = 2000, max_df = 1.0):

    vectorizer = CountVectorizer(max_features=max_features,max_df=max_df)
    vectorizer.fit(X_train)
    
    return vectorizer

def model_NB_train(X_train,y_train,vectorizer):
    # On vectorize nos tweets
    X_train_counts = vectorizer.transform(X_train)
    
    # On entraine nos Naives Bayes
    model = MultinomialNB()
    model.fit(X_train_counts,y_train)

    y_pred_train = model.predict(X_train_counts)
   
    print("Evalution (Phase de train) : ",accuracy_score(y_train,y_pred_train))
    return model

def model_test(model,vectorizer,X_test,y_test):
    
    X_test_counts = vectorizer.transform(X_test)

    y_pred_test = model.predict(X_test_counts)
    
    print("Evalution (Phase de test) : ",accuracy_score(y_test,y_pred_test),"\n")
    print(classification_report(y_test,y_pred_test))
    print(confusion_matrix(y_test,y_pred_test))
    return model

model = model_NB_train(X_train,y_train, vectorizer)
model_test(model,vectorizer,X_test,y_test)





def MLP_train(layer_size,activation, vectorizer, X_train, y_train):
    model = MLPClassifier(10,activation=activation,solver='adam')
    X_train_counts = vectorizer.transform(X_train)
    model.fit(X_train_counts,y_train)
    
    y_pred_train = model.predict(X_train_counts)
    
    print("Evalution (Phase de train) : ",accuracy_score(y_train,y_pred_train))

    
    return model

model = MLP_train(5,'tanh',vectorizer,X_train,y_train)
model_test(model,vectorizer,X_test,y_test)
#%%

# On fait le grid search pour trouver la meilleure configuration
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')


pipeline = Pipeline([
    ('vect', CountVectorizer()),
    ('mlp', MLPClassifier()),
])


parameters = {
    'vect__max_df': (0.25, 0.5, 0.75, 1.0),
    'vect__max_features': (500,2000, 5000),
    'mlp__activation': ('logistic','tanh','relu'),
    'mlp__hidden_layer_sizes' : (2,10,50)
}

grid_search = GridSearchCV(pipeline, parameters, n_jobs=-1, verbose=2)

print("Performing grid search...")
print("pipeline:", [name for name, _ in pipeline.steps])
print("parameters:")
pprint(parameters)
t0 = time()
grid_search.fit(X_test, y_test)
print("done in %0.3fs" % (time() - t0))
print()

print("Best score: %0.3f" % grid_search.best_score_)
print("Best parameters set:")
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))
#%%

if __name__ == '__main__':
        
        
    # Chargement des données
    data = pd.read_csv('../nlp-labs/tobacco-lab/data/Tobacco3482.csv')
    data.head(10)
    
    #On affiche un diagramme d'apparation de chaque catégorie dans notre set de données
    g = sns.countplot(data['label'],orient='h')
    
    #Comme la fréquence d'apparition me parait, inégale, je choisie d'afficher un camembert pour mieux 
    # se rendre compte des disparité
    unique, counts = np.unique(data['label'],return_counts=True)
    plt.pie(counts,labels=unique)
    plt.show()
    
    
    list_files = []
    for root, dirs, files in os.walk("./data", topdown=False):
        for name in files:
            if ".txt" in os.path.join(root, name) :
                list_files.append(os.path.join(root, name))
    
    list_text = []
    for file in list_files:
        file_object = open(file,'r')
        list_text.append(file_object.read())
        
    dict_data = {}
    for i in range(len(data['img_path'])):
        dict_data['../nlp-labs/tobacco-lab/data/'+data['img_path'][i].replace('jpg','txt')] = data['label'][i] 
    X = []
    y = []
    for i in dict_data:
        file_object = open(i,"r")
        X.append(file_object.read())
        file_object.close()
        y.append(dict_data[i])
        
    # On split nos données
    X_train, X_test,y_train,  y_test = train_test_split(X,y, test_size=0.2)
    X_train, X_dev, y_train, y_dev = train_test_split(X_train, y_train, test_size = 0.25)
        
    vect = vectorizer(X_train,5000,0.75)
    model = MLP_train(50,'relu',vect,X_train,y_train)
    model_test(model,vectorizer,X_test,y_test)
