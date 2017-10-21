import pandas as pd
from sklearn import linear_model
import warnings
import matplotlib.pyplot as plt
warnings.filterwarnings(action="ignore", module="scipy", message="^internal gelsd")

# read data:
dataframe = pd.read_fwf('brain_body.txt')
x_values = dataframe[['Brain']]
y_values = dataframe[['Body']]

# train model on data:
body_reg = linear_model.LinearRegression()
body_reg.fit(x_values, y_values)

# visualise result:
brainWeight = 0
# print('For ', brainWeight, ' kg brain the body weight is: ', body_reg.predict(brainWeight)[0][0], ' kg')

plt.scatter(x_values, y_values)
plt.show()
