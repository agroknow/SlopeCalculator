import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt

from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt

request = {
    "aggregations": {
        "years_month": {
            "attribute": "createdOn",
            "format": "yyyy-MM-dd",
            "interval": "MONTH",
            "size": 1200
        }
    },
    "apikey": "32aa618e-be8b-32da-bc99-5172f90a903e",
    "from": "2004-01-01",
    "to":"2012-12-31",
    "detail": True,
    "published":True,
    "entityType": "incident",
    "pageSize": 0,
    "strictQuery": {
        "products.value": "pistachio nuts"
    }
}

apikey = 'apikey'
base_incidents = 'http://148.251.22.254:8080/search-api-1.0/search/'
headers = {'Content-type': 'application/json', 'Accept': 'application/json'}

objects = []

request['entityType'] = 'incident'
response = requests.post(base_incidents, data=json.dumps(request), headers=headers)

# print(response.json())
data = response.text
parsed = json.loads(data)
# print(json.dumps(parsed, indent=4))
for i in parsed.values():
    print(parsed['aggregations']['date_histogram#years_month']['buckets'])
# dataframe
df = pd.DataFrame(parsed['aggregations']['date_histogram#years_month']['buckets'])
# print(df)

df['date_ordinal'] = pd.to_datetime(df['key_as_string']).map(dt.datetime.toordinal)
print(df['doc_count'])
# print(df)
x=df['date_ordinal'].values.reshape(-1, 1)
y= df['doc_count'].values

reg = LinearRegression()
reg.fit(x,y)
print('intercept:', reg.intercept_)
print('slope:', reg.coef_)
y_pred = reg.predict(x)

y_pred= reg.intercept_+ reg.coef_*x
# model = LinearRegression().fit(dfevoo['date_ordinal'].values.reshape(-1, 1), dfevoo['price'].values)
# print('intercept:', model.intercept_)
# print('slope:', model.coef_)

print(y_pred)
slope=reg.coef_*100
plt.title('SLOPE %s '% str(slope)+'%')
plt.scatter(x,y)
plt.plot(x,y_pred,  color='black')
plt.show()


# model = LinearRegression().fit(dfevoo['date_ordinal'].values.reshape(-1, 1), dfevoo['price'].values)
# print('intercept:', model.intercept_)
# print('slope:', model.coef_)

