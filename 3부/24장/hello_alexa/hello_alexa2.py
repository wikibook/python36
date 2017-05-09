import flask
import flask_ask

app = flask.Flask(__name__)
ask = flask_ask.Ask(app, "/")

import logging
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

@ask.launch
def launch_hello_alexa():
    msg = flask.render_template('start')
    repeat_msg = flask.render_template('repeat')
    return flask_ask.question(msg).reprompt(repeat_msg)

@ask.intent('NameIntent')
def hello(name):
    msg = flask.render_template('answer', name = name)
    return flask_ask.statement(msg)

if __name__ == '__main__':
    app.run(debug=True, port=5001)