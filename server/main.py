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
JWT_SECRET = os.getenv("JWT_SECRET")
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


class searchQuery(BaseModel):
    channel_name: str


class JoinChannel(BaseModel):
    channel_id: int
    user_id: int


class LeaveChannel(BaseModel):
    channel_id: int
    user_id: int


class AddPostData(BaseModel):
    user_id: int
    channel_id: int
    message: str
    title: str


class DeletePost(BaseModel):
    post_id: int


class AddComment(BaseModel):
    user_id: int
    post_id: int
    comment: str


# PostgresSQL connection function --------------------
def get_connection():
    try:
        return psycopg2.connect(
            database=POSTGRESQL_DATABASE,
            user=POSTGRESQL_USER,
            password=POSTGRESQL_PASSWORD,
            host="127.0.0.1",
            port=POSTGRESQL_PORT,
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
    allow_headers=[
        "Access-Control-Allow-Headers",
        "Content-Type",
        "Authorization",
        "Access-Control-Allow-Origin",
    ],
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
        map["id"] = data[0]
        map["name"] = data[1]
        map["email"] = data[2]
        map["password"] = data[3]
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
    cursor.execute(
        "INSERT INTO users (name, email, password) values(%s, %s, %s);",
        (item.name, item.email, item.password),
    )
    conn.commit()
    cursor.execute("select * from users;")
    user_data = []
    for data in cursor.fetchall():
        map = {}
        map["id"] = data[0]
        map["name"] = data[1]
        map["email"] = data[2]
        user_data.append(map)

    cursor.close()
    return user_data


@app.post("/login")
async def register(response: Response, data: LoginData):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = (%s)", (data.email,))
    user_data = cursor.fetchone()
    cursor.execute(
        "select channels.id, channels.name from user_channels join channels on user_channels.channel_id = channels.id where user_channels.user_id = %s;",
        (user_data[0],),
    )
    user_channels = cursor.fetchall()
    cursor.execute("select id from posts where user_id = %s;", (user_data[0],))
    user_post = cursor.fetchall()

    if data.password == user_data[3]:
        payload = {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
            "exp": datetime.datetime.now(tz=datetime.timezone.utc)
            + datetime.timedelta(seconds=900),
        }
        user_data = {
            "id": user_data[0],
            "name": user_data[1],
            "email": user_data[2],
            "channels": [],
            "post_ids": [],
        }
        for channel in user_channels:
            user_data["channels"].append(
                {"channel_id": channel[0], "channel_name": channel[1]}
            )
        for post_id in user_post:
            print(post_id[0])
            user_data["post_ids"].append(post_id[0])
        encoded_jwt = jwt.encode(payload=payload, key=JWT_SECRET, algorithm="HS256")
        response.set_cookie(
            key="JWT_TOKEN",
            value=encoded_jwt,
            httponly=True,
            secure=True,
            samesite="none",
        )
        response.set_cookie(
            key="fakesession",
            value="fake-cookie-session-value",
            httponly=True,
            secure=True,
            samesite="none",
        )

        cursor.close()
        return user_data
    cursor.close()
    return {"error": "Wrong Password!", "flag": 1}


@app.get("/get_posts")
def get_posts(response: Response, user_id: int):
    print(user_id)
    cursor = conn.cursor()
    cursor.execute(
        "select posts.id, posts.message, posts.created_at, posts.title, channels.name from posts join channels on posts.channel_id = channels.id  where channel_id in (select user_channels.channel_id from users join user_channels on users.id = user_channels.user_id where users.id = %s) order by posts.created_at DESC;",
        (user_id,),
    )
    fetched_data = cursor.fetchall()
    # print(fetched_data)
    posts = []
    # print(cursor.fetchall())
    for post in fetched_data:
        temp = {}
        temp["id"] = post[0]
        temp["content"] = post[1]
        temp["date"] = post[2]
        temp["title"] = post[3]
        temp["channel"] = post[4]
        posts.append(temp)
    # print(posts)
    cursor.close()
    return posts


@app.get("/search")
def search(query: str):
    cursor = conn.cursor()
    cursor.execute("select * from channels where name = %s;", (query,))

    channel_found = cursor.fetchall()
    if len(channel_found) == 0:
        cursor.close()
        return {"flag": 0}

    channel_response = []
    for channel in channel_found:
        temp = {}
        temp["channel_id"] = channel[0]
        temp["channel_name"] = channel[1]
        channel_response.append(temp)
    cursor.close()
    return channel_response


@app.get("/get_user")
def get_posts(response: Response, user_id: int):
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = (%s)", (user_id,))
    user_data = cursor.fetchone()
    cursor.execute(
        "select channels.id, channels.name from user_channels join channels on user_channels.channel_id = channels.id where user_channels.user_id = %s;",
        (user_data[0],),
    )
    user_channels = cursor.fetchall()
    cursor.execute("select id from posts where user_id = %s;", (user_data[0],))
    user_post = cursor.fetchall()

    user_data = {
        "id": user_data[0],
        "name": user_data[1],
        "email": user_data[2],
        "channels": [],
        "post_ids": [],
    }
    for channel in user_channels:
        user_data["channels"].append(
            {"channel_id": channel[0], "channel_name": channel[1]}
        )
    for post_id in user_post:
        user_data["post_ids"].append(post_id[0])
    cursor.close()
    return user_data


@app.get("/get_channel")
def get_channel(channel_name: str):
    cursor = conn.cursor()
    cursor.execute(
        "select * from posts join channels on channels.id = posts.channel_id where channels.name = %s order by created_at DESC;",
        (channel_name,),
    )

    channel_found = cursor.fetchall()
    if len(channel_found) == 0:
        cursor.close()
        return {"flag": 0}

    all_post = []
    channel_data = {
        "channel_name": channel_found[0][-1],
        "channel_id": channel_found[0][-2],
    }
    for channel in channel_found:
        temp = {}
        temp["channel_id"] = channel[0]
        temp["channel"] = channel[-1]
        temp["content"] = channel[3]
        temp["title"] = channel[5]
        temp["date"] = channel[4]
        all_post.append(temp)
    channel_data["posts"] = all_post

    cursor.close()
    return channel_data


@app.get("/get_post_with_comment")
def get_post_with_comment(post_id: int):
    cursor = conn.cursor()
    cursor.execute(
        "select * from posts join channels on channels.id = posts.channel_id where posts.id = %s ",
        (post_id,),
    )
    post = cursor.fetchall()
    cursor.execute(
        "select * from comments where post_id = %s",
        (post_id,),
    )
    comments = cursor.fetchall()

    print(post[0])

    get_post_with_data = {
        "id": post[0][0],
        "content": post[0][3],
        "date": post[0][4],
        "title": post[0][5],
        "channel": post[0][-1],
        "comments": [],
    }

    for comment in comments:
        get_post_with_data["comments"].append(
            {
                "comment_id": comment[0],
                "user_id": comment[1],
                "post_id": comment[2],
                "comment": comment[3],
                "date": comment[4],
            }
        )

    cursor.close()
    return get_post_with_data


@app.post("/join_channel")
def join_channel(response: Response, data: JoinChannel):
    cursor = conn.cursor()
    cursor.execute(
        "insert into user_channels(user_id, channel_id) values(%s, %s);",
        (data.user_id, data.channel_id),
    )
    if cursor.rowcount == 1:
        conn.commit()
        cursor.close()
        return {"flag": 1}
    cursor.close()
    return {"flag": 0}


@app.post("/leave_channel")
def leave_channel(response: Response, data: JoinChannel):
    cursor = conn.cursor()
    cursor.execute(
        "delete from user_channels where user_id = %s and channel_id = %s;",
        (data.user_id, data.channel_id),
    )
    if cursor.rowcount == 1:
        conn.commit()
        cursor.close()
        return {"flag": 1}
    cursor.close()
    return {"flag": 0}


@app.post("/add_post")
def add_post(response: Response, data: AddPostData):
    cursor = conn.cursor()
    cursor.execute(
        "insert into posts(user_id, channel_id, message, title) values(%s, %s, %s, %s);",
        (data.user_id, data.channel_id, data.message, data.title),
    )
    if cursor.rowcount == 1:
        conn.commit()
        cursor.close()
        return {"flag": 1}
    cursor.close()
    return {"flag": 0}


@app.post("/add_comment")
def add_post(response: Response, data: AddComment):
    cursor = conn.cursor()
    cursor.execute(
        "insert into comments(user_id, post_id, comment) values(%s, %s, %s);",
        (data.user_id, data.post_id, data.comment),
    )
    if cursor.rowcount == 1:
        conn.commit()
        cursor.close()
        return {"flag": 1}
    cursor.close()
    return {"flag": 0}


@app.post("/delete_post")
def delete_post(response: Response, data: DeletePost):
    cursor = conn.cursor()
    cursor.execute("delete from posts where id = %s", (data.post_id,))
    if cursor.rowcount == 1:
        conn.commit()
        cursor.close()
        return {"flag": 1}
    cursor.close()
    return {"flag": 0}


@app.get("/cookie-and-object")
def create_cookie(response: Response):
    response.set_cookie(key="fakesession", value="fake-cookie-session-value")
    return {response}
