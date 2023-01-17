import os

import mariadb
import sys
import bcrypt

class user:
    def __init__(self, userID):
        self.userID = userID
        self.is_authenticated = True
        self.is_active = True
        self.is_anonymous = False
    def get_id(self):
        return self.userID

pepper = "Mizzou2022!_IMT"
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
def newUser(user_id, name, password):
    #Calls the connect to DB function to get the curson.
    cur = connectToDB()

    #Checks to see if the username is already taken returns code 409 if it is.
    print(user_id)
    try:
        cur.execute("SELECT user_id FROM users WHERE user_id =?", (user_id,))

        for x in cur:
            check=x
            x = check[0]
            if x == username:
                raise Exception('e')
            else:
                continue

    except:
        #Returns 409 if the username is taken.
        return 409

    #Separate the password.
    password_hash = password.hash
    seasoning = password.salt

    #Writes the INSERT statements for the space and person.
    cur.execute("INSERT INTO users (user_id, name, password, salt) VALUES (?, ?, ?, ?)", (user_id, name, password_hash, seasoning))

    #Test print.
    cur.execute("SELECT * FROM person")
    for x in cur:
        print(x)

    #Returns 200 if everything went ok.
    return 200

#Checks a username and password. Returns 409 if username isn't found. 403 if the password is incorrect. And 200 if everything
#goes through. Is used by login function from forms.py.

##########Need it to return a user object.
def user_login(username, password):

    ###connection to database
    cur = connectToDB()

    try:
    ###Queries the DB for user_id, password, and salt.
        cur.execute("SELECT user_id, name, password, salt FROM users WHERE user_id =?", (username,))
        #cur.execute(f"SELECT user_id FROM person WHERE user_id = 'ilnam'")

    ###Puts the results of the query in a list.
        for x in cur:
            person = x

        print(person)
        #user_username = person[0]

    ###Puts the user's stored pasword into a variable user_pass and then encodes it in utf-8
        user_pass = person[1]
        user_pass = user_pass.encode('utf-8')
        print(user_pass)

    ###Put's the user's salt into a variable salt, then encodes it in utf-8
        salt = person[2]
        salt = salt.encode('utf-8')
        print(salt)

    ###Put's the root space into a variable
        root_space = person[3]

    ###Adds the pepper to the provided password, then hashes submitted password with the user's salt
        password = password + pepper
        hashed_pass = bcrypt.hashpw(password.encode('utf-8'), salt)
        print(hashed_pass)

    ###Test prints
        print('******')
        print(user_pass)
        print(hashed_pass)

    ###Checks to see if the hashed submitted password is equal to the password stored in the DB and returns 200 if so and 403 if not.
        if hashed_pass == user_pass:
            #Returns 200 if password is good
            return user(username, root_space)
        else:
            #Returns 403 if pass is bad.
            return 403

    except:
        #Returns 409 if username can't be found.
        return 409



def get_user(userID):
    cur = connectToDB()
    try:
        cur.execute("SELECT user_id, root_space_id FROM person WHERE user_id =?", (userID,))
        returnDict = {}
        for (user_id, root_space_id) in cur:
            returnDict[user_id] = root_space_id

        if len(returnDict) != 1:
            return None
        else:
            return returnDict

    except:
        #Returns 409 if the username is taken.
        return None


def load_user_helper(user_id):
    cur = connectToDB()
    cur.execute("SELECT root_space_id FROM person WHERE user_id =?", (user_id,))
    try:
        for x in cur:
            rootSpace = x

        rootSpace = rootSpace[0]
        returnObject = user(user_id, rootSpace)
        return returnObject
    except:
        return None
