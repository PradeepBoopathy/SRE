import aiomysql
import asyncio
from config import config


async def create_connection():
    return await aiomysql.connect(**config.DB_CONFIG)


async def create_sample_table():
    conn = await create_connection()
    try:
        async with conn.cursor() as cur:
            # Check if the sample table exists
            await cur.execute("SHOW TABLES LIKE 'users'")
            existing_table = await cur.fetchone()
            if not existing_table:
                # Create the sample table if it doesn't exist
                await cur.execute(
                    """
                    CREATE TABLE users (
                        id INT AUTO_INCREMENT PRIMARY KEY,
                        name VARCHAR(255),
                        email VARCHAR(255),
                        username VARCHAR(255),
                        password VARCHAR(255)
                    )
                    """
                )
                await conn.commit()
    finally:
        conn.close()
        await conn.wait_closed()


# Run the create_sample_table function
async def run_create_sample_table():
    await create_sample_table()

# Run the function asynchronously
asyncio.run(run_create_sample_table())
