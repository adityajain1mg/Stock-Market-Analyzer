from aiohttp_client_cache import CachedSession, SQLiteBackend
import asyncio
import aiohttp
import re


def break_string(x):
    pattern = r'(\d+)(\D+)'
    matches = re.match(pattern, x)
    number = matches.group(1)
    characters = matches.group(2)

    return number, characters

async def remove_cache_for_url(url):
    async with CachedSession(cache=SQLiteBackend()) as session:
        session.delete(url, ssl=False)

async def make_request(url):
    async with CachedSession(cache=SQLiteBackend()) as session:
        async with session.get(url, ssl=False) as resp:
            return await resp.json()