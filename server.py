import bcrypt
import flask
from flask import Flask, request, session
from util import sort_data, validate_image
import data_handler
from werkzeug.utils import secure_filename
import os
from bonus_questions import SAMPLE_QUESTIONS

UPLOAD_FOLDER = "./static/images/"

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png', '.gif', '.bmp']
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
app.secret_key = 'DDtk96KGHFgSsWZWBUxKZsv'


@app.route("/")
def main_page():
    questions = data_handler.get_questions(limit=5, sort_key="submission_time", sort_dir="DESC")
    if request.args.get('order_by') and request.args.get('order_direction'):
        order_by_key = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        questions = sort_data(questions, order_by_key, order_direction)
    for question in questions:
        question['tags'] = data_handler.get_question_tags(question['id'])
        question['comments'] = len(data_handler.get_question_comments(question['id']))
    return flask.render_template("questions.html", questions=questions, title='Recent questions')


@app.route("/list")
def list_page():
    questions = data_handler.get_questions()
    if request.args.get('order_by') and request.args.get('order_direction'):
        order_by_key = request.args.get('order_by')
        order_direction = request.args.get('order_direction')
        questions = sort_data(questions, order_by_key, order_direction)
    for question in questions:
        question['tags'] = data_handler.get_question_tags(question['id'])
        question['comments'] = len(data_handler.get_question_comments(question['id']))
    return flask.render_template("questions.html", questions=questions, title='Questions')


@app.route("/question/<question_id>")
def list_question(question_id=None):
    answers = data_handler.get_question_answers(question_id)
    for answer in answers:
        answer['comments'] = data_handler.get_answer_comments(answer['id'])
    if question_id is not None:
        question = data_handler.get_questions(question_id)
        comments = data_handler.get_question_comments(question_id)
        tags = data_handler.get_question_tags(question_id)
        return flask.render_template("answers.html", answers=answers, comments=comments, title='Answers',
                                     question=question, tags=tags)
    else:
        return flask.redirect("/")


@app.route("/add-question", methods=['GET', 'POST'])
def add_question():
    if request.method == 'GET':
        return flask.render_template("add_question.html", title='Add question')
    elif request.method == 'POST':
        question_data = dict(request.form)
        uploaded_file = request.files['image']
        question_data['image'] = uploaded_file.filename
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flask.abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        question_data['user_id'] = session['user_id']
        new_question_id = data_handler.add_question(question_data)
        return flask.redirect(f"/question/{new_question_id}")


