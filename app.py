from flask import Flask, escape, request

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/linear', methods=['GET'])
def api_training():
    parameters = request.args

    product = parameters.get('product')
    years_ago = parameters.get('years_ago')
    years_ago=int(years_ago)
    from linear_last_3_years import load_dataset,linear_regression
    df = load_dataset(years_ago, product)
    slope = linear_regression(df)
    print(slope)
    return "ok"

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run(debug = True)
