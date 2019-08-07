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
            "interval": "DAY",
            "size": 1200
        }
    },
    "apikey": "",
    "from": "2013-01-01",
    # "to": "2018-03-01",
    "detail": True,
    "published": True,
    "entityType": "incident",
    "pageSize": 0,
    "strictQuery": {
        "products.value": "pet feed"
    }
}


# dietetic foods, food supplements, fortified foods
# cocoa and cocoa preparations, coffee and tea
# confectionery
# prepared dishes and snacks
# food contact materials
# non-alcoholic beverages
# soups, broths, sauces and condiments
# bivalve molluscs and products therefor
# cephalopods and products therefor
# fats and oils
# ices and desserts
# eggs and egg products
# other food products / mixed
# honey and royal jelly
# alcoholic beverages
# feed additives
# pet feed
# poultry meat and poultry meat products
# cereals and bakery products
# fish and fish products
# herbs and spices
# fruits and vegetables
# meat and meat products (other than poultry)
# nuts, nut products and seeds
# milk and milk products
apikey = ""
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
df['priceStringDate'] = pd.to_datetime(df['key_as_string'])
# print(df.groupby(by=[df.index.month, df.index.year]))
df['date_ordinal'] = pd.to_datetime(df['key_as_string']).map(dt.datetime.toordinal)
df.set_index('priceStringDate', inplace=True)
df = df.drop(columns=['key_as_string', 'key'])
# print(df)
# quit(0)
df_day_freq = df

df_year_freq = df.resample('Y').sum()
df_weekly_freq = df.resample('W').sum()

df_semi_month_freq = df.resample('SM').sum()

df_month_freq = df.resample('M').sum()

#
print(df)

array = [df_day_freq, df_weekly_freq, df_semi_month_freq, df_month_freq, df_year_freq]
for i in array:
    print(i)
    df = i

    df = df.reset_index()
    df['date_ordinal'] = pd.to_datetime(df['priceStringDate']).map(dt.datetime.toordinal)
    # quit(0)
    x = df['date_ordinal'].values.reshape(-1, 1)
    y = df['doc_count'].values
    # print(df)
    reg = LinearRegression()
    reg.fit(x, y)
    print('intercept:', reg.intercept_)
    print('slope:', reg.coef_)
    print('abs_slope:', abs(reg.coef_))
    slope = reg.coef_ * 100

    # if abs(slope)<0.000002:
    #     continue
    y_pred = reg.predict(x)

    # y_pred = reg.intercept_ + reg.coef_ * x
    inc_sum=df['doc_count'].sum()
    # quit(0)
    plt.title(' %s ' % str(df.head(2)))
    plt.xlabel('SLOPE %s ' % str(slope) + '%')
    plt.ylabel('SUM_INC %s ' % str(inc_sum))

    plt.scatter(x, y)
    plt.plot(x, y_pred, color='black')
    plt.show()

