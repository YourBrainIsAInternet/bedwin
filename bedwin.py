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
    return userid

def add_listing(userid, rent, utilities, location, bedrooms):
    locationid = str(uuid.uuid4())
    c.execute("INSERT INTO current VALUES (?, ?, ?, ?, ?, ?)", [locationid, userid, rent, utilities, location, bedrooms])
    c.execute("UPDATE user SET listingid = ? WHERE userid = ?", [locationid, userid])

def list_users():
    c.execute('SELECT * FROM user')
    print [x for x in c]

def list_listings():
    c.execute('SELECT * FROM current')
    print [x for x in c]


create_table()
firstuser = add_user('Cool Renter', 'hate@broker.com')
add_listing(firstuser, 30000, 100, 'farmville', 44) 
list_users()
list_listings()


@app.route('/')
def hello_world():
    return 'Hello World!'




if __name__ == '__main__':
    app.run()
