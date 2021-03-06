#Breast Cancer Classification

#Importing Dataset
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Importing dataset
dataset= pd.read_csv('data.csv')
X= dataset.iloc[:, 2:32].values
y= dataset.iloc[:, 1].values

#Encoding dependent variable
from sklearn.preprocessing import LabelEncoder
le= LabelEncoder()
y= le.fit_transform(y)

#Splitting into training and test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test= train_test_split(X, y, test_size= 0.2)

#Feature Scaling
from sklearn.preprocessing import StandardScaler
sc_X= StandardScaler()
X_train= sc_X.fit_transform(X_train)
X_test= sc_X.transform(X_test)

#Dimensionality Reduction
from sklearn.decomposition import KernelPCA
kpca= KernelPCA(n_components= 2, kernel= 'rbf')
X_train= kpca.fit_transform(X_train)
X_test= kpca.transform(X_test)

#Fitting Naive Bayes
from sklearn.naive_bayes import GaussianNB
classifier= GaussianNB()
classifier.fit(X_train, y_train)

#Predicting results
y_pred= classifier.predict(X_test)
y_pred= (y_pred > 0.5)

#Confusion Matrix
from sklearn.metrics import confusion_matrix
cm= confusion_matrix(y_test, y_pred)

#Calculating accuracy
from sklearn.model_selection import cross_val_score
accuracies= cross_val_score(estimator= classifier, X= X_train, y= y_train, cv= 10, scoring= 'accuracy',
                            n_jobs= -1)
mean= accuracies.mean()
std= accuracies.std()

#Decode function
def decode(j):
    if j==1:
        return 'Malignant'
    else:
        return 'Benign'
    

#Visualising Training set results
from matplotlib.colors import ListedColormap
X_set, y_set= X_train, y_train
X1, X2= np.meshgrid(np.arange(start= X_set[:, 0].min() - 1, stop= X_set[:, 0].max() + 1, step= 0.01),
                    np.arange(start= X_set[:, 1].min() - 1, stop= X_set[:, 1].max() + 1, step= 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha= 0.75, cmap= ListedColormap(('green', 'red')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set==j, 0], X_set[y_set==j, 1], c= ListedColormap(('green', 'red'))(i),
                label= decode(j))

plt.title("Breast Cancer (Training Set)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.show()

#Visualising Test set results
from matplotlib.colors import ListedColormap
X_set, y_set= X_test, y_test
X1, X2= np.meshgrid(np.arange(start= X_set[:, 0].min() - 1, stop= X_set[:, 0].max() + 1, step= 0.01),
                    np.arange(start= X_set[:, 1].min() - 1, stop= X_set[:, 1].max() + 1, step= 0.01))
plt.contourf(X1, X2, classifier.predict(np.array([X1.ravel(), X2.ravel()]).T).reshape(X1.shape),
             alpha= 0.75, cmap= ListedColormap(('green', 'red')))
plt.xlim(X1.min(), X1.max())
plt.ylim(X2.min(), X2.max())

for i, j in enumerate(np.unique(y_set)):
    plt.scatter(X_set[y_set==j, 0], X_set[y_set==j, 1], c= ListedColormap(('green', 'red'))(i),
                label= decode(j))

plt.title("Breast Cancer (Test Set)")
plt.xlabel("PC1")
plt.ylabel("PC2")
plt.legend()
plt.show()