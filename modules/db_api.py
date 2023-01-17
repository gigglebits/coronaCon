import os

import mariadb
import sys

class user:
    def __init__(self, userID):
        self.userID = userID
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    def get_id(self):
        return self.userID

#connects to the database and passes the cursor to the function needing the connection.
def connectToDB():
    try:
        db = mariadb.connect(
            user="root",
            password="root",
            host="127.0.0.1",
            port=3306,
            database="coronacon",

            #user="root",
            #password="root"
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}")
        sys.exit(1)

    #ALlows all of the insert statements to automatically be forwarded to the databse
    db.autocommit = True

    #Creates the cursor
    cur = db.cursor()

    #Returns cursor to the function calling for the connection.
    return cur


#Checks if a username is taken. If it is the function exits with code 409. If not it checks if email is taken. If it is
#the function exits with code 410. If not it goes on to add the user and exits with code 200.
