def dropdown():
    import requests
    import json
    import pandas as pd

    f = open("api_key", "r")
    api_key = f.readline()
    api_key = str(api_key)
    request = {
        "aggregations": {
            "products": {
                "attribute": "products.value.keyword",
                "size": 6000}},
        "apikey": api_key,
        "from": '2014-12-31',
        "detail": True,
        "entityType": "incident"
    }
    apikey = str(api_key)
    base_incidents = 'http://148.251.22.254:8080/search-api-1.0/search/'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    request['entityType'] = 'incident'
    response = requests.post(base_incidents, data=json.dumps(request), headers=headers)
    print(response)

    # data = response.text
    # parsed = json.loads(data)

    parsed = response.json()
    print(parsed)
    # quit(0)

    df = pd.DataFrame(parsed['aggregations']['sterms#products']['buckets'])
    df = df.drop(columns=['doc_count'])

    menu = list(df['key'])
    return menu


def load_dataset(years_ago, product):
    from datetime import datetime, timedelta
    from dateutil.relativedelta import relativedelta
    import dateutil.relativedelta
    import pandas as pd
    import requests
    import json
    import datetime as dt
    f = open("api_key", "r")
    api_key = f.readline()
    api_key = str(api_key)
    # print(api_key)

    now = datetime.now()
    print(now)
    end = str(now.year - 1) + '-12' + '-31'
    begin = str(now.year - years_ago) + '-01' + '-01'
    if years_ago == 6:
        lastmonth = now + dateutil.relativedelta.relativedelta(months=-1)
        end = str(lastmonth.strftime('%Y-%m' + '-31'))
        monthsix = now + relativedelta(months=-6)
        begin = str(monthsix.strftime('%Y-%m' + '-01'))

    request = {
        "aggregations": {
            "years_month": {
                "attribute": "createdOn",
                "format": "yyyy-MM-dd",
                "interval": "DAY",
                "size": 1200

            },
            "products": {
                "attribute": "products.value.keyword",

                "size": 1200

            }
        },
        "apikey": api_key,
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

    apikey = str(api_key)
    base_incidents = 'http://148.251.22.254:8080/search-api-1.0/search/'
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    request['entityType'] = 'incident'
    response = requests.post(base_incidents, data=json.dumps(request), headers=headers)
    print(response)

    # data = response.text
    # parsed = json.loads(data)

    parsed = response.json()
    print(parsed)
    # quit(0)
    for i in parsed.values():
        print(parsed['aggregations']['date_histogram#years_month']['buckets'])
    # dataframe
    df = pd.DataFrame(parsed['aggregations']['date_histogram#years_month']['buckets'])
    # print(df)
    try:
        df['priceStringDate'] = pd.to_datetime(df['key_as_string'])
    except:
        return None, "Νot available\nTry another product"
    # print(df.groupby(by=[df.index.month, df.index.year]))
    df['date_ordinal'] = pd.to_datetime(df['key_as_string']).map(dt.datetime.toordinal)
    df.set_index('priceStringDate', inplace=True)
    df = df.drop(columns=['key_as_string', 'key'])
    msg = "ok"
    if years_ago == 1:
        c = len(df)
        if c <= (365 * 70 / 100):
            msg = "Νot available\nTry another product"
        df_year_freq = df.resample('M').sum()
        df = df_year_freq
    elif years_ago == 6:
        c = len(df)
        if c <= (185 * 70 / 100):
            msg = "Νot available\nTry another product"
        df_year_freq = df.resample('M').sum()
        df = df_year_freq
    else:
        c = len(df)
        if c <= (1080 * 70 / 100):
            msg = "Νot available\nTry another product"
        df_year_freq = df.resample('Y').sum()
        df = df_year_freq
    return df, msg




def linear_regression(df):
    from sklearn.linear_model import LinearRegression
    import matplotlib.pyplot as plt
    import pandas as pd
    import datetime as dt

    # linear
    df = df.reset_index()
    df['date_ordinal'] = pd.to_datetime(df['priceStringDate']).map(dt.datetime.toordinal)
    x = df['date_ordinal'].values.reshape(-1, 1)
    y = df['doc_count'].values
    reg = LinearRegression()
    reg.fit(x, y)
    print('intercept:', reg.intercept_)
    slope = reg.coef_ * 100
    print('slope:', slope)
    y_pred = reg.predict(x)
    inc_sum = df['doc_count'].sum()
    # plot
    plt.title('LINEAR REGRESSION SLOPE %s' % str(slope) + '%')
    # plt.xlabel('DATE_FROM %s ' % str(begin) + '%')
    plt.ylabel('INCIDENTS (%s)' % str(inc_sum))

    plt.xlabel('YEARS')

    plt.scatter(x, y)
    plt.plot(x, y_pred, color='black')
    # plt.tight_layout()
    plt.savefig('plots/sample.png')
    filename = 'plots/sample.png'
    plt.show()
    return slope, filename

# years_ago = 1
# product = "zucchini puree"
# df = load_dataset(years_ago, product)
# slope = linear_regression(df)
# # menu=dropdown()
# print(menu)
# print(slope)
# df_day_freq = df
# df_weekly_freq = df.resample('W').sum()
# df_semi_month_freq = df.resample('SM').sum()
# df_month_freq = df.resample('M').sum()

# quit(0)
