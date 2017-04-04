from flask import Flask
from flask import request, abort, render_template, make_response, jsonify, json
from ApiWrapper.wrapper import Wrapper

app = Flask(__name__)
ApiWrapper = Wrapper('config/config.json')
ApiWrapper.reloadFiles()
ApiWrapper.observe();

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/teste')
def teste():
    response = app.response_class(
        response=ApiWrapper.getFile('CAD'),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/currencies')
def currencies():
    return app.response_class(
        response=ApiWrapper.getCurrencies(),
        status=200,
        mimetype='application/json'
    )

@app.route('/template/index')
def index_template():
    with open('templates/template_index.html', 'r') as _file:
        return app.response_class(
            response=_file.read(),
            status=200,
            mimetype='text/plain'
        )

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


if __name__ == "__main__":
    #app.run(host="0.0.0.0", port=8080, threaded=True)
    app.run(threaded=True, debug=True)
