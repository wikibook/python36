import random
import logging
import flask
import flask_ask

app = flask.Flask(__name__)
ask = flask_ask.Ask(app, "/")
logging.getLogger("flask_ask").setLevel(logging.DEBUG)

def get_baseball_num():
    num = []
    num.append(random.randrange(0, 10, 1))
    num.append(num[0])
    num.append(num[0])

    while (num[0] == num[1]):
        num[1] = random.randrange(0, 10, 1)

    while (num[0] == num[2] or num[1] == num[2]):
        num[2] = random.randrange(0, 10, 1)

    return num

def check_baseball_num(input_num):
    strike_cnt = 0
    ball_cnt = 0
    answer_num = flask_ask.session.attributes['answer']

    for i in range(0, 3):
        for j in range(0, 3):
            if input_num[i] == answer_num[j] and i == j:
                strike_cnt += 1
            elif input_num[i] == answer_num[j]:
                ball_cnt += 1
    if strike_cnt == 3:
        msg = "3 strikes! Good Job"
        return (msg, True)
    elif ball_cnt == 3:
        msg = "3 balls"
        return (msg, False)
    else:
        msg = "{0} balls and {1} strikes".format(ball_cnt, strike_cnt)
        return (msg, False)

@ask.launch
def launch_game():
    msg = flask.render_template('start')
    return flask_ask.question(msg)

@ask.intent("YesIntent")
def start_game():
    msg = flask.render_template('rule')
    answer = get_baseball_num()
    flask_ask.session.attributes['answer'] = answer
    logging.info("Answer is {0}".format(answer))

    return flask_ask.question(msg)

@ask.intent("NoIntent")
def end_game():
    msg = flask.render_template('end')
    return flask_ask.statement(msg)

@ask.intent("AnswerIntent", convert={'first': int, 'second': int, 'third': int})
def answer(first, second, third):
    input_num = [first, second, third]
    logging.info("input number is {0}".format(input_num))
    msg, ret = check_baseball_num(input_num)

    if ret:
        return flask_ask.statement(msg)
    else:
        msg += ". Try again!"
        return flask_ask.question(msg)

if __name__ == '__main__':
    app.run(debug=True, port=7000)