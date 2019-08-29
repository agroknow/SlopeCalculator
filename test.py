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
                "size": 1000
            },
            "hazards": {
                "attribute": "hazards.value.keyword",
                "size": 100
            }
        },

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
    dfhazard=pd.DataFrame(parsed['aggregations']['sterms#hazards']['buckets'])
    dfhazard = dfhazard.drop(columns=['doc_count'])
    hazards=list(dfhazard['key'])
    print (hazards)
    # print(dfhazard)
    df = pd.DataFrame(parsed['aggregations']['sterms#products']['buckets'])
    df = df.drop(columns=['doc_count'])

    menu = list(df['key'])
    return menu, hazards

menu, haz=dropdown()
print(haz)