import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

data = pd.read_csv('train.csv').as_matrix()

clf = DecisionTreeClassifier()

# training data set
xtrain = data[0:38000, 1:]
train_label = data[0:38000, 0]
clf.fit(xtrain, train_label)

# testing the trained model
xtest = data[38000:, 1:]
actual_value = data[38000:, 0]

f, axarr = plt.subplots(3, 3)
for i in range(0, 3):
    for j in range(0, 3):
        testDigit = xtest[(i + 1) * (j + 1)]
        testDigit.shape = (28, 28)
        axarr[i, j].imshow(255 - testDigit, cmap='gray')
        axarr[i, j].set_title(clf.predict([xtest[(i + 1) * (j + 1)]]))

f.subplots_adjust(hspace=0.3)

plt.show()
