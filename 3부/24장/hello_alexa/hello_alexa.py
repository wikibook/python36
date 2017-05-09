import flask
import flask_ask

app = flask.Flask(__name__)
ask = flask_ask.Ask(app, "/")

@ask.launch
def launch_hello_alexa():
    msg = "Hi, My name is Alexa. What is your name?"
    return flask_ask.question(msg)

@ask.intent('NameIntent')
def hello(name):
    msg = "Nice to see you. {0}".format(name)
    return flask_ask.statement(msg)

if __name__ == '__main__':
    app.run(debug=True)