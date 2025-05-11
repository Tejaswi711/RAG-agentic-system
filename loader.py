import aiomysql
from typing import List, Dict

async def create_table(pool):
    """Ensure table exists"""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            await cur.execute("""
                CREATE TABLE IF NOT EXISTS federal_documents (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    document_number VARCHAR(50) UNIQUE,
                    title TEXT,
                    publication_date DATE,
                    type VARCHAR(50),
                    agencies TEXT,
                    summary TEXT,
                    full_text_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            await conn.commit()

async def load_data(pool: aiomysql.Pool, docs: List[Dict]):
    """Bulk insert processed documents"""
    async with pool.acquire() as conn:
        async with conn.cursor() as cur:
            for doc in docs:
                await cur.execute("""
                    INSERT INTO federal_documents 
                    (document_number, title, publication_date, type, agencies, summary, full_text_url)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                    title=VALUES(title), summary=VALUES(summary)
                """, (
                    doc['document_number'],
                    doc['title'],
                    doc['publication_date'],
                    doc['type'],
                    doc['agencies'],
                    doc['summary'],
                    doc['full_text_url']
                ))
            await conn.commit()