@app.route("/question/<question_id>/new-answer", methods=['GET', 'POST'])
def add_answer(question_id):
    if request.method == 'GET':
        question = data_handler.get_questions(question_id)
        return flask.render_template("add_answer.html", title='Add answer', question=question)
    elif request.method == 'POST':
        answer_data = dict(request.form)
        uploaded_file = request.files['image']
        answer_data['image'] = uploaded_file.filename
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flask.abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        answer_data['user_id'] = session['user_id']
        new_answer_data = data_handler.add_answer(answer_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/new-comment", methods=['GET', 'POST'])
def add_question_comment(question_id):
    if request.method == 'GET':
        question = data_handler.get_questions(question_id)
        return flask.render_template("add_question_comment.html", title='Add comment', question=question)
    elif request.method == 'POST':
        comment_data = dict(request.form)
        comment_data['user_id'] = session['user_id']
        data_handler.add_question_comment(comment_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/delete", methods=['POST'])
def delete_question(question_id):
    data_handler.delete_question(question_id)
    return flask.redirect("/list")


@app.route("/question/<question_id>/edit", methods=['GET', 'POST'])
def edit_question(question_id):
    if request.method == 'GET':
        question = data_handler.get_questions(question_id)
        return flask.render_template("edit_question.html", title='Edit question', question=question)
    elif request.method == 'POST':
        question_data = dict(request.form)
        previous_image = question_data.get('previous_image')
        uploaded_file = request.files['image']
        question_data['image'] = uploaded_file.filename
        if uploaded_file.filename == '':
            question_data['image'] = previous_image
        else:
            filename = secure_filename(uploaded_file.filename)
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flask.abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
            question_data['image'] = filename
        question_id = data_handler.update_question(question_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/edit", methods=['GET', 'POST'])
def edit_answer(answer_id):
    if request.method == 'GET':
        answer = data_handler.get_answers(answer_id)
        return flask.render_template("edit_answer.html", title='Edit answer', answer=answer)
    elif request.method == 'POST':
        answer_data = dict(request.form)
        uploaded_file = request.files['image']
        filename = secure_filename(uploaded_file.filename)
        if filename != '':
            answer_data['image'] = filename
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in app.config['UPLOAD_EXTENSIONS'] or \
                    file_ext != validate_image(uploaded_file.stream):
                flask.abort(400)
            uploaded_file.save(os.path.join(app.config['UPLOAD_PATH'], filename))
        else:
            answer_data['image'] = answer_data.get('previous_image', '')
        question_id = data_handler.update_answer(answer_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/new-comment", methods=['GET', 'POST'])
def add_answer_comment(answer_id):
    if request.method == 'GET':
        answer = data_handler.get_answers(answer_id)
        question = data_handler.get_questions(answer[0]['question_id'])
        return flask.render_template("add_answer_comment.html", title='Add comment', answer=answer, question=question)
    elif request.method == 'POST':
        comment_data = dict(request.form)
        comment_data['user_id'] = session['user_id']
        question_id = data_handler.add_answer_comment(comment_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/answer/<answer_id>/toogle_accept_answer", methods=['POST'])
def accept_answer(answer_id):
    user_id = data_handler.get_answers(answer_id=answer_id)[0]['user_id']
    data_handler.update_user_reputation(user_id, 15)
    data_handler.toogle_accept_answer(answer_id)
    return flask.redirect(flask.request.referrer)


@app.route("/answer/<answer_id>/delete", methods=['POST'])
def delete_answer(answer_id):
    data_handler.delete_answer(answer_id)
    return flask.redirect(flask.request.referrer)


@app.route("/question/<question_id>/vote-up", methods=['POST'])
def question_vote_up(question_id):
    user_id = data_handler.get_questions(question_id=question_id)[0]['user_id']
    data_handler.update_user_reputation(user_id, 5)
    data_handler.vote_question(question_id, 1)
    return flask.redirect(flask.request.referrer)


@app.route("/question/<question_id>/vote-down", methods=['POST'])
def question_vote_down(question_id):
    user_id = data_handler.get_questions(question_id=question_id)[0]['user_id']
    data_handler.update_user_reputation(user_id, -2)
    data_handler.vote_question(question_id, -1)
    return flask.redirect(flask.request.referrer)


@app.route("/answer/<answer_id>/vote-up", methods=['POST'])
def answer_vote_up(answer_id):
    user_id = data_handler.get_answers(answer_id=answer_id)[0]['user_id']
    data_handler.update_user_reputation(user_id, 10)
    data_handler.vote_answer(answer_id, 1)
    return flask.redirect(flask.request.referrer)


@app.route("/answer/<answer_id>/vote-down", methods=['POST'])
def answer_vote_down(answer_id):
    user_id = data_handler.get_answers(answer_id=answer_id)[0]['user_id']
    data_handler.update_user_reputation(user_id, -2)
    data_handler.vote_answer(answer_id, -1)
    return flask.redirect(flask.request.referrer)


@app.route("/search", methods=['GET'])
def search_question():
    if request.args.get('q'):
        search_string = request.args.get('q').lower()
        questions = data_handler.find_question(search_string)
        if request.args.get('order_by') and request.args.get('order_direction'):
            order_by_key = request.args.get('order_by')
            order_direction = request.args.get('order_direction')
            questions = sort_data(questions, order_by_key, order_direction)
        for question in questions:
            question['tags'] = data_handler.get_question_tags(question['id'])
            question['comments'] = len(data_handler.get_question_comments(question['id']))
        return flask.render_template("questions.html", questions=questions, title='Questions')
    return flask.redirect(flask.request.referrer)


@app.route("/question/<question_id>/new-tag", methods=['GET', 'POST'])
def add_question_tag(question_id):
    if request.method == 'GET':
        question = data_handler.get_questions(question_id)
        tags = data_handler.get_available_tags()
        return flask.render_template("add_question_tag.html", question=question, tags=tags)
    if request.method == 'POST':
        tag_data = dict(request.form)
        data_handler.add_question_tag(tag_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_question_tag(question_id, tag_id):
    data_handler.delete_question_tag(question_id, tag_id)
    return flask.redirect(f"/question/{question_id}")


@app.route("/comment/<comment_id>/edit", methods=['GET', 'POST'])
def edit_comment(comment_id):
    if request.method == 'GET':
        comment = data_handler.get_comment(comment_id)
        return flask.render_template("edit_comment.html", title='Edit comment', comment=comment)
    elif request.method == 'POST':
        comment_data = dict(request.form)
        question_id = data_handler.update_comment(comment_data)
        return flask.redirect(f"/question/{question_id}")


@app.route("/comment/<comment_id>/delete")
def delete_comment(comment_id):
    data_handler.delete_comment(comment_id)
    return flask.redirect(flask.request.referrer)


@app.route("/login", methods=['GET', 'POST'])
def user_login():
    if request.method == 'GET':
        return flask.render_template("login.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
    errors = []
    user = data_handler.get_user_by_name(username)
    if not user:
        errors.append(f"User {username} does not exist")
        return flask.render_template("login.html", errors=errors)
    is_password_correct = bcrypt.checkpw(password.encode("utf-8"), user['password'].encode("utf-8"))
    if is_password_correct:
        session['username'] = user['username']
        session['user_id'] = user['user_id']
        return flask.redirect("/")
    else:
        return flask.render_template("login.html", errors=["Password incorrect"])


@app.route("/register", methods=['GET', 'POST'])
def user_register():
    if request.method == 'GET':
        return flask.render_template("register.html")
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        repeat_password = request.form['repeat_password']
    errors = []
    if not password == repeat_password:
        errors.append("Passwords not match")
    if len(password) < 4:
        errors.append("Password too short")
    if len(username) < 4:
        errors.append("Username too short")
    if data_handler.check_user_by_name(username) > 0:
        errors.append("User already exists")
    if len(errors) > 0:
        return flask.render_template("register.html", errors=errors)

    hashed_password = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
    user_id = data_handler.add_user(username, hashed_password.decode("utf-8"))
    if user_id:
        return flask.render_template("register_confirm.html")
    return flask.render_template("register.html", errors=["Unknown error, please try again later."])


@app.route("/logout")
def logout():
    session.clear()
    return flask.redirect("/")


@app.route("/users")
def list_users():
    if 'username' not in session.keys():
        return flask.render_template("users.html", errors="Not authorised")
    else:
        return flask.render_template("users.html", users=data_handler.get_users(), title="Users")


@app.route("/tags")
def list_tags():
    tags = data_handler.get_tags_stats()
    return flask.render_template("tags.html", tags=tags, title="Tags")


@app.route("/user/<user_id>")
def user_page(user_id):
    user = data_handler.get_user_by_id(user_id)
    questions = data_handler.get_user_questions(user_id)
    answers = data_handler.get_user_answers(user_id)
    comments = data_handler.get_user_comments(user_id)
    return flask.render_template("user_page.html", user=user, questions=questions, answers=answers, comments=comments,
                                 title="User page")


@app.route("/bonus-questions")
def main():
    return flask.render_template('bonus_questions.html', questions=SAMPLE_QUESTIONS)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5010, debug=True)
