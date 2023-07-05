from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import aiomysql
from config import config
from cryptography.fernet import Fernet
import uvicorn

app = FastAPI()
cipher = Fernet(config.ENCRYPTION_KEY)


class User(BaseModel):
    name: str
    email: str
    username: str
    password: str

async def create_connection():
    return await aiomysql.connect(**config.DB_CONFIG)

def encrypt_data(data: str) -> str:
    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data.decode()


def decrypt_data(data: str) -> str:
    decrypted_data = cipher.decrypt(data.encode())
    return decrypted_data.decode()


@app.post('/register')
async def register_user(user: User):
    async with create_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE username = %s", (user.username,))
            existing_user = await cur.fetchone()
            if existing_user:
                raise HTTPException(status_code=400, detail='Username already taken')
            encrypted_user = User(
                name=encrypt_data(user.name),
                email=encrypt_data(user.email),
                username=user.username,
                password=user.password
            )
            await cur.execute(
                "INSERT INTO users (name, email, username, password) VALUES (%s, %s, %s, %s)",
                (encrypted_user.name, encrypted_user.email, encrypted_user.username, encrypted_user.password)
            )
            await conn.commit()

    return {'message': 'User registered successfully'}


@app.post('/login')
async def login_user(credentials: User):
    async with create_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT * FROM users WHERE username = %s", (credentials.username,))
            matching_user = await cur.fetchone()
            if not matching_user or decrypt_data(matching_user[4]) != credentials.password:
                raise HTTPException(status_code=401, detail='Invalid credentials')

    return {'message': 'Login successful'}


@app.get('/retrieve_email/{username}')
async def retrieve_email(username: str):
    async with create_connection() as conn:
        async with conn.cursor() as cur:
            await cur.execute("SELECT email FROM users WHERE username = %s", (username,))
            matching_user = await cur.fetchone()
            if not matching_user:
                raise HTTPException(status_code=404, detail='User not found')

    email = decrypt_data(matching_user[0])
    return {'email': email}

if __name__ == '__main__':
    uvicorn.run(app, host='0.0.0.0', port=8000)
