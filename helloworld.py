from flask import Flask

app = Flask(__name__)

# Define a route that responds with "Hello World"
@app.route('/')
def hello_world():
    return 'Hello World!'

# Start the server
if __name__ == '__main__':
    app.run(port=3000)