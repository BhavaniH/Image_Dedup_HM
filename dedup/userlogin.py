from Database.base import engine
from Database.Models import img_users, session
from dedup.splitBlocks import conn
from sqlalchemy.sql import select
from dedup.splitBlocks import rehash, getKey
import getpass


def check_user_exist(user_name):
    usernames = img_users.select().where(img_users.c.username==user_name)
    #all_names = user_name.all()
    result = conn.execute(usernames).fetchall()
    #print("usernames from DB:", result, type(result))
    for i in result:
        print("i , user name already exist:",i)
        if user_name == i[0]:
            print("user_name:", i[0])
            #return True
        else:
            return "User already exist"


def register_user(username: str, email: str, password: str):
    print("entering into user login:",username,email,password)
    hashed_password = rehash.sha256(password.encode('utf-8')).hexdigest()
    print("Hashed password :", hashed_password)
    query = img_users.insert().values(username=username,email=email,password=hashed_password)
    conn.execute(query)
    username = getpass.getuser()
    print(username)

