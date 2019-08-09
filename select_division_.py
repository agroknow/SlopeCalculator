import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import os
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
from dateutil import relativedelta
import collections
import numpy as np


def comparison_based_on_division(a, n):
    minpos = a.index(min(a))
    return minpos


def filter_test(slope, dist_mean):
    if (slope > 0.085) or (dist_mean > 2):
        result = True

    else:
        result = False
    return result


# import datetime

def name_function(freq_count):
    if freq_count == 1:
        freq_name = "day"
    elif freq_count == 2:
        freq_name = "week"
    elif freq_count == 3:
        freq_name = "semi-month"

    elif freq_count == 4:
        freq_name = "month"
    else:
        freq_name = "year"
    return freq_name


# date_N_days_ago = datetime.now() - timedelta(months=-6)
months_ago = datetime.now() - relativedelta.relativedelta(months=6)
one_year_ago = datetime.now() - relativedelta.relativedelta(months=12)
three_years_ago = datetime.now() - relativedelta.relativedelta(months=36)
print(datetime.now())
print(months_ago)
print(one_year_ago)
print(three_years_ago)
# today=datetime.date.today()
# print(today)
# quit(0)

# string_date=
# print("Current year: %d" % now.year)
# print ("Current month: %d" % now.month)
# # time=[]
# #date=eval("2018-2011")
# date=eval("2018-2011")
# date=now.year-33
# print(type(date))
# print("three months ago: %s" % date)
# string_date=str(date)+"-03-01"
# print("three months ago string: %s" % string_date)
# quit(0)
f = open('csvfile.csv', 'w')
begin = "2016-01-01"
f.write("three months ago\n")  # Give your csv text here.
# path = path + '/' +begin + '/'
# if not os.path.exists(path):
#     os.mkdir(path)
products = ["dietetic foods, food supplements, fortified foods", "cocoa and cocoa preparations, coffee and tea",
            "confectionery", "prepared dishes and snacks", "food contact materials", "non-alcoholic beverages",
            "soups, broths, sauces and condiments", "bivalve molluscs and products therefor",
            "cephalopods and products thereof", "fats and oils", "ices and desserts", "eggs and egg products",
            "honey and royal jelly", "alcoholic beverages", "feed additives", "pet feed",
            "poultry meat and poultry meat products", "cereals and bakery products", "fish and fish products",
            "herbs and spices", "meat and meat products (other than poultry)", "nuts, nut products and seeds",
            "milk and milk products"]
