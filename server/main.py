# FastApi
from fastapi import FastAPI, Response
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

# JWT for authentication
import jwt

# PostgreSQL Driver
import psycopg2

# Loading .env file
import os
from dotenv import load_dotenv

# utils
import datetime


# Load .env --------------
load_dotenv()
JWT_SECRET = os.getenv('JWT_SECRET')
POSTGRESQL_DATABASE = os.getenv("POSTGRESQL_DATABASE")
POSTGRESQL_USER = os.getenv("POSTGRESQL_USER")
POSTGRESQL_PASSWORD = os.getenv("POSTGRESQL_PASSWORD")
POSTGRESQL_PORT = os.getenv("POSTGRESQL_PORT")


# Pydantic classes to take data from frontend json body ---------------
class RegisterData(BaseModel):
    name: str
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

class getPostData(BaseModel):
    user_id: str


# PostgresSQL connection function --------------------
def get_connection():
    try:
        return psycopg2.connect(
            database="postgres",
            user="postgres",
            password="bantu@69go",
            host="127.0.0.1",
            port=5432,
        )
    except:
        return False

conn = get_connection()

app = FastAPI()

# Adding origin to middleware ----------
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Access-Control-Allow-Headers", 'Content-Type', 'Authorization', 'Access-Control-Allow-Origin'],
)

# Routes ---------------------
@app.get("/")
async def root():
    cursor = conn.cursor()
    # cursor.execute("UPDATE users SET name = (%s) where id = 1;", (name,))
    # cursor.execute("DELETE FROM users;")
    # conn.commit()
    cursor.execute("select * from users;")
    user_data = []
    for data in cursor.fetchall():
        map = {}
        map['id'] = data[0]
        map['name'] = data[1]
        map['email'] = data[2]
        map['password'] = data[3]
        user_data.append(map)

    cursor.close()
    return user_data

@app.post("/register")
async def register(item: RegisterData):
    cursor = conn.cursor()

    # Check if user already exist
    cursor.execute("SELECT * FROM users where email = (%s)", (item.email,))
    if len(cursor.fetchall()) > 0:
        cursor.close()
        return {"error": "User Already Exists"}
    
    # If user doesn't exist, create one.
    cursor.execute("INSERT INTO users (name, email, password) values(%s, %s, %s);", (item.name, item.email, item.password))
    conn.commit()
    cursor.execute("select * from users;")
    user_data = []
    for data in cursor.fetchall():
        map = {}
        map['id'] = data[0]
        map['name'] = data[1]
        map['email'] = data[2]
        user_data.append(map)

    cursor.close()
    return user_data

@app.post("/login")
async def register(response: Response , data: LoginData):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = (%s)", (data.email,))
    user_data = cursor.fetchone()

    if (data.password == user_data[3]):
        payload = {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
            "exp": datetime.datetime.now(tz=datetime.timezone.utc) + datetime.timedelta(seconds=900)
        }
        user_data = {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
        }
        encoded_jwt = jwt.encode(payload=payload, key=JWT_SECRET , algorithm="HS256")
        response.set_cookie(key="JWT_TOKEN", value=encoded_jwt, httponly=True, secure=True, samesite='none')
        response.set_cookie(key="fakesession", value="fake-cookie-session-value", httponly=True, secure=True, samesite='none', )
        
        return user_data

    return {"error": "Wrong Password!", "flag": 1}

@app.get("/get_posts")
def get_posts(response: Response, user_id: int):
    print(user_id)
    cursor = conn.cursor()
    cursor.execute('select posts.id, posts.message, posts.created_at, channels.name from posts join channels on posts.channel_id = channels.id  where channel_id in (select user_channels.channel_id from users join user_channels on users.id = user_channels.user_id where users.id = %s);', (user_id,))
    posts = []
    # print(cursor.fetchall())
    for post in cursor.fetchall():
        temp = {}
        temp['id'] = post[0]
        temp['content'] = post[1]
        temp['date'] = post[2]
        temp['channel'] = post[3]
        posts.append(temp)
    print(posts)
    cursor.close()
    return posts

@app.post("/search/{name}")
def search(name: str):
    pass


@app.get("/cookie-and-object")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {response}