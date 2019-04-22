import flask
import jwt
import sqlite3
import requests
import time
import os
import re

from urllib.parse import unquote


app = flask.Flask(__name__)
app.config['JWT_SECRET'] = 'gSi4WmttWuvy2ewoTGooigPwSDoxwZOy'
app.config['DOWNSTREAM_HOST'] = 'http://localhost:3000'


conn = sqlite3.connect('users.db')
try:
    conn.execute("""
        CREATE TABLE "users" (
            id          varchar not null,
            class       varchar not null,
            username    varchar not null unique,
            password    varchar not null,
            token       varchar null
        );
    """)
    conn.execute("""
        INSERT INTO "users" (id, class, username, password)
        VALUES ('0', 'org.library.net.Admin', 'superuser', 'superuser')
    """)
    conn.commit()
except sqlite3.Error as e:
    print(e)


@app.route('/proxy/user/', methods=['POST'])
def create_user():
    data = flask.request.json
    if 'username' not in data or 'password' not in data or 'id' not in data or '$class' not in data:
        flask.abort(400)

    username = data.pop('username')
    password = data.pop('password')

    conn.execute(
        f"""
        INSERT INTO "users" (id, class, username, password)
        VALUES (?, ?, ?, ?);
        """,
        [data['id'], data['$class'], username, password]
    )

    s = re.escape(flask.json.dumps(data))
    exitcode = os.system(f'''
        export PATH="/usr/local/opt/node@8/bin:$PATH"
        composer participant add -c admin@library  -d {s}
    ''')
    if exitcode:
        conn.rollback()
        flask.abort(500)

    exitcode = os.system(f'''
        export PATH="/usr/local/opt/node@8/bin:$PATH"
        composer identity issue -x -c admin@library \
                                -f cards/{username}.card \
                                -u {username} \
                                -a "resource:{data["$class"]}#{data["id"]}"
    ''')
    if exitcode:
        conn.rollback()
        flask.abort(500)

    exitcode = os.system(f'''
        export PATH="/usr/local/opt/node@8/bin:$PATH"
        composer card import -f cards/{username}.card
    ''')
    if exitcode:
        conn.rollback()
        flask.abort(500)

    exitcode = os.system(f'''
        export PATH="/usr/local/opt/node@8/bin:$PATH"
        composer card export -f cards/{username}.card -c {username}@library
    ''')
    if exitcode:
        conn.rollback()
        flask.abort(500)

    conn.commit()

    return flask.json.dumps({"message": "created"}), 200


@app.route('/proxy/auth/', methods=['POST'])
def authenticate():
    data = flask.request.json
    if 'username' not in data or 'password' not in data:
        flask.abort(400)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, class, username, password, token
        FROM "users" WHERE username = ?
        """,
        [data['username']]
    )
    rows = cur.fetchall()
    if len(rows) == 0:
        flask.abort(401)

    if rows[0][3] != data['password']:
        flask.abort(401)

    token = rows[0][4]
    if token == None:
        token = jwt.encode(
            {"username": data["username"], "timestamp": time.time()},
            app.config['JWT_SECRET']
        )

        response = requests.get(
            app.config['DOWNSTREAM_HOST'] + f'/auth/jwt/callback/?token={token.decode()}',
            allow_redirects=False
        )
        if 'access_token' not in response.cookies:
            print(response, dict(response.cookies))
            flask.abort(500)

        token = unquote(response.cookies['access_token'])
        token = token.split('.')[0].split(':')[1]

        response = requests.post(
            app.config['DOWNSTREAM_HOST'] + f'/api/wallet/import?access_token={token}',
            files={"card": open(f'cards/{data["username"]}.card', 'rb')},
            data={"name": data['username']}
        )
        if not response.ok:
            print(response)
            flask.abort(500)

        conn.execute(
            f"""
            UPDATE users SET token= ? WHERE username = ?
            """,
            [token, rows[0][2]]
        )

    return flask.json.dumps({
        "id": rows[0][0],
        "class": rows[0][1],
        "username": rows[0][2],
        "token": token
    })


@app.route('/proxy/logout/', methods=['POST'])
def logout():
    data = flask.request.json
    if 'username' not in data and 'password' not in data:
        flask.abort(400)

    cur = conn.cursor()
    cur.execute(
        """
        SELECT id, class, username, password, token
        FROM "users" WHERE username = ?
        """,
        [data['username']]
    )
    rows = cur.fetchall()
    if len(rows) == 0:
        flask.abort(401)

    if rows[0][3] != data['password']:
        flask.abort(401)

    conn.execute(
        f"""
        UPDATE users SET token=? WHERE username = ?
        """,
        [None, rows[0][2]]
    )

    return flask.json.dumps({
        "message": "ok"
    })