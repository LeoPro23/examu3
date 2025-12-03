import asyncio
import asyncpg
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ti_management")

async def init_db():
    print(f"Connecting to {DATABASE_URL}...")
    try:
        conn = await asyncpg.connect(DATABASE_URL)
        print("Connected successfully.")
        
        # Read schema.sql
        with open("database/schema.sql", "r") as f:
            schema = f.read()
            
        print("Executing schema...")
        await conn.execute(schema)
        print("Schema executed successfully.")
        
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(init_db())
