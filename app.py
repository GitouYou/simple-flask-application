from flask import Flask
from flask import request, abort, render_template, make_response, jsonify, json
from ApiWrapper.wrapper import Wrapper


app = Flask(__name__)
ApiWrapper = Wrapper('config/config.json')
ApiWrapper.observe()


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/currencies')
def currencies():
    return app.response_class(
        response=ApiWrapper.getCurrencies(),
        status=200,
        mimetype='application/json'
    )


@app.route('/template/<name>')
def index_template(name=''):
    with open('templates/template_' + name + '.html', 'r') as _file:
        return app.response_class(
            response=_file.read(),
            status=200,
            mimetype='text/plain'
        )


@app.route('/today/<name>')
def live(name=None):
    if name:
        with open('model/TODAY.txt', 'r') as todayCurrency:
            myJson = json.load(todayCurrency)
            requestName = 'USD'+name.upper()
            if requestName in myJson['quotes']:
                return app.response_class(
                    response=json.dumps(
                            {
                                "value": str(myJson['quotes'][requestName]),
                                "name": name.upper()
                            }
                        ),
                    status=200,
                    mimetype='application/json'
                )
            else:
                return 'name not found', 404
    abort(404)


@app.route('/chart/')
@app.route('/chart/<name>')
def chart(name=None):
    if name:
        data = ApiWrapper.getFile(name.upper())
        if not data:
            abort(404)
        return app.response_class(
            response=data,
            status=200,
            mimetype='application/json'
        )

    return '', 204


@app.errorhandler(404)
def not_found(error):
    return render_template("error.html", error=error), 404


app.run(threaded=True, debug=True)
