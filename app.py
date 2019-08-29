import base64
from flask import Flask, escape, request,render_template

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def hello_world():
    from linear_last_3_years import dropdown
    menu=dropdown()

    return render_template('sample.html', menu=menu)

@app.route('/linear', methods=['GET'])
def linear():
    parameters = request.args

    product = parameters.get('product')
    years_ago = parameters.get('years_ago')
    years_ago=int(years_ago)
    product=str(product)
    from linear_last_3_years import load_dataset,linear_regression,dropdown
    menu=dropdown()

    df, msg = load_dataset(years_ago, product)

    if df is None:
        return  str(msg)
    slope, filename = linear_regression(df)
    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    print(slope)
    encoded_string = str(encoded_string.decode('utf-8'))
    # imag='<img src="data:image/png;base64, ' +str(encoded_string.decode('utf-8'))+'" />'
    # return '<img src="data:image/png;base64, ' +str(encoded_string.decode('utf-8'))+'" />'
    if msg is 'ok':
        return render_template('sample.html',encoded_string=encoded_string, product=product, years_ago=years_ago, menu=menu)
    else:
        return str(msg)
    #return render_template('sample.html',imag=imag)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run(debug = True, host='136.243.38.67')
