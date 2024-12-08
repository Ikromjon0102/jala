import pytest
from jala.middleware import Middleware


def test_basic_route_adding(app):

    @app.route("/home", allowed_methods = ['get'])
    def home(req, res):
        res.text = "Hello from home"    


def test_duplicate_routes_throws_exception(app):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello from home"    

    with pytest.raises(AssertionError):
        @app.route("/home")
        def home2(req, res):
            res.text = "Hello from home2"


def test_requests_can_be_sent_by_test_client(app, test_client):
    @app.route("/home")
    def home(req, res):
        res.text = "Hello from home"    

    response = test_client.get('http://testserver/home')
    assert response.text == "Hello from home"


def test_parameterizing_routing(app, test_client):
    @app.route("/hello/{name}")
    def greeting(req, res, name):
        res.text = f"Hello {name}"    

        assert test_client.get("http://testserver/hello/Ikromjon").text == "Hello Ikromjon"
        assert test_client.get("http://testserver/hello/alijon").text == "Hello Alijon"

def test_default_response(test_client):
    assert test_client.get('http://testserver/salom').text == "Not found."
    assert test_client.get('http://testserver/salom').status_code == 404

def test_class_based_get(app, test_client):
    @app.route('/books')
    class Books:
        def get(self, req, res):
            res.text = 'Books page'
        
    assert test_client.get('http://testserver/books').text == 'Books page'


def test_class_based_post(app, test_client):
    @app.route('/books')
    class Books:
        def post(self, req, res):
            res.text = 'Endpoint to create a book'
        
    assert test_client.post('http://testserver/books').text == 'Endpoint to create a book'


def test_class_based_method_not_allowed(app, test_client):
    @app.route('/books')
    class Books:
        def post(self, req, res):
            res.text = 'Endpoint to create a book'
        
    response =  test_client.get('http://testserver/books')

    assert response.text == 'Method Not Allowed'
    assert response.status_code == 405

def test_alternative_route(app, test_client):
    def new_handler(req, res):
        res.text = "From new handler"

    app.add_route('/new-handlers', new_handler)

    response = test_client.get("http://testserver/new-handlers")

    assert response.text == "From new handler"


def test_template_handler(app, test_client):
    @app.route('/test-template')
    def templates(req, res):
        res.body = app.template('test.html', context = {"new_title":'Test Title', "new_body":"Test Body"}).encode()

    response = test_client.get("http://testserver/test-template")

    assert "Test Body" in response.text
    assert "Test Title" in response.text
    assert "text/html" in response.headers['Content-Type']


def test_custom_exception_handler(app, test_client):
    def on_exception(req, res, exc):
        res.text = "Somthing went wrong"


    app.add_exception_handler(on_exception)


    @app.route('/exception')
    def exception_throwing_handler(req, res):
        raise AttributeError('some exception')
    

    response = test_client.get('http://testserver/exception')

    assert response.text == 'Somthing went wrong'

def test_not_exist_static_files(test_client):
    assert test_client.get('http://testserver/static/some_css.css').status_code == 404


def test_serving_static_files(test_client):
    response = test_client.get('http://testserver/static/test.css')

    assert "body {color: aliceblue;}" in response.text  

def test_middleware_methods_are_called(app, test_client):
    process_request_called = False
    process_response_called = False


    class SimpleMiddleware(Middleware):
        def __init__(self, app):
            super().__init__(app)

        def process_request(self, request):
            nonlocal process_request_called
            process_request_called = True
            process_response = True

        def process_response(self, request, response):
            nonlocal process_response_called
            process_response_called = True

    app.add_middleware(SimpleMiddleware)

    @app.route('/home')
    def index(req, res):
        res.text = "from handler"
    
    test_client.get('http://testserver/home')

    assert process_request_called is True 
    assert process_response_called is True 


def test_allowed_methods_function_based_handlers(app, test_client):
    
    @app.route('/home', allowed_methods = ['post'])
    def home(req, res):
        res.text = "Hello from home"

    
    response = test_client.get('http://testserver/home')

    assert response.status_code == 405
    assert response.text == "Method Not Allowed"


def test_json_response_helper(app, test_client):
    @app.route('/json')
    def json_hendler(req, res):
        res.json = {'name':'pyjala'}

    response = test_client.get('http://testserver/json')
    res_data = response.json()

    assert response.headers['Content-Type'] == "application/json"
    assert res_data['name'] == "pyjala"
    

def test_text_response_helper(app, test_client):
    @app.route('/text')
    def text_hendler(req, res):
        res.text = "plain text"

    response = test_client.get('http://testserver/text')

    assert 'text/plain' in response.headers['Content-Type']
    assert response.text == "plain text"
    

def test_html_response_helper(app, test_client):
    @app.route('/html')
    def html_hendler(req, res):
        res.html = app.template(
            'test.html',
            context = {"new_title":'Test Title', "new_body":"Test Body"}
        )

    response = test_client.get("http://testserver/html")

    assert 'text/html' in response.headers['Content-Type']
    assert "Test Title" in response.text
    assert "Test Body" in response.text


