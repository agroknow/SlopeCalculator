import base64
from flask import Flask, escape, request,render_template

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/')
def hello_world():
    from linear_last_3_years import dropdown
    menu, menu_haz=dropdown()


    return render_template('sample.html', menu=menu, hazards=menu_haz)

@app.route('/linear', methods=['GET'])
def linear():
    parameters = request.args

    product = parameters.get('product')
    hazards = parameters.get('hazard')

    years_ago = parameters.get('years_ago')
    years_ago=int(years_ago)
    product=str(product)
    hazards = str(hazards)
    print (hazards)
    # hazards='NONE'
    sloparr=[]
    if hazards== 'ALL':
        print ("if")
        from linear_last_3_years import multipleReg
        slope, filename, msg, sloparr =multipleReg(product,years_ago)
        print(msg)
        if msg != "ok":
            return str(msg)
    elif hazards =="NONE":
        from linear_last_3_years import load_dataset_without_haz, linear_regression
        df, msg = load_dataset_without_haz(years_ago, product)
        if df is None:
            return str(msg)
        slope, filename, x, y, y_pred = linear_regression(df)
    else:
        # hazards='chemical'
        from linear_last_3_years import load_dataset, linear_regression
        df, msg = load_dataset(years_ago, product, hazards)
        if df is None:
            return str(msg)
        slope, filename,x,y,y_pred = linear_regression(df)

    from linear_last_3_years import load_dataset,linear_regression,dropdown
    menu, menu_haz=dropdown()


    with open(filename, "rb") as image_file:
        encoded_string = base64.b64encode(image_file.read())

    print(slope)
    encoded_string = str(encoded_string.decode('utf-8'))
    # imag='<img src="data:image/png;base64, ' +str(encoded_string.decode('utf-8'))+'" />'
    # return '<img src="data:image/png;base64, ' +str(encoded_string.decode('utf-8'))+'" />'
    if not sloparr:
        sloparr=slope
    if msg is 'ok':
        return render_template('sample.html',encoded_string=encoded_string, product=product, years_ago=years_ago, menu=menu, hazards=menu_haz, hazard=hazards, sloparr=sloparr)
    else:
        return str(msg)
    #return render_template('sample.html',imag=imag)

@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


if __name__ == '__main__':
    app.run(debug = True)
