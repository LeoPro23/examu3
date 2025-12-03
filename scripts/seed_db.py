import asyncio
import asyncpg
import os

async def seed_db():
    database_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/ti_management")
    
    print(f"Connecting to {database_url}...")
    try:
        conn = await asyncpg.connect(database_url)
        
        with open("database/seeds.sql", "r", encoding="utf-8") as f:
            sql = f.read()
            
        print("Executing seeds...")
        await conn.execute(sql)
        print("Seeds executed successfully!")
        
        await conn.close()
    except Exception as e:
        print(f"Error seeding database: {e}")

if __name__ == "__main__":
    asyncio.run(seed_db())
