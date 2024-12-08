from jala.app import PyTempFrameApp
from jala.middleware import Middleware

app = PyTempFrameApp()


@app.route('/home', allowed_methods = ['get'])
def home(request, response):
    response.text = "Hello this is Home page"


@app.route('/about', allowed_methods=['get'])
def about(request, response):
    response.text =  "Hello this is About page"


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

def on_exception(req, res, exc):
    res.text = str(exc)


app.add_exception_handler(on_exception)


@app.route('/exception')
def exception_throwing_handler(req, res):
    raise AttributeError('some exception')



class LoginMiddleware(Middleware):
    def process_request(self, req):
        print(f"request is being called {req.url}")
    
    def process_response(self, req, res):
        print(f"response has been generated {req.url}")

app.add_middleware(LoginMiddleware)
