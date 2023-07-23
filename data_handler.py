import connection


@connection.connection_handler
def get_questions(cursor, question_id=None, limit=None, sort_key=None, sort_dir="ASC"):
    query = """
    SELECT question.*, MAX(app_user.username) AS username, MAX(app_user.reputation) AS reputation,  COUNT(comment.id) AS comments 
    FROM question 
    LEFT JOIN app_user on app_user.user_id = question.user_id 
    LEFT JOIN comment ON question.id = comment.question_id 
    """
    if question_id:
        query += "WHERE question.id = %(question_id)s"
    query += "GROUP BY question.id "
    if sort_key:
        query += f"ORDER BY {sort_key} {sort_dir}"
    else:
        query += "ORDER BY id ASC"
    if limit:
        query += """
        LIMIT %(limit)s
        """
    cursor.execute(query, {"question_id": question_id, "limit": limit})
    return cursor.fetchall()


@connection.connection_handler
def get_user_questions(cursor, user_id):
    query = """
    SELECT * FROM question WHERE user_id = %s 
    ORDER BY title
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_user_answers(cursor, user_id):
    query = """
    SELECT * FROM answer WHERE user_id = %s 
    ORDER BY submission_time
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_user_comments(cursor, user_id):
    query = """
    SELECT * FROM comment WHERE user_id = %s 
    ORDER BY submission_time
    """
    cursor.execute(query, (user_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_question_comments(cursor, question_id):
    query = """
    SELECT comment.*, app_user.username AS username, app_user.reputation AS reputation FROM comment LEFT JOIN app_user ON app_user.user_id = comment.user_id WHERE question_id = %s
    AND answer_id IS NULL
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_question_tags(cursor, question_id):
    query = """
    SELECT tag.* FROM tag JOIN question_tag qt on tag.id = qt.tag_id 
    WHERE question_id = %s
    """
    cursor.execute(query, (question_id,))
    return cursor.fetchall()


@connection.connection_handler
def find_question(cursor, text):
    query = """
    SELECT * FROM question
    WHERE lower(title) LIKE %(title)s
    OR lower(message) like %(message)s
    """
    cursor.execute(query, {"title": f"%{text}%", "message": f"%{text}%"})
    return cursor.fetchall()


@connection.connection_handler
def get_answers(cursor, answer_id=None):
    query = """
    SELECT * FROM answer
    """
    if answer_id:
        query += """
        WHERE id = %(answer_id)s
        """
    cursor.execute(query, {"answer_id": answer_id})
    return cursor.fetchall()


@connection.connection_handler
def get_question_answers(cursor, question_id):
    query = """
    SELECT answer.*, app_user.username , app_user.reputation FROM answer LEFT JOIN app_user ON app_user.user_id = answer.user_id 
    WHERE question_id = %(question_id)s
    ORDER BY submission_time DESC
    """
    cursor.execute(query, {"question_id": question_id})
    return cursor.fetchall()


@connection.connection_handler
def add_question(cursor, question_data):
    query = """
    INSERT INTO question
    VALUES(default, now(), default, default, %(title)s, %(message)s, %(image)s, %(user_id)s)
    RETURNING id
    """
    cursor.execute(query, dict(question_data))
    return cursor.fetchall()[0]['id']


@connection.connection_handler
def update_question(cursor, question_data):
    query = """
    UPDATE question
    SET title = %(title)s, message = %(message)s, image = %(image)s
    WHERE id = %(id)s
    RETURNING id
    """
    cursor.execute(query, dict(question_data))
    return cursor.fetchall()[0]['id']


@connection.connection_handler
def add_answer(cursor, answer_data):
    query = """
    INSERT INTO answer
    VALUES(default, now(), default,  %(question_id)s, %(message)s, %(image)s, %(user_id)s)
    RETURNING question_id
    """
    cursor.execute(query, dict(answer_data))
    return cursor.fetchall()[0]['question_id']


@connection.connection_handler
def delete_answer(cursor, answer_id):
    query = """
    DELETE FROM answer WHERE id = %s
    """
    cursor.execute(query, (answer_id,))
    return None


@connection.connection_handler
def update_answer(cursor, answer_data):
    query = """
    UPDATE answer
    SET message = %(message)s, image = %(image)s
    WHERE id = %(id)s
    RETURNING question_id
    """
    cursor.execute(query, dict(answer_data))
    return cursor.fetchall()[0]['question_id']


@connection.connection_handler
def toogle_accept_answer(cursor, answer_id):
    query = """
    UPDATE answer
    SET is_accepted = NOT is_accepted
    WHERE id = %s
    """
    cursor.execute(query, (answer_id,))
    return None


@connection.connection_handler
def delete_question(cursor, question_id):
    query = """
    DELETE FROM question WHERE id = %s
    """
    cursor.execute(query, (question_id,))
    return None


@connection.connection_handler
def vote_answer(cursor, answer_id, vote_change):
    query = """
    UPDATE answer SET vote_number = vote_number + %s
    WHERE id = %s 
    """
    cursor.execute(query, (vote_change, answer_id))
    return None


@connection.connection_handler
def vote_question(cursor, question_id, vote_change):
    query = """
    UPDATE question SET vote_number = vote_number + %s
    WHERE id = %s 
    """
    cursor.execute(query, (vote_change, question_id))
    return None


@connection.connection_handler
def add_question_comment(cursor, comment_data):
    query = """
    INSERT INTO comment 
    VALUES(default, %(id)s, NULL, %(message)s, now(), 0, %(user_id)s)
    RETURNING question_id
    """
    cursor.execute(query, dict(comment_data))
    return cursor.fetchall()[0]['question_id']


@connection.connection_handler
def add_answer_comment(cursor, comment_data):
    query = """
    INSERT INTO comment 
    VALUES(default, %(question_id)s, %(id)s, %(message)s, now(), 0, %(user_id)s)
    RETURNING question_id
    """
    cursor.execute(query, dict(comment_data))
    return cursor.fetchall()[0]['question_id']


@connection.connection_handler
def delete_question_tag(cursor, question_id, tag_id):
    query = """
    DELETE FROM question_tag WHERE question_id = %s AND tag_id = %s
    """
    cursor.execute(query, (question_id, tag_id))
    return None


@connection.connection_handler
def get_available_tags(cursor):
    query = "SELECT * FROM tag ORDER BY name"
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def add_new_tag(cursor, tag_name):
    query = "INSERT INTO tag(name) VALUES(%s) RETURNING id"
    cursor.execute(query, (tag_name,))
    return cursor.fetchall()[0]['id']


@connection.connection_handler
def add_question_tag(cursor, tag_data):
    if tag_data['new_tag_name']:
        tag_data['tag_id'] = add_new_tag(tag_data['new_tag_name'])
    query = """
    INSERT INTO question_tag VALUES(%s, %s)
    ON CONFLICT DO NOTHING;
    """
    cursor.execute(query, (tag_data['question_id'], tag_data['tag_id']))
    return None


@connection.connection_handler
def get_answer_comments(cursor, answer_id):
    query = "SELECT comment.*, app_user.username AS username FROM comment LEFT JOIN app_user ON app_user.user_id = comment.user_id WHERE answer_id = %s ORDER BY submission_time DESC"
    cursor.execute(query, (answer_id,))
    return cursor.fetchall()


@connection.connection_handler
def get_comment(cursor, comment_id):
    query = "SELECT * FROM comment WHERE id = %s"
    cursor.execute(query, (comment_id,))
    return cursor.fetchall()


@connection.connection_handler
def update_comment(cursor, comment_data):
    query = "UPDATE comment SET message = %(message)s, submission_time = now(), edited_count = edited_count + 1 WHERE id = %(id)s RETURNING question_id"
    cursor.execute(query, comment_data)
    return cursor.fetchall()[0]['question_id']


@connection.connection_handler
def delete_comment(cursor, comment_id):
    query = "DELETE FROM comment where id = %s"
    cursor.execute(query, (comment_id,))
    return None


@connection.connection_handler
def add_user(cursor, username, hashed_password):
    cursor.execute("INSERT INTO app_user(username, password) VALUES (%s, %s) RETURNING user_id",
                   (username, hashed_password))
    return cursor.fetchone()['user_id']


@connection.connection_handler
def check_user_by_name(cursor, username):
    cursor.execute("SELECT count(user_id) AS count FROM app_user WHERE username = %s", (username,))
    return cursor.fetchone()['count']


@connection.connection_handler
def get_user_by_name(cursor, username):
    cursor.execute("SELECT * FROM app_user WHERE username = %s", (username,))
    return cursor.fetchone()


@connection.connection_handler
def get_user_by_id(cursor, user_id):
    cursor.execute("SELECT * FROM app_user WHERE user_id = %s", (user_id,))
    return cursor.fetchone()


@connection.connection_handler
def get_users(cursor):
    query = """
    SELECT app_user.*, COUNT(distinct question.id) as questions, COUNT(distinct answer.id) AS answers, COUNT(distinct comment.id) AS comments FROM app_user
    LEFT JOIN question ON question.user_id = app_user.user_id
    LEFT JOIN answer ON answer.user_id = app_user.user_id
    LEFT JOIN comment ON comment.user_id = app_user.user_id
    GROUP BY app_user.user_id
    """
    cursor.execute(query)
    return cursor.fetchall()


@connection.connection_handler
def update_user_reputation(cursor, user_id, value):
    query = """
    UPDATE app_user SET reputation = reputation + %s
    WHERE user_id = %s
    """
    cursor.execute(query, (value, user_id))


@connection.connection_handler
def get_tags_stats(cursor):
    query = """
    SELECT tag.name, COUNT(qt.question_id) AS counter FROM tag JOIN question_tag qt on tag.id = qt.tag_id
    GROUP BY tag.name
    ORDER BY tag.name
    """
    cursor.execute(query)
    return cursor.fetchall()
