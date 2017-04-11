# simple-flask-application
A simple flask application using mustache and highcharts
###### v 0.0.1
#
## Instalation:
clone or unzip the repository 
```sh
    $ unzip simple-flask-app.zip
``` 
or
```sh
    $ git clone git@github.com:joaofreires/simple-flask-application.git
```

You can use pip to install
```sh
    $ pip install -e simple-flask-app
```

#### Config
```json
{
    "api":{
        "token": "", // your api token (currency layer)
        "currencies": ["BRL", "EUR", "ARS"], //Currencies that you'll use
        "titles": {"BRL": "REAL Quotation", "EUR": "EURO Quotation"...} //Title for some currencies
      },
    "history": 7, //Days that the api will remember
    "modelPath": "model/highchart.json", //Highchart model
    "resultDir": "model" //result directory path
}
```
NOTE: Maybe just add new currencies throw a error, so you need go to file `ApiWrapper/currencies/currencie_factory.py` and add:
```py
if name.upper() == 'YOUR_CURRENCY':
        return Currency('YOUR_CURRENCY')
```

##### Finally
```sh 
    $ simple-flask-app
```

And the application will run on localhost:5000