# products=[1]
for product in products:
    # product="nuts, nut products and seeds"
    # f.write(str(product) + '\n')
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
        "to":"2018-12-31" ,
        "detail": True,
        "published": True,
        "entityType": "incident",
        "pageSize": 0,
        "strictQuery": {
            "products.value": product
        }
    }
    path = os.getcwd()
    # path='C:\Users\user\PycharmProjects\product_feature\three_years_ago'
    path = path + "\comp_div" + "/" + product + '/'
    print(path)
    # quit(0)
    # if not os.path.exists(path):
    #     os.mkdir(path)
    # else:
    #     continue
    # quit(0)
    # dietetic foods, food supplements, fortified foods
    # cocoa and cocoa preparations, coffee and tea
    # confectionery
    # prepared dishes and snacks
    # food contact materials
    # non-alcoholic beverages
    # soups, broths, sauces and condiments
    # bivalve molluscs and products therefor
    # cephalopods and products thereof
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
    apikey = '32aa618e-be8b-32da-bc99-5172f90a903e'
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

    # print(np.count_nonzero(dftoarray == 2))
    # quit(0)
    df_day_freq = df

    df_year_freq = df.resample('Y').sum()
    df_weekly_freq = df.resample('W').sum()

    df_semi_month_freq = df.resample('SM').sum()

    df_month_freq = df.resample('M').sum()

    # array_freq = [df_day_freq, df_weekly_freq, df_semi_month_freq, df_month_freq, df_year_freq]
    array_freq = [df_weekly_freq, df_semi_month_freq, df_month_freq]

    freq_name = ""
    freq_count = 0
    array_div = []
    for i in array_freq:
        freq_count = freq_count + 1

        # print(i)
        df = i
        # quit(0)
        # # df=df_weekly_freq
        # dftoarray = df['doc_count'].values
        # # print(dftoarray)
        #
        # print(collections.Counter(dftoarray))
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
        slope = abs(reg.coef_) * 100
        # print(y-y_pred)
        # if abs(slope)<0.000002:
        #     continue
        y_pred = reg.predict(x)
        distance = abs(y - y_pred)
        dist_mean = distance.mean()
        result_for_slope = filter_test(slope, dist_mean)
        # freq_name=name_function(freq_count)
        division = dist_mean // slope
        array_div.append(division)

        inc_sum = df['doc_count'].sum()

        # f.write(str(freq_name) + ' ')
        # f.write(str(slope) + " ")
        # f.write(str(dist_mean) + " ")
        # f.write(str(inc_sum) + " ")
        # f.write(str(dist_mean) + " ")
        #
        # f.write(str(result_for_slope))  # Give your csv text here.
        #
        # f.write('\n')
        ## Python will convert \n to os.linesep
        # f.close()
        # if result_for_slope is False:
        #     continue
        # else:
        #     #calculate distance
        #     # distance=[]
        #     # distance=abs(y-y_pred)
        #     # print(distance)
        #     # print('max')
        #     # print(distance.max())
        #
        #     # y_pred = reg.intercept_ + reg.coef_ * x
        #
        #     # quit(0)
        #     plt.title(' inc_sum  %s ' % str(inc_sum))
        #     # plt.xlabel('DATE_FROM %s ' % str(begin) + '%')
        #     plt.xlabel('SLOPE %s ' % str(slope) + '%')
        #
        #     plt.ylabel('MEAN %s ' % str(dist_mean))
        #
        #     plt.scatter(x, y)
        #     plt.plot(x, y_pred, color='black')
        #     plt.savefig(path + '%s.png' % str(freq_name), bbox_inches='tight')
        #     plt.show()
        # break
    quit(0)
    result = comparison_based_on_division(array_div, len(array_div))
    print(result)
    if result == 0:
        df = df_weekly_freq
        freq_count = 2
    elif result == 1:
        df = df_semi_month_freq
        freq_count = 3

    elif result == 2:
        df = df_month_freq
        freq_count = 4
    else:
        print("nothing from comparison")
        print(result)

        # quit(0)
        # df=df_weekly_freq
    dftoarray = df['doc_count'].values
    # print(dftoarray)

    print(collections.Counter(dftoarray))
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
    slope = abs(reg.coef_) * 100
    # print(y-y_pred)
    # if abs(slope)<0.000002:
    #     continue
    y_pred = reg.predict(x)
    distance = abs(y - y_pred)
    dist_mean = distance.mean()
    result_for_slope = filter_test(slope, dist_mean)
    freq_name = name_function(freq_count)
    division = dist_mean // slope
    array_div.append(division)

    inc_sum = df['doc_count'].sum()

    f.write(str(freq_name) + ' ')
    f.write(str(slope) + " ")
    f.write(str(dist_mean) + " ")
    f.write(str(inc_sum) + " ")
    f.write(str(dist_mean) + " ")

    f.write(str(result_for_slope))  # Give your csv text here.

    f.write('\n')
    ## Python will convert \n to os.linesep

    # calculate distance
    # distance=[]
    # distance=abs(y-y_pred)
    # print(distance)
    # print('max')
    # print(distance.max())

    # y_pred = reg.intercept_ + reg.coef_ * x

    # quit(0)
    plt.title(' inc_sum  %s ' % str(inc_sum))
    # plt.xlabel('DATE_FROM %s ' % str(begin) + '%')
    plt.xlabel('SLOPE %s ' % str(slope) + '%')

    plt.ylabel('MEAN %s ' % str(dist_mean))

    plt.scatter(x, y)
    plt.plot(x, y_pred, color='black')
    plt.savefig(path + '%s.png' % str(freq_name), bbox_inches='tight')
    plt.show()
    # quit(0)
