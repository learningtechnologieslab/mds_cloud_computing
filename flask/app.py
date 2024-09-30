from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/about')
def about():
	return "This is the About page."


'''
'<name>' is a dynamic part of the URL, 
where you can pass any value (e.g., /user/John will display “Hello, John!”).
Navigating to http://127.0.0.1:5000/user/John will display the "Hello, John!"
'''
@app.route('/user/<name>')
def greet_user(name):
	return f"Hello, {name}!"


@app.route('/html_example')
def html_example():
    return "<h1>Welcome to My Flask App</h1><p>This is a basic example.</p>"


'''
render_template() looks for the hello.html file inside the templates folder.
The variable name is passed to the template and replaces {{ name }} in the HTML.
Running the App When you run the application and navigate to /hello/Bob, 
the browser will display: Hello, Bob!
'''
@app.route('/hello/<name>')
def hello(name):
    return render_template('hello.html', name=name)



app.run()