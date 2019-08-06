import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.preprocessing import MinMaxScaler


#take the dataset
df = pd.read_csv("food_dataset.csv")

dfevoo = df[df['product'].str.contains('χοιριν')]
import datetime as dt
dfevoo['date_ordinal'] = pd.to_datetime(dfevoo['priceStringDate']).map(dt.datetime.toordinal)
dfevoo = dfevoo.drop(columns=['price_id', 'product', 'priceDate', 'url', 'country', 'dataSource']).sort_values(
    by='priceStringDate')
dfevoo = pd.DataFrame(dfevoo)
dfevoo = dfevoo.groupby('priceStringDate').mean().reset_index()


x=dfevoo['date_ordinal'].values.reshape(-1, 1)
y= dfevoo['price'].values

reg = LinearRegression()
reg.fit(x,y)
print('intercept:', reg.intercept_)
print('slope:', reg.coef_)
y_pred = reg.predict(x)
# model = LinearRegression().fit(dfevoo['date_ordinal'].values.reshape(-1, 1), dfevoo['price'].values)
# print('intercept:', model.intercept_)
# print('slope:', model.coef_)

print(y_pred)
plt.scatter(x,y)
plt.plot(x,y_pred,  color='black')
plt.show()
# plt.show()
quit(0)

plt.plot(x,  color='red')
plt.show()

plt.show()
# quit(0)
