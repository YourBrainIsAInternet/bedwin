import sqlite3, uuid
from flask import Flask
conn = sqlite3.connect('profile.db')
c = conn.cursor()
app = Flask(__name__)


def create_table():
    c.execute('DROP TABLE user')
    c.execute('DROP TABLE current')
    c.execute('DROP TABLE wanted')
    c.execute('CREATE TABLE user (userid string, name string, email string, listingid int, wantedid int)')
    c.execute('CREATE TABLE current (listingid string, userid int, rent int, utilities int, location string, bedrooms string)')
    c.execute('CREATE TABLE wanted (wantedid string, rentmin int, rentmax int, locationwant string, locationnowant string)')

def dict_factory(cursor, row):
    d = {}
    for idx, name in enumerate(cursor.description):
        d[name[0]] = row[idx]
    return d

conn.row_factory = dict_factory
c = conn.cursor()

def add_user(name, email, listingid=None, wantedid=None):
    userid = str(uuid.uuid4())
    print userid
    c.execute("INSERT INTO user VALUES (?, ?, ?, ?, ?)", [userid, name, email, listingid, wantedid])

def list_users():
    c.execute('SELECT * FROM user')
    print [x for x in c]

create_table()
add_user('Cool Renter', 'hate@broker.com')
list_users()


@app.route('/')
def hello_world():
    return 'Hello World!'




if __name__ == '__main__':
    app.run()
