#


def load_dataset(years_ago, product):
    from datetime import datetime, timedelta
    import pandas as pd
    import requests
    import json
    import datetime as dt

    now = datetime.now()
    end = str(now.year - 1) + '-12' + '-31'
    begin = str(now.year - years_ago) + '-01' + '-01'
    print(begin)
    request = {
        "aggregations": {
            "years_month": {
                "attribute": "createdOn",
                "format": "yyyy-MM-dd",
                "interval": "DAY",
                "size": 1200
            }
        },
        "apikey": '32aa618e-be8b-32da-bc99-5172f90a903e',
        "from": begin,
        "to": end,
        "detail": True,
        "published": True,
        "entityType": "incident",
        "pageSize": 0,
        "strictQuery": {
            "products.value": product
        }
    }

    apikey = '32aa618e-be8b-32da-bc99-5172f90a903e'
    base_incidents = 'http://148.251.22.254:8080/search-api-1.0/search/'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    request['entityType'] = 'incident'
    response = requests.post(base_incidents, data=json.dumps(request), headers=headers)
    data = response.text
    parsed = json.loads(data)
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
    return df

    # products = ["dietetic foods, food supplements, fortified foods", "cocoa and cocoa preparations, coffee and tea",
    #             "confectionery", "prepared dishes and snacks", "food contact materials", "non-alcoholic beverages",
    #             "soups, broths, sauces and condiments", "bivalve molluscs and products therefor",
    #             "cephalopods and products thereof", "fats and oils", "ices and desserts", "eggs and egg products",
    #             "honey and royal jelly", "alcoholic beverages", "feed additives", "pet feed",
    #             "poultry meat and poultry meat products", "cereals and bakery products", "fish and fish products",
    #             "herbs and spices", "meat and meat products (other than poultry)", "nuts, nut products and seeds",
    #             "milk and milk products"]
    # for product in products:

    # freq


def linear_regression(df):
    from sklearn.linear_model import LinearRegression
    import matplotlib.pyplot as plt
    import pandas as pd
    import datetime as dt
    df_year_freq = df.resample('Y').sum()

    df = df_year_freq
    # linear
    df = df.reset_index()
    df['date_ordinal'] = pd.to_datetime(df['priceStringDate']).map(dt.datetime.toordinal)
    x = df['date_ordinal'].values.reshape(-1, 1)
    y = df['doc_count'].values
    reg = LinearRegression()
    reg.fit(x, y)
    print('intercept:', reg.intercept_)
    slope = abs(reg.coef_) * 100
    print('slope:', abs(slope))
    y_pred = reg.predict(x)
    inc_sum = df['doc_count'].sum()
    # plot
    plt.title('YEAR')
    # plt.xlabel('DATE_FROM %s ' % str(begin) + '%')
    plt.xlabel('SLOPE %s ' % str(slope) + '%')

    plt.ylabel('inc_sum  %s ' % str(inc_sum))

    plt.scatter(x, y)
    plt.plot(x, y_pred, color='black')
    # plt.tight_layout()
    plt.savefig('plots/sample.png')
    filename = 'plots/sample.png'
    plt.show()
    return slope, filename


years_ago = 3
product = "nuts, nut products and seeds"
df = load_dataset(years_ago, product)
slope = linear_regression(df)
print(slope)
# df_day_freq = df
# df_weekly_freq = df.resample('W').sum()
# df_semi_month_freq = df.resample('SM').sum()
# df_month_freq = df.resample('M').sum()

# quit(0)
