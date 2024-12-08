# Jala: Python Web Framework built for learning purposes

![purpose](https://img.shields.io/badge/purpose-learning-green)
![PyPi - Version](https://img.shields.io/pypi/v/jala)

Jala is a Python web framework built for learing purposes

It's a WSGI faramework and can be used with any WSGI application server such as Gunicorn (in windows waitress).


## Installation

```shell
pip install jala
```

## How to use it

### Basic usage:
```python
from jala.app import PyTempFrameApp

app = PyTempFrameApp()

@app.route('/home', allowed_methods = ['get'])
def home(request, response):
    response.text = "Hello this is Home page"


@app.route('/hello/{name}')
def greeting(request, respnse, name):
    respnse.text = f"Hello {name.title()}"


@app.route('/books')
class Books:
    def get(self, request, response):
        response.text = 'Books page'
    
    def post(self, request, response):
        response.text = "Endpoint to create a book"

    
def new_handler(req, res):
    res.text = "From new handler"

app.add_route('/new-handler', new_handler)


@app.route('/template')
def template_handler(req, res):
    res.body = app.template(
        'home.html',
        context = {"new_title":'yangi Title', "new_body":"yap - yangi Body"}
    )

```

### Unit Tests
The recommended way of writing unit test is with [pytest](https://docs.pytest.org/en/latest/).
There are two built in fixture that you may want to use when writing unit test with Jala. The first one is `app` which is an instance of the main `API` class:

```python
def test_route_overlab_throws_exception(app):
    @app.route("/")
    def home(req, resp):
        resp.text = "Welcome Home."
    
    with pytest.raises(AssertionError)
    @app.route("/")
        def home2(req, resp):
            resp.text = "Welcome Home2."

```
The other one is a `client` that you can use to send HTTP requests to your handlers. It is based on the famous [requests](https://requests.readthedocs.io/) and it should feel very familiar:

```python 
def test_parameterizing_routing(app, client):
    @app.route("/hello/{name}")
    def greeting(req, res, name):
        res.text = f"Hello {name}"    

        assert test_client.get("http://testserver/hello/matthew").text == "Hello matthew"
```

## Templates
The default folder for templates is `templates`. You can change it when initializing the main `API()` class:

```python
app = API(templates_dir = "template_dir_name")
```

Then you can use HTML files in that folder like so in a handler:
```python 
@app.route('/show/template')
def template_handler(req, res):
    res.body = app.template(
        'example.html',
        context = {"new_title":'Awesome Framework', "new_body":"Welcome to the future!"}
    )
```


## Static Files

Just like templates, the default folder for static files is `static` and you can override it:
```python
app = API(static_dir="static_dir_name")
```

Then you can use the files inside this folder in HTML files:

```html
<html>

<head>
    <title>{{new_title}}</title>
    <link rel="stylesheet" href="/static/main.css">
</head>

<body>
    <h1> {{ body }} </h1>
    <p>This a paragraph</p>
</body>

</html>v
```

### Middleware

You can write custom middleware classes by inheriting from the `jala.middleware.Middleware` class overriding its two methods that are called before and after each request:


```python
from jala.app import PyTempFrameApp
from jala.middleware import Middleware

app = PyTempFrameApp()

class SampleCustomMiddleware(Middleware):
    def process_request(self, req):
        print(f"Before dispatch {req.url}")
    
    def process_response(self, req, res):
        print(f"After dispatch {req.url}")

app.add_middleware(SampleCustomMiddleware)
```
