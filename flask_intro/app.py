from flask import Flask, request
from flask import render_template
from flask_debugtoolbar import DebugToolbarExtension


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

@app.route('/varialbes/<some_variable>')
def varialbes(some_variable):
    return render_template('variables.html', some_variable=some_variable)


@app.route('/if_example/<condition>')
def if_example(condition):
    return render_template('if_example.html', condition=condition)

@app.route('/loop_example')
def loop_example():
    return render_template('loop_example.html')

@app.route('/static_example')
def static_example():
    return render_template('static_example.html')

@app.route('/form_example')
def form_example():
    return render_template('form_example.html')

@app.route('/submit_form_example', methods=['POST'])
def submit_form_example():
    form_data = request.form['sample_form_data']
    return f"Data received: {form_data}"

app.run(debug=True)