import os
DB_URL = "postgres://ivpallnyfezioy:075baf8e129b0d52dbd6d87dd3c774363b0b10b499921f821378ed7084bfc744@ec2-46-137-187-23.eu-west-1.compute.amazonaws.com:5432/dagmb1jla3rmdp"	#os.getenv("DATABASE_URL")

import psycopg2 as dbapi2

def check_if_user_exists(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "SELECT * FROM USERACCOUNT WHERE username=%s;"
            cursor.execute(statement, (data["password"]))
            connection.commit()
            userlist = cursor.fetchall()
            print('userlist')
            print(userlist)
            if userlist == []:
                return False
            else:
                return True



def insert_socialmedia(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO SOCIALMEDIA (facebook, twitter, instagram, discord, youtube, googleplus) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (data["facebook"], data['twitter'], data["instagram"], data["discord"], data["youtube"], data["googleplus"]))
            connection.commit()
            print("Added socialmedia")
            id = cursor.fetchone()[0]
            print(id)
            return id
    
def insert_contactinfo(data, socialmedia_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO CONTACTINFO (socialmedia, phoneNumber, email, fax, homePhone, workmail) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (socialmedia_id, data['phoneNumber'], data["email"], data["fax"], data["homePhone"], data["workmail"]))
            connection.commit()
            print("Added contactinfo")
            id = cursor.fetchone()[0]
            print(id)
            return id
    
def insert_person(data, contactinfo_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO PERSON (contactinfo, name, surname, birthDay, educationLevel, gender) VALUES (%s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (contactinfo_id, data["name"], data['surname'], data["birthday"], data["education"], data["gender"]))
            connection.commit()
            print("Added person")
            id = cursor.fetchone()[0]
            print(id)
            return id
    
    
def insert_useraccount(data, person_id):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            statement = "INSERT INTO USERACCOUNT (person, lastEntry, username, password, joinedDate, securityAnswer, membershiptype) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING id;"
            cursor.execute(statement, (person_id, data["lastEntry"], data['username'], data["password"], data["joinedDate"], data["securityAnswer"], data["membership"]))
            connection.commit()
            print("Added useraccount")
            id = cursor.fetchone()[0]
            print(id)
            return id

def create_user(data):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor() as cursor:
            if check_if_user_exists(data) == False:
                id = insert_socialmedia(data)
                id = insert_contactinfo(data, id)
                id = insert_person(data, id)
                id = insert_useraccount(data, id)
                connection.commit()
                print("User created")
                return True
            else:
                return False

def select_socialmedia():
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM SOCIALMEDIA;"
            cursor.execute(statement)
            connection.commit()
            data = cursor.fetchall()
            return data

def select_a_socialmedia(username, password):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            statement = "SELECT * FROM SOCIALMEDIA WHERE id = (SELECT socialmedia FROM CONTACTINFO FULL OUTER JOIN (SELECT contactinfo FROM PERSON FULL OUTER JOIN ((SELECT person FROM USERACCOUNT WHERE username=%s and password=%s)) AS T2 ON PERSON.id = T2.person) AS T3 ON CONTACTINFO.id = T3.contactinfo);"
            cursor.execute(statement, (username, password))
            connection.commit()
            data = cursor.fetchall()
            return data[0]

def update_socialmedia(data, username, password):
    with dbapi2.connect(DB_URL) as connection:
        with connection.cursor(cursor_factory=dbapi2.extras.RealDictCursor) as cursor:
            id = select_a_socialmedia(username, password)["id"]
            print(id)
            #print(data)
            statement = "UPDATE SOCIALMEDIA SET facebook=%s, twitter=%s, instagram=%s, discord=%s, youtube=%s, googleplus=%s WHERE id=%s"
            cursor.execute(statement, (data["facebook"], data["twitter"], data["instagram"], data["discord"], data["youtube"], data["googleplus"], id))
            connection.commit()
        