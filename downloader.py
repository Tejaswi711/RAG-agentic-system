import aiohttp
import asyncio
import json
from datetime import datetime, timedelta
import os


async def fetch_documents(start_date: str, end_date: str) -> list:
    """Fetch documents from Federal Register API"""
    url = "https://www.federalregister.gov/api/v1/documents.json"
    params = {
        "conditions[publication_date][gte]": start_date,
        "conditions[publication_date][lte]": end_date,
        "per_page": 1000
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            if response.status == 200:
                data = await response.json()
                return data.get('results', [])
            raise Exception(f"API Error: {response.status}")


async def save_raw_data(data: list, date: str) -> str:
    """Save raw JSON for backup"""
    os.makedirs('data/raw', exist_ok=True)
    filename = f"data/raw/federal_register_{date}.json"
    with open(filename, 'w') as f:
        json.dump(data, f)
    return filename